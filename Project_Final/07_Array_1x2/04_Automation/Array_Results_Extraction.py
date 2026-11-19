"""Postprocess native CST curves, angular cuts, paired local fields and the mesh study."""
from Array_Audit import load_curve,band_edges,audit
from pathlib import Path
import numpy as np,csv,json,math,re
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'06_Working';P=ROOT/'01_CST_Project';R=ROOT/'02_Simulation_Results';C=ROOT/'03_Comparison';DOC=ROOT/'05_Documentation';ORIG=ROOT.parent/'02_Simulation_Results'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(path,rows):
    if not rows:return
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
def sphere(folder):
    a=np.loadtxt(folder/'Farfield_150_Sphere.txt',skiprows=2);a=a[np.lexsort((a[:,0],a[:,1]))];th=np.unique(a[:,0]);ph=np.unique(a[:,1]);v=a[:,2].reshape(len(ph),len(th))
    lin=10**(v/10);q=np.trapezoid(lin*np.sin(np.radians(th)),np.radians(th),axis=1);norm=np.trapezoid(np.r_[q,q[0]],np.radians(np.r_[ph,360]))/(4*np.pi)
    peak=a[np.argmax(a[:,2])];out=dict(D_broadside_dBi=v[0,0],theta_deg=peak[0],phi_deg=peak[1],sphere_mean=norm,broadside_Ephi_dBi=a[0,5],broadside_Etheta_dBi=a[0,3])
    curves={}
    for name,phi in [('E',90),('H',0)]:
        t=np.r_[-th[:0:-1],th];d=np.r_[v[np.where(ph==phi+180)[0][0],:0:-1],v[np.where(ph==phi)[0][0]]];k=np.argmax(d);target=d[k]-3
        il=np.flatnonzero(d[:k]<target)[-1];ir=k+1+np.flatnonzero(d[k+1:]<target)[0]
        lo=np.interp(target,d[il:il+2],t[il:il+2]);hi=np.interp(target,d[ir-1:ir+1][::-1],t[ir-1:ir+1][::-1])
        out.update({name+'_HPBW_deg':hi-lo,name+'_low_deg':lo,name+'_high_deg':hi})
        maxima=np.flatnonzero((d[1:-1]>d[:-2])&(d[1:-1]>=d[2:]))+1
        others=[d[i] for i in maxima if i!=k and abs(t[i])<90]
        out[name+'_other_forward_peak_relative_dB']=max(others)-d[k] if others else None
        curves[name]=(t,d)
    return out,curves
def raw(folder):
    return folder/'CST_Raw' if folder==ORIG else folder
def frequency(folder):
    rows=[]
    for v in sorted(read(folder/'summary.json')['farfields'],key=lambda t:t['f_GHz']):
        rows.append(dict(f_GHz=v['f_GHz'],S11_dB=v['s11_dB'],Dmax_dBi=v['Dmax_dBi'],realized_gain_dBi=v['realized_gain_dBi'],rad_eff_pct=100*10**(v['rad_eff_dB']/10),total_eff_pct=100*10**(v['total_eff_dB']/10)))
    return rows
def scattering(folder):
    f,g=load_curve(raw(folder),r'1D Results\S-Parameters\S1,1');x,zref=load_curve(raw(folder),r'1D Results\Reference Impedance\ZRef 1(1)')
    z0=np.interp(f,x,zref.real);z=z0*(1+g)/(1-g);g50=(z-50)/(z+50)
    return f,g,z0,z,g50
def metrics(folder,pattern=None):
    ff=frequency(folder);op=next(v for v in ff if v['f_GHz']==150).copy();f,g,z0,z,g50=scattering(folder)
    k=np.argmin(abs(f-150));db=20*np.log10(abs(g));bands=band_edges(f,db);band=next((v for v in bands if v['f_low_GHz']<=150<=v['f_high_GHz']),max(bands,key=lambda v:v['BW_GHz']) if bands else {})
    op.update(band);op.update(fmin_GHz=f[np.argmin(abs(g))],minimum_S11_dB=min(db),Zre150_ohm=z[k].real,Zim150_ohm=z[k].imag,reference_ohm=z0[k],S11_50_dB=20*np.log10(abs(g50[k])),realized_50_dBi=op['Dmax_dBi']+10*np.log10(op['rad_eff_pct']/100*(1-abs(g50[k])**2)))
    sp,_=sphere(pattern or folder);op.update(sp);op['realized_broadside_dBi']=op['D_broadside_dBi']+10*np.log10(op['total_eff_pct']/100)
    projects=list(folder.glob('*.cst'))
    if projects:
        log=(projects[0].with_suffix('')/'Result'/'Model.log').read_text(errors='replace')
        matches=re.findall(r'Number of mesh cells:\s*(\d+)',log);op['cells']=int(matches[-1]) if matches else None
    return op
