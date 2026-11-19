"""Postprocess archived CST outputs; zero interpolation of farfields in frequency."""
from Array_Results_Extraction import sphere,scattering,band_edges,field_rows,write
from pathlib import Path
import json,csv,re,math,shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT.parent/'07_Array_1x2';BASE=ROOT/'01_Baseline_Copy/01_CST_Project'
D,F,T,V,R,DOC=[ROOT/k for k in ['02_Loss_Diagnostics','03_Feed_Optimisation','04_Substrate_Metal_Study','06_Final_Candidate','07_Results_and_Figures','09_Documentation']]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def data(p):
    with p.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def dump(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf-8')
def sources():
    ref=OLD/'03_Comparison';oldfolders=[ROOT.parent/'02_Simulation_Results',OLD/'06_Working/GroundControl',BASE]
    ret=[]
    for n,c,p,b,src,key in zip(['Original Single Patch','Enlarged-Ground Single Patch','Previous 1x2 Array'],data(ref/'Common50_150GHz.csv'),data(ref/'Three_Model_Power_150GHz.csv'),data(ref/'Common_50ohm_Bandwidth.csv'),oldfolders,['original','ground_control','array']):
        flow=src/'CST_Raw' if key=='original' else src
        pp=float(next(v for v in data(flow/'1D Results_Power_Excitation [1]_Power Absorbed at all Ports.csv') if abs(float(v['x'])-150)<1e-5)['real'])
        m=read(ref/'Comparison_Metrics.json')[key];row=dict(name=n,group='validated historical',source=str(src),eta=float(c['rad_eff_pct']),G50=float(c['realized_gain_50_dBi']),D=float(c['directivity_dBi']),S11_50=float(c['reflection_50_dB']),eta_total50=float(c['total_eff_50_pct']),bandwidth50=float(b['BW_GHz']),low50=float(b['f_low_GHz']),high50=float(b['f_high_GHz']),Pport=pp,solver=read(src/'summary.json')['solver']['state'])
        for dest,orig in [('Pacc','Paccepted_W'),('Prad','Prad_W'),('Pin','Pstim_W'),('Pout','Poutgoing_W'),('Pmetal','Pmetal_W'),('Pdiel','Pdielectric_W')]:row[dest]=float(p[orig])
        row['residual_pct']=100*(row['Pacc']-row['Prad']-row['Pmetal']-row['Pdiel']-pp)/row['Pacc']
        for k in ['E_HPBW_deg','H_HPBW_deg','theta_deg','sphere_mean']:row[k]=m[k]
        ret.append(row)
    return ret
def case(folder):
    m=read(folder/'completed.json');p=read(folder/'parameters.json');sp,_=sphere(folder)
    log=(folder/folder.name/'Result/Model.log').read_text(errors='replace');c=re.findall(r'Number of mesh cells:\s*([\d]+)',log)
    assert c
    m.update(source=str(folder),cells=int(c[-1]),**p,**sp)
    m['group']='ideal diagnostic' if p.get('pec') or p['loss_tangent']==0 else 'numerical diagnostic' if 'mode_factor' in p else 'real materials'
    return m
def save(fig,name):
    fig.tight_layout();fig.savefig(R/(name+'.png'),dpi=155,bbox_inches='tight');plt.close(fig)
def freq(folder):
    f,g,z0,z,g50=scattering(folder);rows=[]
    s=read(folder/'summary.json')
    for q in s['farfields']:
        k=np.argmin(abs(f-q['f_GHz']));eta=10**(q['rad_eff_dB']/10)
        rows.append(dict(GHz=q['f_GHz'],D=q['Dmax_dBi'],G50=q['Dmax_dBi']+10*np.log10(eta*(1-abs(g50[k])**2)),rad_pct=100*eta,total50_pct=100*eta*(1-abs(g50[k])**2)))
    return sorted(rows,key=lambda v:v['GHz'])
def main():
    verification=read(V/'verification.json');folder=Path(verification['path']).parent;allcases=[case(f.parent) for stage in [D,F,T,V] for f in sorted(stage.glob('*/completed.json'))]
    final=next(v for v in allcases if v['source']==str(folder));s=sources();s.append(final);diag=[v for v in allcases if v['group']=='ideal diagnostic']
    write(R/'Efficiency_Optimisation_Comparison.csv',s+diag);write(R/'All_Candidates.csv',allcases)
    dct={v['name']:v for v in allcases};baseline=read(R/'Baseline_Power_Recomputed.json')
    fig,ax=plt.subplots(figsize=(9,4.3));li=s+diag;ax.bar(range(len(li)),[v['eta'] for v in li],color=['#46758e','#46758e','#46758e','#08795c']+['#b88b55']*len(diag));ax.axhline(80,ls=':',color='#933');ax.set(xticks=range(len(li)),xticklabels=['Original','Larger ground','Previous array','Final array']+[v['name'].split('_',1)[1] for v in diag],ylabel='Radiation efficiency (%)',ylim=(0,105),title='150 GHz • actual efficiency, ideal diagnostics in tan');ax.tick_params(axis='x',labelrotation=15);save(fig,'Radiation_Efficiency_Comparison')
    for k,name in [('Pmetal','Metal_Loss'),('Pdiel','Dielectric_Loss')]:
        fig,ax=plt.subplots(figsize=(8,4));labels=['Original','Larger ground','Previous array','Final array']+[v['name'].split('_',1)[1] for v in diag];ax.bar(labels,[100*v[k]/v['Pacc'] for v in li],color=['#48788f']*3+['#08795c']+['#b88b55']*len(diag));ax.set(ylabel='Fraction of accepted power (%)',title=name.replace('_',' ')+' at 150 GHz');ax.tick_params(axis='x',labelrotation=17);save(fig,name+'_Comparison')
    fig,ax=plt.subplots(figsize=(7,4.5));bottom=np.zeros(4);labels=['Original','Larger ground','Previous array','Final array']
    for k,lab in [('Prad','Radiated'),('Pmetal','Gold'),('Pdiel','Polyimide'),('Pport','Port absorption')]:
        a=np.array([v[k]/v['Pacc']*100 for v in s]);ax.bar(labels,a,bottom=bottom,label=lab);bottom+=a
    ax.set(ylabel='Fraction of accepted power (%)',title='150 GHz power budget');ax.legend(fontsize=8,ncol=2);save(fig,'Power_Breakdown')
    orig=ROOT.parent/'02_Simulation_Results';oldpattern=OLD/'02_Simulation_Results'
    # Local reuse of scattering(), whose legacy ORIG constant is relative to its study.
    dirs=[orig/'CST_Raw',OLD/'06_Working/GroundControl',BASE,folder];pats=[orig,dirs[1],oldpattern,folder];names=['Original single','Larger ground single','Previous array','Final array'];ff=[freq(BASE),freq(folder)]
    write(R/'Final_Frequency_Monitors.csv',ff[-1])
    f,g,z0,z,g50=scattering(folder);write(R/'Final_S11.csv',[dict(GHz=x,native_real=y.real,native_imag=y.imag,reference_ohm=zv,S11_50_dB=20*np.log10(abs(gg))) for x,y,zv,gg in zip(f,g,z0,g50)])
    touch=np.loadtxt([l for l in next(folder.glob('CST_50ohm*.s1p')).read_text().splitlines() if l.strip() and l.lstrip()[0] not in '!#']);assert np.allclose(f,touch[:,0],atol=.0001)
    err=float(max(abs(g50-touch[:,1]-1j*touch[:,2])));assert err<1e-5
    fig,ax=plt.subplots(figsize=(8,4.5))
    for path,lab in zip(dirs,names):
        x,_,_,_,gg=scattering(path);ax.plot(x,20*np.log10(abs(gg)),label=lab)
    ax.axhline(-10,ls=':',color='#777');ax.set(xlabel='Frequency (GHz)',ylabel='S11 at 50 Ω (dB)');ax.legend();ax.grid(alpha=.2);save(fig,'S11_Comparison')
    for key,title in [('D','Directivity'),('G50','Realized_Gain')]:
        fig,ax=plt.subplots(figsize=(8,4.4))
        for series,lab in zip(ff,names[-2:]):ax.plot([v['GHz'] for v in series],[v[key] for v in series],'.-',label=lab)
        ax.set(xlabel='CST monitor frequency (GHz)',ylabel=title.replace('_',' ')+' (dBi)');ax.legend();ax.grid(alpha=.2);save(fig,title+'_Comparison')
    for plane in ['E','H']:
        fig,ax=plt.subplots(figsize=(8,4.5))
        for path,lab in zip(pats,names):
            tt,ds=sphere(path)[1][plane];ax.plot(tt,ds,label=lab)
        tt,ds=sphere(folder)[1][plane];write(R/(plane+'_Plane.csv'),[dict(deg=x,D_dBi=y,relative_dB=y-max(ds)) for x,y in zip(tt,ds)]);ax.set(xlabel='Signed angle from +z (deg)',ylabel='Directivity (dBi)',ylim=(-30,12),xlim=(-180,180));ax.legend(fontsize=8);ax.grid(alpha=.2);save(fig,plane+'_Plane_Comparison')
    j=np.loadtxt(folder/'Surface_Current_150.txt',skiprows=2);mask=abs(j[:,2]-final['substrate_h']-final['metal_thickness'])<.0001;j=j[mask];mag=np.sqrt((j[:,3:9]**2).sum(axis=1));assert len(j)>100
    fig,ax=plt.subplots(figsize=(7,4.5));sc=ax.scatter(j[:,0],j[:,1],c=mag,vmin=0,vmax=np.percentile(mag,98),s=3,cmap='viridis');fig.colorbar(sc,ax=ax,extend='max',label='|K| (A/m)');ax.set(xlabel='x (mm)',ylabel='y (mm)',title='150 GHz current on top gold');ax.set_aspect('equal');save(fig,'Surface_Current')
    shutil.copy2(folder/'Farfield_150_CST.png',R/'Final_3D_Farfield.png')
    br=field_rows(folder);write(R/'Final_Branch_Balance.csv',br);ab=max(abs(v['right_minus_left_dB']) for v in br);ph=max(abs(v['right_minus_left_deg']) for v in br)
    proxies=[]
    for fld in [D/'A_Gold_PI',*T.iterdir()]:
        if not (fld/'Edge_Field_150.txt').is_file():continue
        a=np.loadtxt(fld/'Edge_Field_150.txt',skiprows=2);q=np.loadtxt(fld/'Farfield_150_Sphere.txt',skiprows=2);x=q[:,0];w=10**(q[:,2]/10)*np.sin(np.deg2rad(x));proxies.append(dict(case=fld.name,h_mm=dct[fld.name]['substrate_h'],edge_Ez_RMS_Vm_per_sqrtW=np.sqrt(np.mean(a[:,7]**2+a[:,8]**2)/dct[fld.name]['Pacc']),near_horizon_radiated_fraction_70_to_110_deg=float(w[(x>=70)&(x<=110)].sum()/w.sum()),theta_deg=dct[fld.name]['theta_deg']))
    write(R/'Substrate_Edge_Diagnostics.csv',proxies)
    dump(R/'Validation.json',dict(touchstone_max_complex_error=err,max_branch_amplitude_difference_dB=ab,max_branch_phase_difference_deg=ph,sphere_mean=final['sphere_mean'],residual_pct=final['residual_pct'],solver=verification['solver'],original_saved_efficiency=baseline['eta'],skin_depth_um=1e6*math.sqrt(1/(math.pi*150e9*4*math.pi*1e-7*4.561e7))))
if __name__=='__main__':main()
