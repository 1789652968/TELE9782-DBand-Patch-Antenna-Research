"""Audit, comparison tables and engineering plots. Re-run safely after additional solves."""
from Round2_Analysis import *
import shutil, cmath, collections
V=ROOT/'07_Final_Candidates';A=ROOT/'06_Advanced_Candidates'
def ref_record(folder,name):
    ff=next(q for q in read(folder/'summary.json')['farfields'] if q['f_GHz']==150)
    f,_,ref,z,g=scattering(folder);i=np.argmin(abs(f-150));assert abs(f[i]-150)<.0001
    eta=100*10**(ff['rad_eff_dB']/10);et=eta*(1-abs(g[i])**2)
    sp,_=sphere(folder)
    return dict(name=name,solver=read(folder/'summary.json')['solver']['state'],eta=eta,eta_total50=et,S11_50=20*np.log10(abs(g[i])),D=ff['Dmax_dBi'],G50=ff['Dmax_dBi']+10*np.log10(et/100),D0=sp['D_broadside_dBi'],G0=sp['D_broadside_dBi']+10*np.log10(et/100),theta=sp['theta_deg'],phi=sp['phi_deg'],sphere_mean=sp['sphere_mean'],path=str(folder))
def table(rows,columns,headers):
    def fmt(v):
        if v is None:return '—'
        if isinstance(v,(float,np.floating)):return f'{v:.3f}'
        return str(v).replace('|','/')
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(columns))+' |']+['| '+' | '.join(fmt(q.get(k)) for k in columns)+' |' for q in rows])
def feasible(q):return q.get('solver')=='SUCCESS' and q['D']>=6.5 and q['S11_50']<=-10 and abs(q['residual_pct'])<=2 and abs(q['sphere_mean']-1)<.02
def score(v):
    axes=[('eta',90,6,3),('eta_total50',88,7,1),('G0',8,.6,2),('G50',8.5,.6,1),('D',9,1,.5),('bandwidth50',13.5,4,1)]
    return sum(w*max(0,(goal-v[k])/s) for k,goal,s,w in axes)+2.5*max(0,(v['theta']-5)/12)+.6*max(0,(v['S11_50']+17)/7)
def vector(q):return np.array([q[k] for k in ['eta','eta_total50','D','G50','G0','bandwidth50']]+[-q['theta'],-q['S11_50']])
def pareto(q,peers):
    a=vector(q);return not any(np.all(vector(other)>=a) and np.any(vector(other)>a) for other in peers)
def all_trials():
    rows=[]
    for path in sorted(ROOT.glob('0[3-7]_*/**/round2.json')):
        q=read(path);c=read(path.parent/'parameters.json');q['cells']=cells(path.parent);q['project']=str(path.parent/(path.parent.name+'.cst'));q['feasible']=feasible(q);q['balanced_gap_score']=score(q)
        q.update(c);rows.append(q)
    sc=[q for q in rows if q['mode']=='screen' and q['feasible']]
    for q in rows:
        q['pareto_same_screen_grid']=pareto(q,sc) if q in sc else None
        q['note']=('Hard/quality gate failed' if not q['feasible'] else ('Nondominated in tested screen set' if q['pareto_same_screen_grid'] else 'Dominated in tested screen set') if q['mode']=='screen' else q['mode'])
    failed=[]
    for path in ROOT.glob('0[3-7]_*/**/error.json'):
        known=next((v for v in rows if v['path']==str(path.parent)),None)
        if known is not None:
            known['recovered_error']=read(path)['error'];known['recovered_error_file']=str(path)
        else:
            status=read(path.parent/'summary.json')['solver']['state'] if (path.parent/'summary.json').exists() else 'UNVERIFIED'
            failed.append(dict(name=path.parent.name,solver=status,path=str(path.parent),note=read(path)['error']))
    write(R/'All_Optimisation_Trials.csv',rows+failed)
    write(R/'Screen_Pareto.csv',[q for q in sc if q['pareto_same_screen_grid']])
    return rows
