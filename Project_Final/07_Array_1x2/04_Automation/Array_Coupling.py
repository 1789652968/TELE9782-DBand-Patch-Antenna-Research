"""Quantify local fields/current across spacings from common 150 GHz CST monitor samples."""
from Array_Results_Extraction import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def run():
    selected=read(W/'selection.json');noms=[t[1] for t in selected['trials'] if t[2].get('array_spacing')==1]
    base=max((t for t in selected['trials'] if t[1] in noms),key=lambda t:t[0])[1]
    folders=[W/'Spacing90',W/base,W/'Spacing110',W/'Spacing120',W/'Spacing130',R];rows=[]
    for folder in folders:
        if folder==R:
            p=read(P/'parameters.json');metrics150=metrics(P,R)
        else:p=read(folder/'parameters.json');metrics150=metrics(folder)
        fld=field_rows(folder);j=np.loadtxt(folder/'Surface_Current_150.txt',skiprows=2)
        kvec=j[:,3:9:2]+1j*j[:,4:9:2];ksq=(abs(kvec)**2).sum(axis=1)
        t=p['substrate_h']+p['metal_thickness']
        # Top-surface area-weighted RMS of CST complex K in interior rectangles.
        def rms(center):
            mask=(abs(j[:,0]-center)<.20)&(abs(j[:,1])<.12)&(abs(j[:,2]-t)<.0001)&(j[:,9]>0)
            assert mask.any();return np.sqrt(np.average(ksq[mask],weights=j[mask,9]))
        row=dict(case=folder.name,spacing_mm=p['array_spacing'],mesh_near=p['mesh_near'],left_patch_Krms_A_per_m=rms(-p['array_spacing']/2),right_patch_Krms_A_per_m=rms(p['array_spacing']/2),max_local_abs_amplitude_delta_dB=max(abs(q['right_minus_left_dB']) for q in fld),max_local_abs_phase_delta_deg=max(abs(q['right_minus_left_deg']) for q in fld),mean_left_Ez_V_per_m=np.mean([q['left_Ez_V_per_m'] for q in fld]))
        row.update({k:metrics150[k] for k in ['Zre150_ohm','Zim150_ohm','fmin_GHz','S11_dB','Dmax_dBi','realized_gain_dBi','rad_eff_pct','E_HPBW_deg','H_HPBW_deg','theta_deg','phi_deg','H_other_forward_peak_relative_dB','E_other_forward_peak_relative_dB']});rows.append(row)
        if folder==R:
            fig,ax=plt.subplots(figsize=(8,4.8));mask=abs(j[:,2]-t)<.0001
            sc=ax.scatter(j[mask,0],j[mask,1],c=np.sqrt(ksq[mask]),s=4,marker='s',cmap='viridis',vmin=0,vmax=np.percentile(np.sqrt(ksq[mask]),98))
            cb=fig.colorbar(sc,ax=ax,extend='max');cb.set_label('Complex current magnitude (A/m)')
            ax.set_aspect('equal');ax.set(xlabel='x (mm)',ylabel='y (mm)',title='150 GHz • top gold surface • CST facet values');fig.tight_layout();fig.savefig(R/'Surface_Current_Map.png',dpi=180);plt.close(fig)
    write(C/'Spacing_Field_and_Pattern_Study.csv',rows)
if __name__=='__main__':run()
