"""Direct numerical audit and diagnostic plots from saved CST exports."""
from pathlib import Path
import numpy as np, csv, json, math, re, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from Array_Results_Extraction import sphere,field_rows,scattering,write
ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/'01_Baseline_Backup/TELE9782_DBand_Efficiency_Final'
R=ROOT/'08_Results_and_Figures'; DI=ROOT/'02_Diagnostics'; DOC=ROOT/'10_Documentation'
LEGACY=ROOT.parent/'07_Array_1x2'; LEGFIG=LEGACY/'02_Simulation_Results'
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def region_stats(folder,c):
    a=np.loadtxt(folder/'Surface_Current_150.txt',skiprows=2);x,y,z=a[:,:3].T
    y=y-c.get('shift_y',0);ky=a[:,5]+1j*a[:,6]; strength=np.sqrt(np.sum(a[:,3:9]**2,axis=1));w=a[:,9]
    d=c['array_spacing']/2;j=c['junction_y'];h=c['substrate_h'];l=c['patch_length'];fw=c['feed_width'];tw=c['transformer_width'];t=c['transformer_length']
    masks={'T junction':(abs(x)<=fw*.65)&(abs(y-j)<=tw*.7),'transformers':(abs(x)>fw*.65)&(abs(x)<t)&(abs(y-j)<tw*.49),'bends':(abs(abs(x)-d)<fw*.54)&(abs(y-j)<fw*.54),'inset contact':(abs(abs(x)-d)<fw*.7)&(abs(y-(-l/2+c['inset_length']))<.035),'patch +Y edge':(abs(abs(x)-d)<c['patch_width']/2)&(abs(y-l/2)<.045),'patch -Y edge':(abs(abs(x)-d)<c['patch_width']/2)&(abs(y+l/2)<.045)}
    rows=[];top=z>=h-1.e-6
    for name,mask in masks.items():
        ok=mask&top&(w>0)
        if ok.any():rows.append(dict(name=folder.name,region=name,facets=int(sum(ok)),area_mm2=sum(w[ok]),K_rms_Apm=np.sqrt(np.average(strength[ok]**2,weights=w[ok])),K_max_Apm=max(strength[ok]),K2_area_A2=np.sum(w[ok]*strength[ok]**2)*1.e-6))
    balance=[]
    for label,yy in [('post-bend',(j-l/2)/2),('inset entrance',-l/2+.025),('before inset contact',-l/2+c['inset_length']-.035)]:
        vals=[]
        for xpos in [-d,d]:
            use=top&(abs(x-xpos)<fw*.48)&(abs(y-yy)<.026)&(w>0)
            if use.any():vals.append(np.average(ky[use],weights=w[use]))
        if len(vals)==2 and all(abs(v)>1.e-9 for v in vals):
            ratio=vals[1]/vals[0];balance.append(dict(name=folder.name,region=label,y_mm=yy,Ky_left_Apm=abs(vals[0]),Ky_right_Apm=abs(vals[1]),difference_dB=20*np.log10(abs(ratio)),phase_deg=np.angle(ratio,deg=True)))
    return rows,balance
def cells(folder):
    logs=list(folder.glob('*/Result/Model.log'))
    if not logs:return None
    found=re.findall(r'Number of mesh cells:\s*([\d,]+)',logs[0].read_text(errors='replace'));return int(found[-1].replace(',','')) if found else None
def audit(folder):
    c=read(folder/'parameters.json');rr,bb=region_stats(folder,c);pairs=field_rows(folder)
    sp,_=sphere(folder);return rr,bb,pairs,sp