def field_rows(folder):
    a=np.loadtxt(folder/'Branch_Ez_150.txt',skiprows=2);out=[]
    for y in np.unique(a[:,1]):
        pair=a[np.isclose(a[:,1],y)];pair=pair[np.argsort(pair[:,0])];assert len(pair)==2
        el,er=pair[:,7]+1j*pair[:,8]
        out.append(dict(y_mm=y,x_left_mm=pair[0,0],x_right_mm=pair[1,0],z_mm=pair[0,2],left_Ez_V_per_m=abs(el),right_Ez_V_per_m=abs(er),right_minus_left_dB=20*np.log10(abs(er/el)),right_minus_left_deg=np.angle(er/el,deg=True)))
    return out
def main():
    ver=read(R/'Verification.json');source=ver['source'];selected=read(W/'selection.json')['name']
    ff=frequency(P);write(R/'Final_Array_Performance.csv',ff)
    for name,key in [('Directivity','Dmax_dBi'),('Realized_Gain','realized_gain_dBi'),('Radiation_Efficiency','rad_eff_pct'),('Total_Efficiency','total_eff_pct')]:
        write(R/(name+'.csv'),[{'f_GHz':v['f_GHz'],key:v[key]} for v in ff])
    f,g,z0,z,g50=scattering(P);write(R/'S11.csv',[dict(f_GHz=x,S_real=y.real,S_imag=y.imag,S11_native_dB=20*np.log10(abs(y)),native_reference_ohm=ref,S11_common50_dB=20*np.log10(abs(yy))) for x,y,ref,yy in zip(f,g,z0,g50)])
    sp,curves=sphere(R)
    for name,(ang,d) in curves.items():write(R/(name+'_Plane.csv'),[dict(signed_angle_deg=t,absolute_directivity_dBi=v,relative_to_cut_peak_dB=v-max(d)) for t,v in zip(ang,d)])
    (R/'Sphere_Normalization.json').write_text(json.dumps(sp,indent=2))
    checks=audit(P);write(R/'Power_Balance.csv',checks['farfield_checks']);write(R/'Impedance_Bandwidth.csv',checks['matched_bands'])
    history=[]
    for file in sorted(W.glob('*/summary.json')):
        folder=file.parent
        if not (folder/'Farfield_150_Sphere.txt').exists():continue
        p=read(folder/'parameters.json');s=read(file);v=metrics(folder)
        label='Ground size control' if folder.name=='GroundControl' else 'Final source mesh' if folder.name==source else 'Selected screening geometry' if folder.name==selected else 'Mesh sensitivity' if folder.name in ['Fine','Refined','Medium'] else 'Screening candidate'
        warnings=' | '.join(dict.fromkeys(str(t.get('text','')).strip() for t in s['messages'] if t.get('type')=='WARNING'))
        history.append(dict(name=folder.name,role=label,native_project=s['project'],solver=s['solver']['state'],**p,**v,warnings=warnings))
    write(R/'Optimisation_History.csv',history)
    geom=read(P/'parameters.json');mesh=[v for v in history if v['name']!='Final50' and all(float(v.get(k,-99))==float(u) for k,u in geom.items() if k not in ['mesh_near','mesh_box'])];mesh.sort(key=lambda v:v['cells'])
    for v in history:
        roles={'MeshHoldout':'Independent higher-resolution validation','Refined':'Selected physical mesh','RetunedFine':'Fine-grid validation of retuned geometry','Spacing120_Retuned':'Resonance retuning and coarse comparator','Fine':'Fine-grid validation of initial screening winner'}
        v['role']=roles.get(v['name'],v['role'])
        if v['role']=='Screening candidate':
            v['selection_reason']='Outside -10 dB match at 150 GHz' if v['S11_dB']>-10 else 'Matched screening result with lower realized gain than winner'
        else:v['selection_reason']=v['role']
    write(R/'Optimisation_History.csv',history)
    write(R/'Mesh_Convergence.csv',mesh);write(R/'Branch_Balance.csv',field_rows(R))
if __name__=='__main__':main()



