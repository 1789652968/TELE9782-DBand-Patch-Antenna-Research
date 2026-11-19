"""Plot CST-exported currents with a common color scale for all five spacings."""
from Array_Results_Extraction import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def mapdata(folder):
    j=np.loadtxt(folder/'Surface_Current_150.txt',skiprows=2)
    j=j[np.abs(j[:,2]-.042)<.0001]
    return j[:,0],j[:,1],np.sqrt(np.sum(j[:,3:9]**2,axis=1))
def run():
    trials=read(W/'selection.json')['trials'];base=max([r for r in trials if r[2]['array_spacing']==1],key=lambda r:r[0])[1]
    folders=[W/'Spacing90',W/base,W/'Spacing110',W/'Spacing120',W/'Spacing130'];ds=[.9,1,1.1,1.2,1.3]
    data=[mapdata(d) for d in folders];scale=np.percentile(np.concatenate([d[2] for d in data]),98)
    fig,axes=plt.subplots(2,3,figsize=(11,6.3),sharex=True,sharey=True,layout='constrained')
    for ax,d,spacing in zip(axes.flat,data,ds):
        x,y,k=d;sc=ax.scatter(x,y,c=k,s=2,marker='s',cmap='viridis',vmin=0,vmax=scale,rasterized=True)
        ax.set_aspect('equal');ax.set_title(f'd = {spacing:.2f} mm');ax.set(xlim=(-1.15,1.15),ylim=(-1.28,.45))
    axes.flat[-1].axis('off')
    fig.supxlabel('x (mm)');fig.supylabel('y (mm)');fig.colorbar(sc,ax=list(axes.flat),extend='max',label='|K| on top gold (A/m)');fig.savefig(C/'Spacing_Current_Comparison.png',dpi=170);plt.close(fig)
    for folder in [*folders,W/'Initial',W/'Length',W/'Inset',R]:
        if not (folder/'Surface_Current_150.txt').exists():continue
        x,y,k=mapdata(folder);fig,ax=plt.subplots(figsize=(7.2,4.8));sc=ax.scatter(x,y,c=k,s=3,marker='s',cmap='viridis',vmin=0,vmax=scale)
        ax.set_aspect('equal');ax.set(xlabel='x (mm)',ylabel='y (mm)',title='Top gold current magnitude at 150 GHz');fig.colorbar(sc,ax=ax,extend='max',label='|K| (A/m)');fig.tight_layout();fig.savefig(folder/'Surface_Current_150.png',dpi=155);plt.close(fig)
if __name__=='__main__':run()
