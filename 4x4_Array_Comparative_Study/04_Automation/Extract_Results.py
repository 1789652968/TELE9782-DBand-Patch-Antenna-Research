"""Use actual CST exports to calculate the common-50-ohm comparison and figures."""
from pathlib import Path
import argparse, csv, json, math, re, os
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
path_from_project='08_Efficiency_Optimisation/06_Final_Candidate/TELE9782_DBand_Efficiency_Final'
BASE=Path(os.environ['TELE9782_BASELINE_DIR']) if 'TELE9782_BASELINE_DIR' in os.environ else ROOT.parent/path_from_project
if not (BASE/'parameters.json').exists():BASE=ROOT.parent/'Project_Final'/path_from_project
COMP=ROOT/'03_Comparison'
RESULTS=ROOT/'02_Simulation_Results'
def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def raw(folder,name):
    with (folder/(name+'.csv')).open(newline='',encoding='utf-8-sig') as f:
        a=list(csv.DictReader(f))
    return np.array([float(row['x']) for row in a]),np.array([complex(float(row['real']),float(row['imag'])) for row in a])
def write(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        if rows:
            w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
def write_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding='utf-8')
def pattern(folder,filename='Farfield_150_Sphere.txt'):
    a=np.loadtxt(folder/filename,skiprows=2)
    t=np.unique(a[:,0]);p=np.unique(a[:,1]);a=a[np.lexsort((a[:,0],a[:,1]))]
    assert len(a)==len(p)*len(t) and t[0]==0 and t[-1]==180
    d=a[:,2].reshape(len(p),len(t))
    return a,t,p,d
def cut(t,p,d,phi):
    first=d[np.where(p==phi)[0][0]]
    other=d[np.where(p==phi+180)[0][0]]
    x=np.r_[-t[:0:-1],t];y=np.r_[other[:0:-1],first]
    peak=np.argmax(np.where(abs(x)<=90,y,-np.inf));level=y[peak]-3
    dx=[]
    for sign in [-1,1]:
        i=peak
        while 0<=i+sign<len(x) and y[i+sign]>=level:i+=sign
        j=i+sign
        if not 0<=j<len(x):return x,y,None
        dx.append(x[i]+(level-y[i])*(x[j]-x[i])/(y[j]-y[i]))
    return x,y,float(dx[1]-dx[0])
def bandwidth(f,y):
    right=np.flatnonzero(f>=150)[0];inside=y<=-10
    if not inside[right]:return 0.,None,None
    lo=right;hi=right
    while lo>0 and inside[lo-1]:lo-=1
    while hi+1<len(f) and inside[hi+1]:hi+=1
    def cross(j,k):return float(f[j]+(-10-y[j])*(f[k]-f[j])/(y[k]-y[j]))
    a=float(f[0]) if lo==0 else cross(lo-1,lo)
    b=float(f[-1]) if hi==len(f)-1 else cross(hi,hi+1)
    return b-a,a,b