def figures(rows,compare,sel_roots,vset):
    historical=['Original single','Previous array','Round 1']
    labelmap={q['path']:q['name'] for q in compare[:3]}
    for role,target in sel_roots.items():
        shortening={'Highest_Efficiency':'Highest η','Best_Balanced':'Balanced','Best_Broadside':'Broadside'}
        labelmap[target]=labelmap.get(target,'')+(' / ' if target in labelmap else '')+shortening[role]
    unique={q['path']:q for q in compare};chart=list(unique.values())
    labels=[labelmap[q['path']] for q in chart]
    for fld,unit,title in [('eta','%','Radiation_Efficiency'),('eta_total50','%','Total_Efficiency_50ohm'),('S11_50','dB','S11_150GHz'),('D','dBi','Peak_Directivity'),('G50','dBi','Peak_Realized_Gain'),('G0','dBi','Broadside_Realized_Gain'),('theta','degrees','Beam_Offset')]:
        fig,ax=plt.subplots(figsize=(9,4.6));v=[q[fld] for q in chart];bars=ax.bar(range(len(v)),v,color=['#697b88']*3+['#087f72']*(len(v)-3));ax.set_xticks(range(len(v)),labels,rotation=12,ha='right');ax.bar_label(bars,fmt='%.2f',padding=3);ax.margins(y=.15);ax.set_ylabel(unit);ax.set_title(title.replace('_',' ')+' at 150 GHz');ax.grid(axis='y',alpha=.15);save(title)
    physical=[q for q in chart if 'Pacc' in q]
    plt.figure(figsize=(9,4.6));bottom=np.zeros(len(physical))
    for key,label in [('Prad','Radiated'),('Pmetal','Gold'),('Pdiel','Polyimide'),('Pport','Port absorption'),('residual_pct','Residual')]:
        vals=np.array([q[key] if key=='residual_pct' else 100*q[key]/q['Pacc'] for q in physical]);plt.bar(range(len(vals)),vals,bottom=bottom,label=label);bottom+=vals
    plt.xticks(range(len(physical)),[labelmap[q['path']] for q in physical],rotation=10,ha='right');plt.ylabel('% of accepted power');plt.legend(loc='center left',bbox_to_anchor=(1,0.5));save('Power_Breakdown')
    eligible=[q for q in rows if q['mode']=='screen' and q['feasible']];plt.figure(figsize=(8,5))
    if eligible:
        p=plt.scatter([q['theta'] for q in eligible],[q['eta'] for q in eligible],c=[q['G0'] for q in eligible],cmap='viridis',s=60);plt.colorbar(p,label='+Z gain at 50 Ω (dBi)')
    front=[q for q in eligible if q['pareto_same_screen_grid']]
    if front:plt.scatter([q['theta'] for q in front],[q['eta'] for q in front],s=90,facecolors='none',edgecolors='#20262b',linewidths=.85,label='Screen: nondominated across 8 objectives')
    for q in [v['fresh'] for v in vset.values()]:plt.scatter(q['theta'],q['eta'],s=130,marker='*',label=q['name'])
    plt.axvline(5,color='.65',ls=':');plt.axhline(90,color='.65',ls=':');plt.xlabel('Beam offset (degrees)');plt.ylabel('Radiation efficiency (%)');plt.title('Matched coarse candidates and delivery re-solves');plt.legend(fontsize=8);save('Pareto_Tradeoff')
    fig,axes=plt.subplots(1,3,figsize=(12,4))
    for n,t in vset.items():
        reg=[t[k] for k in ['screen','production','dense','fresh']]
        for ax,k in zip(axes,['eta','theta','G0']):ax.plot(range(4),[q[k] for q in reg],marker='o',label=n)
    for ax,label in zip(axes,['Radiation efficiency (%)','Beam offset (degrees)','+Z gain (dBi)']):ax.set_xticks(range(4),['Screen','Prod.','Dense','Reopen'],rotation=22);ax.set_ylabel(label);ax.grid(alpha=.2)
    axes[0].legend(fontsize=7);save('Mesh_Convergence')
    folders=[('Round 1',BASE)]+[(labelmap[path],Path(path)) for path in dict.fromkeys(sel_roots.values())];line_fig(folders)
    for _,folder in folders[1:]:
        shutil.copyfile(folder/'Farfield_150_CST.png',R/('3D_Farfield_'+folder.name+'.png'));shutil.copyfile(folder/'Geometry.png',R/('Geometry_'+folder.name+'.png'));current_plot(folder)
def freq_rows(folder):
    q=read(folder/'round2.json');f,g,zref,z,g50=scattering(folder);out=[];r=read(folder/'summary.json')
    assert np.max(abs(zref-zref[0]))<.001
    for ff in sorted(r['farfields'],key=lambda x:x['f_GHz']):
        k=ff['f_GHz'];i=np.argmin(abs(f-k));assert abs(f[i]-k)<.0001
        eta=10**(ff['rad_eff_dB']/10);et=eta*(1-abs(g50[i])**2)
        d=dict(name=q['name'],frequency_GHz=k,S11_50=20*np.log10(abs(g50[i])),D=ff['Dmax_dBi'],eta_pct=100*eta,total50_pct=100*et,Gpeak50=ff['Dmax_dBi']+10*np.log10(et))
        path=folder/f'Farfield_{k:g}_Sphere.txt'
        if path.exists():
            arr=np.loadtxt(path,skiprows=2);imax=arr[:,2].argmax();d.update(theta=arr[imax,0],phi=arr[imax,1],D0=arr[0,2],G0=arr[0,2]+10*np.log10(et))
        out.append(d)
    return out
