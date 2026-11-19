"""Generate field comparisons and per-frequency, full angular data derived from CST samples."""
from Round2_Analysis import *
def detail(folder,sub):
    files=sorted(folder.glob('Farfield_*_Sphere.txt'));out=[]
    for path in files:
        f=float(path.name.split('_')[1]);a=np.loadtxt(path,skiprows=2)
        ph=np.unique(a[:,1]);th=np.unique(a[:,0]);a=a[np.lexsort((a[:,0],a[:,1]))];shape=(len(ph),len(th));D=a[:,2].reshape(shape)
        phi=np.radians(a[:,1]);et=10**(a[:,3]/20)*np.exp(1j*np.radians(a[:,4]));ep=10**(a[:,5]/20)*np.exp(1j*np.radians(a[:,6]))
        # Ludwig-3, y-polarized co component; unit vectors rotate with phi.
        co=et*np.sin(phi)+ep*np.cos(phi);cross=et*np.cos(phi)-ep*np.sin(phi)
        pk=np.max(D);forward=a[:,0]<=90;main=forward&(a[:,2]>=pk-3)
        cr=20*np.log10(np.maximum(abs(cross),1.e-16)/np.maximum(abs(co),1.e-16))
        ip,jp=np.unravel_index(D.argmax(),shape);lobes=[]
        for i,p in enumerate(ph):
            for j in range(1,len(th)-1):
                if not 0<th[j]<90 or (i,j)==(ip,jp):continue
                val=D[i,j]
                neighbours=[D[(i+di)%len(ph),j+dj] for di in [-1,0,1] for dj in [-1,0,1] if di or dj]
                if val>=max(neighbours) and val>min(neighbours):
                    cosg=np.cos(np.radians(th[j]))*np.cos(np.radians(th[jp]))+np.sin(np.radians(th[j]))*np.sin(np.radians(th[jp]))*np.cos(np.radians(p-ph[ip]))
                    if np.degrees(np.arccos(np.clip(cosg,-1,1)))>10:lobes.append((val,th[j],p))
        zo=np.flatnonzero((a[:,0]==0)&(a[:,1]==0))[0];bo=np.flatnonzero((a[:,0]==180)&(a[:,1]==0))[0]
        out.append(dict(design=folder.name,f_GHz=f,main_theta=th[jp],main_phi=ph[ip],sampled_peak_dBi=pk,D0_dBi=a[zo,2],front_back_axial_dB=a[zo,2]-a[bo,2],front_back_hemisphere_peaks_dB=max(a[forward,2])-max(a[a[:,0]>90,2]),crosspol_dBc_at_plusZ=cr[zo],worst_crosspol_dBc_forward_3dB_contour=max(cr[main]),secondary_forward_local_peak_dBc=max(lobes)[0]-pk if lobes else None))
        for label,ang in [('E',90),('H',0)]:
            pos=D[np.where(ph==ang)[0][0]];neg=D[np.where(ph==ang+180)[0][0]]
            write(sub/f'{folder.name}_{f:g}GHz_{label}.csv',[dict(signed_theta_deg=t,directivity_dBi=v) for t,v in zip(np.r_[-th[:0:-1],th],np.r_[neg[:0:-1],pos])])
    return out
def eplots(folders):
    plots=plt.subplots(len(folders),2,figsize=(9,3.1*len(folders)),squeeze=False);fig,axes=plots
    for ax,(label,folder) in zip(axes,folders):
        a=np.loadtxt(folder/'Efield_XY_150.txt',skiprows=2);x,y=a[:,0],a[:,1];z=a[:,7]+1j*a[:,8];m=abs(z);ref=z[m.argmax()]
        mask=m>max(m)*.03
        plt.sca(ax[0]);p=plt.scatter(x,y,c=20*np.log10(np.maximum(m,1.)),s=5,cmap='inferno',vmin=55,vmax=110);fig.colorbar(p,ax=ax[0],label='dB(V/m)');ax[0].set_title(label+' • |Ez|')
        plt.sca(ax[1]);p=plt.scatter(x[mask],y[mask],c=np.angle(z[mask]/ref,deg=True),s=5,cmap='twilight',vmin=-180,vmax=180);fig.colorbar(p,ax=ax[1],label='degrees');ax[1].set_title('Phase relative to peak-|Ez| sample')
        for aaxx in ax:aaxx.set_aspect('equal');aaxx.set_xlabel('x (mm)');aaxx.set_ylabel('y (mm)')
    save('Efield_Amplitude_Phase_Comparison')
def finish(paths):
    out=[];sub=R/'Angular_Cuts';sub.mkdir(exist_ok=True);folders=[('Previous 1×2',DI/'PreviousArray'),('Round 1',DI/'FirstOptimised')]
    for path in dict.fromkeys(paths):
        folder=Path(path);out+=detail(folder,sub);folders.append((folder.name,folder))
    write(R/'Full_Sphere_Audit.csv',out)
    if all((f/'Efield_XY_150.txt').exists() for _,f in folders):eplots(folders)
    oldfig=ROOT.parent/'07_Array_1x2/02_Simulation_Results'
    source=oldfig/'Surface_Current_Map.png'
    if source.exists():
        import shutil
        shutil.copyfile(source,R/'Surface_Current_Previous_Array.png')
    current_plot(BASE)