def observations(folder):
    dct=read(folder/'summary.json');c=read(folder/'parameters.json')
    monitor=next(x for x in dct['farfields'] if x['f_GHz']==150)
    f,g=raw(folder,'1D Results_S-Parameters_S1,1')
    fr,zr=raw(folder,'1D Results_Reference Impedance_ZRef 1(1)')
    z0=np.interp(f,fr,zr.real)
    z=z0*(1+g)/(1-g);g50=(z-50)/(z+50)
    k=int(np.argmin(abs(f-150)));assert abs(f[k]-150)<.0001
    db=20*np.log10(abs(g50));bw,flo,fhi=bandwidth(f,db)
    def p(term):
        x,y=raw(folder,'1D Results_Power_Excitation [1]_'+term);i=int(np.argmin(abs(x-150)))
        assert abs(x[i]-150)<2e-5,term
        return float(y[i].real)
    accepted=p('Power Accepted'); radiated=p('Power Radiated');gold=p('Loss in Metals');pi=p('Loss in Dielectrics')
    port=p('Power Absorbed at all Ports');pout=p('Power Outgoing all Ports');stim=p('Power Stimulated')
    rad=radiated/accepted;total=rad*(1-abs(g50[k])**2)
    grid,t,phi,d=pattern(folder)
    peak=grid[grid[:,2].argmax()]
    eang,ep,eh=cut(t,phi,d,90);hang,hp,hh=cut(t,phi,d,0)
    broad=float(d[0,0]);gain_ratio=10*math.log10(total);dmax=monitor['Dmax_dBi']
    sphere_rows=grid[grid[:,1]<360];sphere_integral=float(np.sum(10**(sphere_rows[:,2]/10)*np.sin(np.radians(sphere_rows[:,0])))*math.radians(t[1]-t[0])*math.radians(phi[1]-phi[0])/(4*np.pi))
    filename=next(folder.glob('*.cst'))
    log=(filename.with_suffix('')/'Result/Model.log').read_text(errors='replace')
    cells=re.findall(r'Number of mesh cells:\s*([\d,]+)',log)
    calc=re.findall(r'Total simulation time:\s*([\d,.]+)',log)
    completed=re.findall(r'(\d{4}-\d{2}-\d{2} \d\d:\d\d:\d\d)\s+Steady state energy criterion met',log)
    ver=read(folder/'Export_Complete.json') if (folder/'Export_Complete.json').is_file() else {}
    geometry=read(folder/'layout.json') if (folder/'layout.json').is_file() else {}
    res= dict(design=folder.name,frequency_GHz=150,patch_count=16 if geometry else 2,
        radiation_efficiency_pct=100*rad,total_efficiency_50ohm_pct=100*total,
        s11_50ohm_dB=float(db[k]),input_r_ohm=float(z[k].real),input_x_ohm=float(z[k].imag),modal_reference_ohm=float(z0[k]),
        directivity_dBi=dmax,peak_realized_gain_50ohm_dBi=dmax+gain_ratio,
        plus_z_directivity_dBi=broad,plus_z_realized_gain_50ohm_dBi=broad+gain_ratio,
        beam_theta_deg=float(peak[0]),beam_phi_deg=float(peak[1]),angular_step_deg=float(t[1]-t[0]),
        e_plane_hpbw_deg=eh,h_plane_hpbw_deg=hh,bandwidth_10dB_GHz=bw,band_lower_GHz=flo,band_upper_GHz=fhi,
        best_match_freq_GHz=float(f[np.argmin(db)]),best_s11_50ohm_dB=float(np.min(db)),
        stimulated_W=stim,accepted_W=accepted,radiated_W=radiated,metal_loss_W=gold,dielectric_loss_W=pi,port_absorption_W=port,
        balance_residual_W=accepted-radiated-gold-pi-port,
        metal_loss_pct_accepted=gold/accepted*100,dielectric_loss_pct_accepted=pi/accepted*100,
        port_absorption_pct_accepted=port/accepted*100,balance_residual_pct_accepted=(accepted-radiated-gold-pi-port)/accepted*100,
        accepted_identity_residual_W=stim-pout-accepted,
        directivity_sphere_mean=sphere_integral,radiation_efficiency_minus_monitor_pp=100*(rad-10**(monitor['rad_eff_dB']/10)),
        board_width_mm=geometry.get('board_width_mm',c.get('ground_width')),board_length_mm=geometry.get('board_length_mm',c.get('ground_length')),
        T_junctions=geometry.get('junctions',1),feed_total_centerline_mm=geometry.get('network_total_centerline_mm'),
        port_to_inset_centerline_mm=geometry.get('equal_path_to_inset_mm'),
        mesh_cells=int(cells[-1].replace(',','')) if cells else None,steps_per_wave_near=c['mesh_near'],
        steps_per_box_near=c['mesh_box'],solver_state=dct['solver']['state'],solver_log_completion=completed[-1] if completed else None,
        reported_solver_calculation_seconds=float(calc[-1].replace(',','')) if calc else None,run_plus_export_wall_seconds=ver.get('wall_seconds') if ver.get('wall_scope')!='export_only' else None,
        recovered_export_wall_seconds=ver.get('wall_seconds') if ver.get('wall_scope')=='export_only' else None,
        native_project=str(filename))
    if not geometry:
        inlet=c['junction_y']+c['ground_length']/2+c['launch_length']
        leaf=c['array_spacing']/2-c['patch_length']/2+c['inset_length']-c['junction_y']
        res.update(feed_total_centerline_mm=inlet+2*leaf,port_to_inset_centerline_mm=inlet+leaf)
    path=folder/'CST_50ohm.s1p'
    if path.is_file():
        rows=np.array([list(map(float,s.split())) for s in path.read_text().splitlines() if s.strip() and not s.lstrip().startswith(('!','#'))])
        assert len(rows)==len(f) and np.max(abs(rows[:,0]-f))<.00005
        res['touchstone_max_complex_delta']=float(np.max(abs(g50-(rows[:,1]+1j*rows[:,2]))))
        assert res['touchstone_max_complex_delta']<.0001
    else:res['touchstone_max_complex_delta']=None
    rn=folder/'RealizedGain_Native_150_Sphere.txt'
    if rn.is_file():
        n,*_=pattern(folder,rn.name);assert np.array_equal(n[:,:2],grid[:,:2])
        delta=10*math.log10(abs(1-abs(g50[k])**2)/(1-abs(g[k])**2))
        res['native_gain_renormalized_peak_dBi']=float(n[:,2].max()+delta)
        res['native_gain_peak_delta_dB']=res['native_gain_renormalized_peak_dBi']-res['peak_realized_gain_50ohm_dBi']
        assert abs(res['native_gain_peak_delta_dB'])<.05
    else:res.update(native_gain_renormalized_peak_dBi=None,native_gain_peak_delta_dB=None)
    res['maximum_port_extension_mm']=geometry['board_x'][0]-geometry['port_x'] if geometry else c['launch_length']
    res['bounding_width_mm']=res['board_width_mm']+(res['maximum_port_extension_mm'] if geometry else 0)
    res['bounding_length_mm']=res['board_length_mm']+(0 if geometry else c['launch_length'])
    return res,(f,db),(eang,ep),(hang,hp),grid
