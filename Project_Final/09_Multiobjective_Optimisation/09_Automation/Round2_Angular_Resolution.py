"""Evaluate the 150 GHz native far field on a 1 deg grid from stored CST currents."""
from pathlib import Path
def complete_angular(path):
    if not path.is_file():return False
    with path.open(errors='replace') as f:
        next(f,None);next(f,None)
        n=sum(1 for line in f if line.strip() and len(line.split())==8)
    return n in (181*360,181*361)
def export(p,folder):
    path=folder/'Farfield_150_1deg_Directivity.txt'
    if complete_angular(path):return
    m=p.model3d;assert m.SelectTreeItem(r'Farfields\farfield (f=150) [1]')
    ff=m.FarfieldPlot;ff.Reset();ff.Plottype('3d');ff.SetPlotMode('directivity');ff.SelectComponent('Abs');ff.SetScaleLinear(False);ff.SetPlotRangeOnly(False);ff.Step(1);ff.Step2(1);ff.Plot()
    a=m.ASCIIExport;a.Reset();a.FileName(str(path));a.Execute()
def summarize(paths):
    from Round2_Analysis import R,DOC,read,write,np
    rows=[]
    for path in dict.fromkeys(paths):
        folder=Path(path);q=read(folder/'round2.json')
        a=np.loadtxt(folder/'Farfield_150_1deg_Directivity.txt',skiprows=2);th=np.unique(a[:,0]);ph=np.unique(a[:,1])
        assert np.allclose(np.diff(th),1) and np.allclose(np.diff(ph),1)
        assert len(a)==len(th)*len(ph) and len(th)==181 and len(ph) in (360,361)
        a=a[a[:,1]<360];w=10**(a[:,2]/10)*np.sin(np.radians(a[:,0]));mean=float(w.sum()*np.radians(1)**2/(4*np.pi))
        peak=a[a[:,2].argmax()]
        rows.append(dict(design=folder.name,theta_2deg=q['theta'],theta_1deg=peak[0],phi_2deg=q['phi'],phi_1deg=peak[1],sphere_mean_2deg=q['sphere_mean'],sphere_mean_1deg=mean,mean_equivalent_dB=10*np.log10(mean),native_Dmax=q['D'],Dmax_1deg=peak[2],angular_samples=len(a),closure_pct=q['residual_pct']))
    write(R/'Angular_Resolution_Check.csv',rows)
    out=DOC/'Final_Optimisation_Report.md'
    with out.open('a',encoding='utf-8') as f:
        f.write('\n## 原生角分辨率复查\n\n从已保存的原生 150 GHz 远场重新评估 1° 全空间网格。相对全空间方向性平均值的偏差给出角积分和绝对增益的核对量，报告沿用各工程的原生增益及接受功率效率。\n\n')
        for t in rows:f.write(f"- {t['design']} 的 2°/1° 网格峰值偏角为 {t['theta_2deg']:.0f}°/{t['theta_1deg']:.0f}°。两者方向性积分为 {t['sphere_mean_2deg']:.5f}/{t['sphere_mean_1deg']:.5f}，后者相当于偏离单位积分 {t['mean_equivalent_dB']:+.3f} dB。功率闭合差占接受功率 {t['closure_pct']:.3f}%。\n")

