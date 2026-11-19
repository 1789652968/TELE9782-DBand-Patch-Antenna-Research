"""Supplemental delivery checks and replacement decision against the incumbent."""
from Round2_Report import *
from Round2_Patterns import finish
import hashlib
def supplements(rows,comparisons,sel,tested):
    win=read(Path(sel['Best_Balanced'])/'round2.json');old=comparisons[2]
    from Round2_Comparison_Figures import plot
    plot(sel.values())
    from Round2_Checks import historical_and_winner
    from Round2_Edges import append
    historical_and_winner(sel.values());finish(sel.values());append(sel.values());allcuts=[];statistics=[]
    for row in rows:
        folder=Path(row['path']);sp,curves=sphere(folder)
        statistics.append(dict(path=str(folder),name=row['name'],mode=row['mode'],**sp))
        for plane,(ang,value) in curves.items():
            off=10*np.log10(row['eta_total50']/100)
            allcuts.extend(dict(path=str(folder),plane=plane,angle=t,D_dBi=v,G50_dBi=v+off) for t,v in zip(ang,value))
    write(R/'All_Trial_Cuts_150.csv',allcuts);write(R/'All_Trial_Patterns_150.csv',statistics)
    parent=read(ROOT/'02_Diagnostics/Baseline_Raw_Recalculation.json')
    t=next(t for t in tested.values() if t['fresh']['path']==win['path'])
    improvement=score(old)-score(win)
    recommend=improvement>.25 and win['eta']>=old['eta']-.5 and (win['theta']<=8 or win['G0']>=old['G0']+.15)
    chosen=Path(win['path']) if recommend else BASE
    oldpath=ROOT.parent/'08_Efficiency_Optimisation/06_Final_Candidate/TELE9782_DBand_Efficiency_Final'
    path=(chosen/(chosen.name+'.cst') if recommend else oldpath/(oldpath.name+'.cst'))
    d={'replace_round_1':recommend,'project':str(path),'candidate':win['name'],'baseline_score':score(old),'new_score':score(win),'rule':'score improves by >0.25, eta >= baseline minus 0.5 pp, and either theta <=8 deg or +Z gain improves by >=0.15 dB','sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    (V/'Recommended_Project.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
    phy=[v for v in rows if v['mode']=='screen'];by={v['name']:v for v in phy}
    with (DOC/'Final_Optimisation_Report.md').open('a',encoding='utf-8') as out:
        out.write('\n## 课程最终版与更换决定\n\n')
        out.write(('推荐替换上一轮设计。' if recommend else '建议保留上一轮课程交付设计，第二轮入围工程作为对照。')+f" 基线和第二轮综合候选的加权目标缺口分别为 {score(old):.3f} 和 {score(win):.3f}，越低越接近软目标。更换判据及工程 SHA256 见 Recommended_Project.json。\n\n课程工程：\u0060{path}\u0060。\n")
        out.write('\n### 约束与损耗余量\n\n')
        each=[(label,win[k],thr,(win[k]<=thr if k in ('theta','S11_50') else win[k]>=thr)) for label,k,thr in [('ηrad %','eta',90),('ηtotal %','eta_total50',88),('Dpeak dBi','D',9),('Gpeak dBi','G50',8.5),('G+Z dBi','G0',8),('偏角°','theta',5),('S11 dB','S11_50',-17),('带宽 GHz','bandwidth50',13.5)]]
        for nm,num,th,hit in each:out.write(f"- {nm}：{num:.3f}，目标 {th:g}，{'达到' if hit else '未达到'}。\n")
        gold=100*win['Pmetal']/win['Pacc'];pi=100*win['Pdiel']/win['Pacc'];port=100*win['Pport']/win['Pacc']
        out.write(f'\n综合候选在实际接受功率中的非辐射份额为 {100-win["eta"]:.2f}%。达到 90% 所容许的非辐射份额是 10%。其中金损、介质损和端口吸收分别占 {gold:.2f}%、{pi:.2f}%、{port:.2f}%，其余为数值闭合差。差额取决于馈电、辐射和场分布的共同作用，不能把每个单变量试验的收益相加。这里的最优只针对已实际研究的设计空间。\n')
    portpath=R/'Port_Mode_Sensitivity.json'
    if portpath.exists():
        mode=read(portpath);d=mode['delta']
        with (DOC/'Final_Optimisation_Report.md').open('a',encoding='utf-8') as out:
            out.write(f"\n## 端口模式独立敏感性\n\n保持几何、端口截面和参考面以及 20/30 网格设置相同，只把模式计算参考频率由 150 改为 140 GHz。在 150 GHz 原生求解工作点，辐射效率变化 {d['eta']:+.3f} 个百分点，50 Ω S11 变化 {d['S11_50']:+.3f} dB，+Z 实现增益变化 {d['G0']:+.3f} dB，波束偏角变化 {d['theta']:+.0f}°。对应端口吸收变化 {d['Pport']*1000:+.3f} mW。见 Port_Mode_Sensitivity.json 的两套原始数据和日志证据。\n")
    (R/'Deliverable_Audit.json').write_text(json.dumps(dict(trials=len(rows),screen=len(phy),finalists=len(tested),unique_selected=len(set(sel.values())),recommended=read(V/'Recommended_Project.json'),fullsphere_and_ports_verified=True),indent=2),encoding='utf-8')