def volts(folder):
    file=folder/'Patch_Feed_Ez150.txt'
    if not file.is_file():return [],{}
    a=np.loadtxt(file,skiprows=2);l=read(folder/'layout.json');assert len(a)==len(l['patches'])==16
    u=a[:,7]+1j*a[:,8];u0=np.angle(np.mean(u/abs(u)))
    rows=[]
    for i,x in enumerate(a):
        p=l['patches'][i];assert abs(x[0]-p['x'])<1e-7 and abs(x[1]-p['probe_y'])<1e-7
        rows.append(dict(patch=p['name'],x_mm=x[0],y_mm=x[1],z_mm=x[2],Ez_re_Vm=x[7],Ez_im_Vm=x[8],Ez_abs_Vm=abs(u[i]),Ez_phase_about_circular_mean_deg=np.degrees(np.angle(u[i]*np.exp(-1j*u0)))))
    return rows,dict(connected_patch_probes=len(rows),minimum_Ez_Vm=float(min(abs(u))),maximum_Ez_Vm=float(max(abs(u))),
            magnitude_spread_dB=float(20*np.log10(max(abs(u))/min(abs(u)))),maximum_abs_relative_phase_deg=float(max(abs(x['Ez_phase_about_circular_mean_deg']) for x in rows)))