def final_audit(folder):
    q=read(folder/'round2.json');c=read(folder/'parameters.json');sp,curves=sphere(folder);r,b,ez,_=audit(folder);write(folder/'Current_Regions.csv',r);write(folder/'Paired_Ky.csv',b);write(folder/'Paired_Ez.csv',ez)
    for name,(ang,d) in curves.items():write(folder/(name+'_plane_150.csv'),[dict(signed_angle_deg=t,directivity_dBi=v,gain50_dBi=v+10*np.log10(q['eta_total50']/100)) for t,v in zip(ang,d)])
    native=np.loadtxt(folder/'RealizedGain_Native_150_Sphere.txt',skiprows=2);direction=np.loadtxt(folder/'Farfield_150_Sphere.txt',skiprows=2);assert np.all(native[:,:2]==direction[:,:2])
    ntop=native[native[:,2].argmax()];ff=next(v for v in read(folder/'summary.json')['farfields'] if v['f_GHz']==150);f,_,ref,_,g50=scattering(folder)
    assert np.max(abs(ref-ref[0]))<.001
    g0=ff['realized_gain_dBi']-q['G50'];k=np.argmin(abs(f-150))
    touch=next(folder.glob('*.s1p'));data=np.loadtxt((s for s in touch.read_text().splitlines() if s.strip() and not s.lstrip().startswith(('!','#'))))
    assert len(data)==len(f)
    touchmax=np.max(abs((data[:,1]+1j*data[:,2])-g50))
    mdir=next(folder.glob('*/Model/3D/ModelHistory.json'));history=mdir.read_text();code='\n'.join('\n'.join(rec['code']) for rec in json.loads(history)['history'])
    logpath=next(folder.glob('*/Result/Model.log'));log=logpath.read_text(errors='replace')
    checks={p:p in code for p in ['.Sigma "4.561e+007"','.TanD "loss_tangent"','.NumberOfModes "1"','.Orientation "ymin"','.CalculationType "TD-S"', '.MeshType "PBA"','Solid.Add "antenna:trunk", "antenna:patchleft"','Solid.Add "antenna:trunk", "antenna:patchright"']}
    boundary={}
    for axis in ['Xmin','Xmax','Ymin','Ymax','Zmin','Zmax']:
        vals=re.findall(r'\.'+axis+r'\s+"([^"]+)"',code)
        assert vals
        boundary[axis]=vals[-1]
    assert boundary=={k:('open' if k=='Ymin' else 'expanded open') for k in boundary}
    for spec in ['.ReferencePlaneDistance "0"','.PortOnBound "True"','.FrequencyForMinimumDistance "130"', '.MinimumDistancePerWavelengthNewMeshEngine "4"']:
        checks[spec]=spec in code
    assert np.max(abs(data[:,0]-f))<.00005
    mask=direction[:,2]>-35
    native_offset=10*np.log10(10**(ff['total_eff_dB']/10))
    angular_delta=float(np.max(abs((native[mask,2]-direction[mask,2])-native_offset)))
    assert angular_delta<.025,angular_delta
    warnings=[s.strip() for s in log.splitlines() if 'constant approximation' in s.lower() or 'port meshing' in s.lower() or 'steady state energy' in s.lower()][-8:]
    closure=q['Pacc']-q['Prad']-q['Pmetal']-q['Pdiel']-q['Pport'];err=100*q['Prad']/q['Pacc']-q['eta_farfield']
    native_gamma=(complex(q['Rin'],q['Xin'])-q['Zref'])/(complex(q['Rin'],q['Xin'])+q['Zref'])
    accepted_closure=q['Pin']-q['Pout']-q['Pacc']
    reflected_power_identity=q['Pout']/q['Pin']-abs(native_gamma)**2
    assert abs(accepted_closure)/q['Pin']<.0001 and abs(reflected_power_identity)<.0001
    out=dict(stimulated_minus_outgoing_minus_accepted_W=accepted_closure,outgoing_fraction_minus_native_reflection=reflected_power_identity,final_boundary=boundary,reference_plane_distance_mm=0,maximum_native_gain_identity_residual_dB=angular_delta,native_gain_theta=ntop[0],native_gain_phi=ntop[1],native_peak_gain=float(ntop[2]),native_minus_50ohm_peak_dB=g0,touchstone_max_gamma_difference=float(touchmax),cells=cells(folder),closure_W=closure,eta_power_minus_farfield_pp=err,maximum_Ez_phase_diff_deg=max(abs(x['right_minus_left_deg']) for x in ez),maximum_Ez_amp_diff_dB=max(abs(x['right_minus_left_dB']) for x in ez),model_checks=checks,solver_log_evidence=warnings,**sp)
    assert touchmax<.0001 and abs(err)<.1 and abs(sp['sphere_mean']-1)<.02 and all(checks.values())
    (folder/'Independent_Audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    return out


if __name__=='__main__':
    import subprocess
    from Round2_Delivery import main
    if (V/'Final_Selection.json').exists():
        subprocess.run([str(ROOT.parents[1]/'CST Studio Suite 2024/Opera/code/bin/python.exe'),'-u',str(Path(__file__).with_name('Round2_Targeted.py'))],check=True)
        subprocess.run([str(ROOT.parents[1]/'CST Studio Suite 2024/Opera/code/bin/python.exe'),'-u',str(Path(__file__).with_name('Round2_Port.py'))],check=True)
        subprocess.run([str(ROOT.parents[1]/'CST Studio Suite 2024/Opera/code/bin/python.exe'),'-u',str(Path(__file__).with_name('Round2_Fields.py'))],check=True)
    main()