def baseline():
    r,b,e,sp=audit(BASE);write(DI/'Baseline_Current_Regions.csv',r);write(DI/'Baseline_Paired_Ky.csv',b);write(DI/'Baseline_Paired_Ez.csv',e)
    v=read(DI/'Baseline_Raw_Recalculation.json')
    (DOC/'Beam_Squint_Diagnosis.md').write_text(f"""# 150 GHz beam-squint diagnosis

The delivery archive and the round-two backup have identical SHA256. The audit uses the complete CST 2024 results, the native 2° theta/phi full-sphere export, and complex surface-current and electric-field exports. The two patch centers lie on X at ±0.560 mm. The waveguide port and common feed enter from −Y. Theta is measured from +Z; phi is measured from +X toward +Y.

| Quantity | Saved 82.99% delivery |
|---|---:|
| Native peak directivity | {v['D']:.4f} dBi |
| Sampled peak direction | theta {v['theta']:.0f}°, phi {v['phi']:.0f}°, in the YZ (E) plane |
| Directivity / realized gain (50 ohm) at +Z | {v['D0']:.3f} / {v['G0']:.3f} dBi |
| Peak realized gain (50 ohm) | {v['G50']:.3f} dBi |
| E/H half-power beamwidth | {sp['E_HPBW_deg']:.2f}° / {sp['H_HPBW_deg']:.2f}° |
| +/-Z axial front/back | {v['FBaxial']:.2f} dB |
| Directivity sphere integral / 4π | {v['sphere_mean']:.6f} |

At four mirrored feed locations the largest right/left Ez difference is {max(abs(u['right_minus_left_dB']) for u in e):.6f} dB and {max(abs(u['right_minus_left_deg']) for u in e):.6f}°. The area-weighted longitudinal current in {len(b)} mirrored feed windows differs by up to {max(abs(u['difference_dB']) for u in b):.4f} dB and {max(abs(u['phase_deg']) for u in b):.4f}°. The current windows combine sampled facets within each stated region, so the estimate depends on spatial sampling. These are local phasors; neither method separates forward and reflected waves. See the two paired CSVs in 02_Diagnostics.

The measured imbalance across X is too small to explain a 16° tilt along Y. The complete aperture includes the one-sided launch, divider, inset slots and fields scattered by the finite substrate and ground. Their Y asymmetry can change the E-plane phase distribution while preserving left/right symmetry. The pattern alone cannot uniquely allocate the tilt between them. Controlled geometric perturbations are tabulated separately at the same mesh setting.

The highest regional sampled RMS surface current is {max(r,key=lambda q:q['K_rms_Apm'])['region']} ({max(q['K_rms_Apm'] for q in r):.1f} A/m). Regions are diagnostic windows, may overlap, and do not partition metal loss. Compare the solver's integrated loss in metals between runs. The baseline allocates {100*v['Pmetal']/v['Pacc']:.2f}% of accepted power to gold, {100*v['Pdiel']/v['Pacc']:.2f}% to polyimide, {100*v['Pport']/v['Pacc']:.2f}% to port absorption and {v['residual_pct']:.3f}% to the remaining closure residual.
""",encoding='utf-8')
def save(name):
    plt.tight_layout();plt.savefig(R/(name+'.png'),dpi=160,bbox_inches='tight');plt.close()
def line_fig(folders):
    for label,sub in [('Radiation_Efficiency_vs_Frequency','rad'),('S11_50ohm_vs_Frequency','s11'),('E_plane','E'),('H_plane','H')]:
        plt.figure(figsize=(8.3,4.5))
        for nm,folder in folders:
            if sub=='rad':
                ff=sorted(read(folder/'summary.json')['farfields'],key=lambda q:q['f_GHz']);plt.scatter([q['f_GHz'] for q in ff],[100*10**(q['rad_eff_dB']/10) for q in ff],s=19,label=nm)
            elif sub=='s11':
                x,_,_,_,g=scattering(folder);plt.plot(x,20*np.log10(abs(g)),label=nm)
            else:
                _,curves=sphere(folder);x,y=curves[sub];plt.plot(x,y,label=nm)
        if sub=='s11':plt.axhline(-10,color='gray',ls=':');plt.ylim(-50,0)
        if sub in ('E','H'):plt.xlim(-180,180);plt.ylim(-24,12)
        plt.xlabel('Frequency (GHz)' if sub in ('rad','s11') else 'Signed angle from +Z (degrees)');plt.ylabel({'rad':'Radiation efficiency (%)','s11':'S11 at 50 Ω (dB)','E':'E-plane directivity (dBi)','H':'H-plane directivity (dBi)'}[sub]);plt.grid(alpha=.2);plt.legend();save(label)
def current_plot(folder):
    a=np.loadtxt(folder/'Surface_Current_150.txt',skiprows=2);h=read(folder/'parameters.json')['substrate_h'];a=a[a[:,2]>=h-1.e-6]
    k=np.sqrt((a[:,3:9]**2).sum(axis=1));plt.figure(figsize=(8,5));plt.scatter(a[:,0],a[:,1],c=k,s=4,cmap='inferno',vmin=0,vmax=np.percentile(k,99));plt.axis('equal');plt.colorbar(label='|K| (A/m), colour clipped at 99th percentile');plt.xlabel('X (mm)');plt.ylabel('Y (mm)');plt.title(folder.name+' • top gold, 150 GHz');save('Surface_Current_'+folder.name)
if __name__=='__main__':baseline()