def initial_report():
    r,*_=observations(BASE);s=read(BASE/'completed.json')
    for col,key in [('radiation_efficiency_pct','eta'),('s11_50ohm_dB','S11_50'),('peak_realized_gain_50ohm_dBi','G50'),('bandwidth_10dB_GHz','bandwidth50')]:
        assert math.isclose(r[col],s[key],abs_tol=1e-9)
    write_json(RESULTS/'Verification/Baseline_1x2_Independent_Recalculation.json',r)
def figures(values,folder):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    out=COMP/'Comparison_Figures';out.mkdir(parents=True,exist_ok=True)
    def save(f,name):
        f.tight_layout();f.savefig(out/(name+'.png'),dpi=180,bbox_inches='tight');plt.close(f)
    names=['Optimised 1×2','Basic 4×4']
    fig,ax=plt.subplots(figsize=(7.8,4.5))
    for label,(_,v,*_) in zip(names,values):ax.plot(*v,label=label)
    ax.axhline(-10,color='gray',ls='--');ax.axvline(150,color='gray',alpha=.6,ls=':')
    ax.set(xlabel='Frequency (GHz)',ylabel='S11 re-referenced to 50 Ω (dB)');ax.grid(alpha=.2);ax.legend()
    save(fig,'S11_50ohm')
    fig,axes=plt.subplots(1,2,figsize=(11,4.5),sharey=True)
    for label,(metrics,_,e,h,_) in zip(names,values):
        for name,ax,cutval in zip(['E plane (YZ)','H plane (XZ)'],axes,[e,h]):
            ax.plot(*cutval,label=label);ax.set(title=name,xlabel='Signed θ (degrees)',xlim=(-90,90));ax.grid(alpha=.2);ax.legend()
    axes[0].set_ylabel('Directivity (dBi)');save(fig,'E_H_Planes')
    labels=['Radiated','Metal loss','Dielectric loss','Port absorption','Residual']
    power=['radiated_W','metal_loss_W','dielectric_loss_W','port_absorption_W','balance_residual_W']
    fig,axes=plt.subplots(1,2,figsize=(10,5))
    for normalized,ax in zip([False,True],axes):
        pos=np.arange(len(labels))
        for j,(q,*_) in enumerate(values):
            vals=[q[k]*(100/q['accepted_W'] if normalized else 1000) for k in power];ax.bar(pos+(j-.5)*.34,vals,width=.34,label=names[j])
        ax.set_xticks(pos,labels,rotation=22,ha='right');ax.set_ylabel('Share of accepted power (%)' if normalized else 'CST power (mW)');ax.legend();ax.grid(axis='y',alpha=.2)
    save(fig,'Power_Absolute_and_Normalized')
    fig,ax=plt.subplots(subplot_kw={'projection':'3d'},figsize=(7,6))
    grid,t,p,d=pattern(folder)
    pp,tt=np.meshgrid(np.radians(np.r_[p,p[0]+360]),np.radians(t),indexing='ij')
    val=np.vstack([d,d[0]]);radius=np.clip((val+10)/max(1,val.max()+10),0,1)
    ax.plot_surface(radius*np.sin(tt)*np.cos(pp),radius*np.sin(tt)*np.sin(pp),radius*np.cos(tt),
                    facecolors=plt.cm.viridis(radius),edgecolor='none',rstride=3,cstride=3)
    ax.set(xlabel='X',ylabel='Y',zlabel='Z',title='4×4 CST directivity at 150 GHz')
    ax.set_box_aspect((1,1,1));fig.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(-10,val.max()),cmap='viridis'),ax=ax,label='Directivity (dBi)')
    save(fig,'4x4_3D_Directivity')
    fig,ax=plt.subplots(subplot_kw={'projection':'3d'},figsize=(7,6))
    ratio=10*np.log10(values[1][0]['total_efficiency_50ohm_pct']/100)
    gain=val+ratio;radius=np.clip((gain+15)/max(1,gain.max()+15),0,1)
    ax.plot_surface(radius*np.sin(tt)*np.cos(pp),radius*np.sin(tt)*np.sin(pp),radius*np.cos(tt),
                    facecolors=plt.cm.plasma(radius),edgecolor='none',rstride=3,cstride=3)
    ax.set(xlabel='X',ylabel='Y',zlabel='Z',title='4×4 realized gain at 150 GHz, 50 Ω')
    ax.set_box_aspect((1,1,1));fig.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(-15,gain.max()),cmap='plasma'),ax=ax,label='Realized gain (dBi)')
    save(fig,'4x4_3D_Realized_Gain_50ohm')
    current=folder/'Surface_Current_150.txt'
    if current.is_file():
        s=np.loadtxt(current,skiprows=2);h=read(folder/'parameters.json')['substrate_h']
        s=s[(s[:,2]>h*.75)&(np.linalg.norm(s[:,3:9],axis=1)>0)]
        field=np.linalg.norm(s[:,3:9],axis=1)
        fig,ax=plt.subplots(figsize=(7,6));c=ax.scatter(s[:,0],s[:,1],c=field,s=3,cmap='inferno',vmax=np.percentile(field,99));ax.set(aspect='equal',xlabel='x (mm)',ylabel='y (mm)');fig.colorbar(c,ax=ax,label='CST surface-current magnitude (A/m), 99th percentile scale');save(fig,'4x4_Surface_Current_150')
