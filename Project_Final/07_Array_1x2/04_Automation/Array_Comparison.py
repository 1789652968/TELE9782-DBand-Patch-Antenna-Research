"""Compare the reopened array against both single-element controls and plot source data."""
from Array_Results_Extraction import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def save(fig,name):
    fig.tight_layout();fig.savefig(C/(name+'.png'),dpi=175,bbox_inches='tight');plt.close(fig)
def run():
    folders=[ORIG,W/'GroundControl',P];labels=['Original single patch','Single on array ground','Corporate-fed array'];colors=['#456383','#a16129','#007b6e']
    met=[metrics(folder,R if folder==P else None) for folder in folders];rows=[];single,control,array=met
    comp=['f_GHz','Dmax_dBi','D_broadside_dBi','realized_gain_dBi','realized_broadside_dBi','S11_dB','S11_50_dB','realized_50_dBi','reference_ohm','Zre150_ohm','Zim150_ohm','fmin_GHz','minimum_S11_dB','f_low_GHz','f_high_GHz','BW_GHz','FBW_percent','rad_eff_pct','total_eff_pct','E_HPBW_deg','H_HPBW_deg','theta_deg','phi_deg','main_ground_mm2','with_launch_area_mm2','elements','feed_network']
    for v,area,n,feed in zip(met,[1.96,3.75,3.75],[1,1,2],['Straight inset','Straight inset','Symmetric T and two stepped branches']):
        v.update(main_ground_mm2=area,with_launch_area_mm2=area+.25,elements=n,feed_network=feed)
    for k in comp:
        a,b,c=[v[k] for v in met];numeric=isinstance(c,(int,float,np.floating));db=('dB' in k);pct='pct' in k or 'percent' in k
        delta=c-a if numeric else '';ratio=(100*(c-a)/abs(a) if numeric and a!=0 and not db and k not in ['theta_deg','phi_deg','Zim150_ohm','Zre150_ohm'] else '')
        note='Near-pole azimuth is grid-sensitive' if k=='phi_deg' else 'Degrees from +z' if k=='theta_deg' else 'Change in percentage points' if pct else 'Array minus original in dB' if db else 'Returned power relative to incident power' if k=='reference_ohm' else 'Array minus original in tabulated units'
        if k=='reference_ohm':note='Native solver wave reference'
        rows.append(dict(metric=k,original_single=a,single_enlarged_ground=b,new_array=c,absolute_difference=delta,relative_difference_percent=ratio,interpretation=note))
    write(C/'Single_vs_Array_150GHz.csv',rows)
    freq=[frequency(folder) for folder in folders];long=[]
    for label,folder,series in zip(labels,folders,freq):
        f,g,z0,z,g50=scattering(folder)
        for v in series:
            k=np.argmin(abs(f-v['f_GHz']));mis=1-abs(g50[k])**2;total=v['rad_eff_pct']*mis
            long.append(dict(design=label,**v,S11_common50_dB=20*np.log10(abs(g50[k])),total_common50_pct=total,realized_common50_dBi=v['Dmax_dBi']+10*np.log10(total/100)))
    write(C/'Single_vs_Array_Frequency.csv',long)
    optimum=[]
    for label,m,series in zip(labels,met,freq):
        valid=[v for v in series if v['S11_dB']<=-10]
        for key,opts in [('Best realized gain among matched monitors',valid),('Highest gain among all monitors',series),('Highest directivity among all monitors',series)]:
            if opts:optimum.append(dict(design=label,criterion=key,**max(opts,key=lambda v:v['Dmax_dBi' if 'directivity' in key else 'realized_gain_dBi'])))
    write(C/'Operating_Point_Comparison.csv',optimum)
    for key,y,name in [('Dmax_dBi','Maximum directivity (dBi)','Directivity_Comparison'),('realized_gain_dBi','Maximum realized gain at common 50 Ω (dBi)','Realized_Gain_Comparison')]:
        fig,ax=plt.subplots(figsize=(7.5,4.5))
        for series,label,c in zip(freq,labels,colors):
            plotted=([v['realized_common50_dBi'] for v in long if v['design']==label] if key=='realized_gain_dBi' else [v[key] for v in series])
            ax.plot([v['f_GHz'] for v in series],plotted,'.-',label=label,color=c)
        ax.set(xlabel='Frequency (GHz)',ylabel=y,title='CST farfield monitor samples');ax.legend();ax.grid(alpha=.2);save(fig,name)
    fig,ax=plt.subplots(figsize=(7.5,4.5))
    for series,label,c in zip(freq,labels,colors):
        for key,style in [('rad_eff_pct','.-'),('total_eff_pct','.:' )]:ax.plot([v['f_GHz'] for v in series],[v[key] for v in series],style,label=label+(' • radiation' if key.startswith('rad') else ' • total'),color=c)
    ax.set(xlabel='Frequency (GHz)',ylabel='Efficiency (%)',ylim=(0,100));ax.legend(fontsize=8,ncol=2);ax.grid(alpha=.2);save(fig,'Efficiency_Comparison')
    fig,ax=plt.subplots(figsize=(7.5,4.5));band50=[]
    for folder,label,c in zip(folders,labels,colors):
        f,g,z0,z,g50=scattering(folder);db=20*np.log10(abs(g50));ax.plot(f,db,label=label,color=c)
        for band in band_edges(f,db):band50.append(dict(design=label,**band))
    write(C/'Common_50ohm_Bandwidth.csv',band50)
    ax.axhline(-10,color='#666',ls=':');ax.set(xlabel='Frequency (GHz)',ylabel='S11 at common 50 Ω (dB)');ax.legend();ax.grid(alpha=.2);save(fig,'S11_Comparison')
    fig,ax=plt.subplots(figsize=(7.5,3.3))
    for i,m in enumerate(met):
        lo=m['f_low_GHz'];hi=m['f_high_GHz'];ax.plot([lo,hi],[i,i],color=colors[i],lw=7,solid_capstyle='butt');ax.text((lo+hi)/2,i+.09,f'{lo:.2f}–{hi:.2f} GHz',ha='center',fontsize=9)
    ax.axvline(150,color='#777',ls=':');ax.set(yticks=range(3),yticklabels=labels,ylim=(-.4,2.45),xlabel='Native −10 dB matched interval (GHz)');ax.grid(axis='x',alpha=.2);save(fig,'Bandwidth_Comparison')
    planes=[sphere(R if folder==P else folder)[1] for folder in folders]
    for pl in ['E','H']:
        fig,axes=plt.subplots(2,1,figsize=(8,6.8),sharex=True)
        for q,label,c in zip(planes,labels,colors):
            t,d=q[pl];axes[0].plot(t,d,label=label,color=c);axes[1].plot(t,d-max(d),color=c)
        axes[0].set(ylabel='Absolute directivity (dBi)',ylim=(-30,12),title=pl+'-plane at 150 GHz');axes[1].set(ylabel='Relative to cut peak (dB)',xlabel='Signed angle from +z (degrees)',ylim=(-32,2),xlim=(-180,180));axes[1].axhline(-3,color='#666',ls=':');axes[0].legend(fontsize=9)
        for ax in axes:ax.grid(alpha=.2)
        save(fig,pl+'_Plane_Comparison')
    (C/'Comparison_Metrics.json').write_text(json.dumps(dict(zip(['original','ground_control','array'],met)),indent=2))
if __name__=='__main__':run()

