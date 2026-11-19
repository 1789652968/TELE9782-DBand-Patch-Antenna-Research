"""Document separate CST loss terms and the independent port sensitivity of the efficiency leader."""
from Round2_Analysis import ROOT,R,DOC,read
def append():
    entry=R/'Highest_Efficiency_Port_Check.json'
    if not entry.exists():return
    base=read(ROOT/'02_Diagnostics/Baseline_Raw_Recalculation.json')
    sl=read(ROOT/'07_Final_Candidates/Final_Selection.json');from pathlib import Path
    hi=read(Path(sl['Highest_Efficiency'])/'round2.json');br=read(Path(sl['Best_Broadside'])/'round2.json')
    probe=read(entry);delta=probe['delta']
    with (DOC/'Final_Optimisation_Report.md').open('a',encoding='utf-8') as f:
        f.write('\n## 最高效率候选的损耗来源与数值敏感性\n\n')
        for title,key in [('金属损耗','Pmetal'),('介质损耗','Pdiel'),('端口吸收','Pport')]:
            a=100*base[key]/base['Pacc'];b=100*hi[key]/hi['Pacc']
            f.write(f"- {title}占接受功率的比例从 {a:.3f}% 变为 {b:.3f}%，差 {b-a:+.3f} 个百分点。\n")
        f.write(f"\n剩余闭合差从 {base['residual_pct']:.3f}% 变为 {hi['residual_pct']:.3f}%。该分解中变化最大的一项为端口吸收；效率的净变化包括所有功率项。端口截面与参考面保持一致。独立粗网格控制把端口模式计算频率从 150 改到 140 GHz，观察到工作点辐射效率变化 {delta['eta']:+.3f} 个百分点，端口吸收变化 {1000*delta['Pport']:+.3f} mW，偏角变化 {delta['theta']:+.0f}°。见 Highest_Efficiency_Port_Check.json。CST 日志的 F-Calc 分别为 150 和 140；两次计算都在 150 GHz 对端口截面材料取常量近似。该试验只检验模式频率设置的敏感性，绝对效率仍取决于模型采用的边界和端口定义。\n")
        f.write(f"\n法线候选相对第一轮的效率增量为 {br['eta']-base['eta']:+.3f} 个百分点，和同一几何三次高分辨率计算之间的离散程度同时解读。它的主要收益是主瓣回到法线附近。\n")
        f.write('\n系统重启时，法线交付工程已经保存并完成重开复算。导出中断的 Touchstone 文本已从原生数据库重新导出，1001 个复数采样全部核对。核对量在该工程的 Touchstone_Recovery.json。\n')


        import csv
        with (R/'Final_Frequency_Monitors.csv').open(encoding='utf-8-sig',newline='') as src:
            measured=[row for row in csv.DictReader(src) if float(row['frequency_GHz']) in (145,150,154)]
        f.write('\n## 三项候选的频率稳定性\n\n|交付候选|频率 GHz|主瓣偏角 °|+Z 实现增益 dBi|S11 dB，50 Ω|\n|---|---:|---:|---:|---:|\n')
        for row in measured:
            f.write(f"|{row['name']}|{float(row['frequency_GHz']):.0f}|{float(row['theta']):.0f}|{float(row['G0']):.3f}|{float(row['S11_50']):.2f}|\n")
        far=next(row for row in measured if row['name']==br['name'] and float(row['frequency_GHz'])==154)
        f.write(f"\n法线候选在 154 GHz 的实算偏角为 {float(far['theta']):.0f}°，此时 S11 为 {float(far['S11_50']):.2f} dB。150 GHz 工作点的偏角改善不能外推到整个匹配频带。\n")