def publish(folder):
    b=observations(BASE);q=observations(folder);r=q[0];m=b[0]
    assert r['solver_state']=='SUCCESS'
    probes,qual=volts(folder)
    cols=['s11_50ohm_dB','radiation_efficiency_pct','total_efficiency_50ohm_pct','directivity_dBi','peak_realized_gain_50ohm_dBi','plus_z_realized_gain_50ohm_dBi',
          'bandwidth_10dB_GHz','beam_theta_deg','metal_loss_pct_accepted','dielectric_loss_pct_accepted']
    change={k:r[k]-m[k] for k in cols}
    write(COMP/'Array_1x2_vs_4x4_Comparison.csv',[m,r]);write_json(RESULTS/'Verification/Final_Metrics.json',dict(baseline=m,array4x4=r,change=change,feed_probes=qual))
    write(RESULTS/'Farfield/Patch_Feed_Probes_150.csv',probes)
    for name,data in [('1x2',b),('4x4',q)]:
        v,f,e,h,grid=data
        write(RESULTS/f'S_Parameters/{name}_S11_50ohm.csv',[dict(frequency_GHz=x,S11_50ohm_dB=y) for x,y in zip(*f)])
        for plane,(ang,d) in [('E',e),('H',h)]:
            k=10*np.log10(v['total_efficiency_50ohm_pct']/100)
            write(RESULTS/f'Farfield/{name}_{plane}_plane_150.csv',[dict(theta_signed_deg=t,directivity_dBi=z,realized_gain_50ohm_dBi=z+k) for t,z in zip(ang,d)])
    write(RESULTS/'Power_Loss/Power_Balance_150.csv',[{k:v for k,v in row.items() if k=='design' or k.endswith(('_W','_accepted'))} for row in [m,r]])
    write(RESULTS/'Efficiency/Frequency_Monitors.csv',[{'design':tag,**mon} for tag,fo in [('1x2',BASE),('4x4',folder)] for mon in read(fo/'summary.json')['farfields']])
    figures([b,q],folder)
    print('FINAL_METRICS',r)
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('case',nargs='?',default='Final_4x4')
    parser.add_argument('--summary',action='store_true')
    parser.add_argument('--baseline',action='store_true')
    args=parser.parse_args()
    if args.baseline:initial_report()
    else:
        folder=ROOT/'01_CST_Project'/args.case
        if args.summary:print(json.dumps(observations(folder)[0],indent=2))
        else:publish(folder)

