"""Write paired-grid and broadside checks for the two physical array designs."""
from Efficiency_Analysis import *
def extra():
    verification=read(V/'verification.json');folder=Path(verification['path']).parent
    selection=read(V/'selection.json')
    old=data(OLD/'02_Simulation_Results/Mesh_Convergence.csv')
    allcases=data(R/'All_Candidates.csv');rows=[]
    for aim,key in [(20,selection['screen']),(36,selection['source']),(38,selection['holdout'])]:
        prev=next(v for v in old if float(v['mesh_near'])==aim);new=next(v for v in allcases if v['name']==key)
        rows.append(dict(steps_per_wave=aim,steps_per_box=float(new['mesh_box']),previous_case=prev['name'],new_case=key,previous_cells=int(prev['cells']),new_cells=int(new['cells']),previous_eta_pct=float(prev['rad_eff_pct']),new_eta_pct=float(new['eta']),gain_in_efficiency_pp=float(new['eta'])-float(prev['rad_eff_pct'])))
    write(R/'Matched_Mesh_Comparison.csv',rows)
    m=case(folder);o=read(OLD/'03_Comparison/Comparison_Metrics.json')['array'];g0=m['D_broadside_dBi']+10*np.log10(m['eta_total50']/100)
    oldg=float(o['D_broadside_dBi'])+10*np.log10(sources()[2]['eta_total50']/100)
    text='## 同网格设定的独立交叉检查与正上方性能\n\n'
    text+='每个设计各自按相同每波长及每包围盒网格参数离散，几何不同导致单元数不同。下表是重开复算前的独立求解对比。交付值使用最终重开求解。\n\n| 网格参数 | 旧阵列 ηrad | 新阵列 ηrad | 差值 |\n|---|---:|---:|---:|\n'
    for v in rows:text+=f"| {v['steps_per_wave']}/{v['steps_per_box']:g} | {v['previous_eta_pct']:.2f}% | {v['new_eta_pct']:.2f}% | {v['gain_in_efficiency_pp']:+.2f} 点 |\n"
    text+=f"\n以 +Z 为固定链路方向，旧阵列和新阵列的 50 Ω 实现增益分别为 {oldg:.3f} 和 {g0:.3f} dBi，变化 {g0-oldg:+.3f} dB。新阵列在 +Z 的方向性为 {m['D_broadside_dBi']:.3f} dBi，低于它自身的峰值 {m['D']-m['D_broadside_dBi']:.3f} dB。主瓣 θ 从 {o['theta_deg']:.0f}° 改为 {m['theta_deg']:.0f}°；θ 是相对 +Z 的偏转角。对于指定波束指向的链路，应同时使用这个正上方增益及完整方向图。"
    g=read(folder/'parameters.json')
    oldlen=1.2/2-.513/2+.165+.530
    newlen=g['array_spacing']/2-g['patch_length']/2+g['inset_length']-g['junction_y']
    text+=f"\n\n从 T 结中心至 inset 末端的单侧中心线路径由 {oldlen:.4f} 缩至 {newlen:.4f} mm。主干相应加长，具体损耗归因采用实算的整机功率分量。"
    f=DOC/'Efficiency_Optimisation_Report.md';s=f.read_text(encoding='utf-8')
    if '## 同网格设定的独立交叉检查' not in s:f.write_text(s.replace('## 图表及工程限制',text+'\n\n## 图表及工程限制'),encoding='utf-8')
if __name__=='__main__':extra()
