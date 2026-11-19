"""Common-scale comparisons of recorded 3-D data, with the older 1x2 included."""
from Round2_Analysis import *
def plot(paths):
    prev=ROOT.parent/'07_Array_1x2/02_Simulation_Results'
    unique=list(dict.fromkeys(paths))
    sources=[('Previous 1×2',prev),('Round 1',BASE)]+[(p.parent.name,p) for p in map(Path,unique)]
    fig=plt.figure(figsize=(4.4*len(sources),4.6));norm=plt.Normalize(-15,11)
    for i,(label,folder) in enumerate(sources):
        a=np.loadtxt(folder/'Farfield_150_Sphere.txt',skiprows=2);a=a[np.lexsort((a[:,0],a[:,1]))]
        ph=np.unique(a[:,1]);th=np.unique(a[:,0]);dv=a[:,2].reshape(len(ph),len(th))
        # Periodic seam only; every radius and colour comes from an exported angular sample.
        ph=np.r_[ph,360];dv=np.vstack((dv,dv[0]))
        ph,th=np.meshgrid(np.radians(ph),np.radians(th),indexing='ij')
        r=np.maximum(dv+15,0)/26;x=r*np.sin(th)*np.cos(ph);y=r*np.sin(th)*np.sin(ph);z=r*np.cos(th)
        ax=fig.add_subplot(1,len(sources),i+1,projection='3d');ax.plot_surface(x,y,z,facecolors=plt.cm.viridis(norm(dv)),rstride=2,cstride=2,linewidth=0,antialiased=True,shade=False)
        ax.set(xlim=(-1,1),ylim=(-1,1),zlim=(-1,1),xlabel='X',ylabel='Y',zlabel='Z',title=label);ax.set_box_aspect((1,1,1));ax.view_init(20,-34);ax.set_xticks([0]);ax.set_yticks([0]);ax.set_zticks([0])
    fig.subplots_adjust(bottom=.17);cb=fig.add_axes([.31,.09,.38,.027]);fig.colorbar(plt.cm.ScalarMappable(norm=norm,cmap='viridis'),cax=cb,orientation='horizontal',label='Absolute directivity at 150 GHz (dBi), clipped below −15');fig.savefig(R/'Three_Generation_3D_Farfield.png',dpi=170,bbox_inches='tight');plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(11,4.5),sharey=True)
    for label,folder in sources:
        _,cuts=sphere(folder)
        for ax,(key,cut) in zip(axs,cuts.items()):
            ax.plot(*cut,label=label);ax.set_title(key+' plane');ax.set_xlabel('Signed angle from +Z (degrees)');ax.set_xlim(-115,115);ax.set_ylim(-18,11);ax.grid(alpha=.15)
    axs[0].set_ylabel('Absolute directivity at 150 GHz (dBi)');axs[1].legend(fontsize=8);save('Three_Generation_EH_Cuts')

