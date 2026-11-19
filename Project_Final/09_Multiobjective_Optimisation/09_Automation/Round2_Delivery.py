"""Write sourced Markdown and verify the collection using the computed audit tables."""
from Round2_Report import *
def legacy():
    cmp=list(csv.DictReader((LEGACY/'03_Comparison/Common50_150GHz.csv').open()))
    bands=list(csv.DictReader((LEGACY/'03_Comparison/Common_50ohm_Bandwidth.csv').open()))
    rows=[]
    for i,pat,name in [(0,ROOT.parent/'02_Simulation_Results','Original single'),(2,LEGFIG,'Previous array')]:
        d=cmp[i];sp,_=sphere(pat);et=float(d['total_eff_50_pct']);rows.append(dict(name=name,solver='SUCCESS',eta=float(d['rad_eff_pct']),eta_total50=et,S11_50=float(d['reflection_50_dB']),D=float(d['directivity_dBi']),G50=float(d['realized_gain_50_dBi']),D0=sp['D_broadside_dBi'],G0=sp['D_broadside_dBi']+10*np.log10(et/100),theta=sp['theta_deg'],phi=sp['phi_deg'],sphere_mean=sp['sphere_mean'],bandwidth50=float(bands[i]['BW_GHz']),low50=float(bands[i]['f_low_GHz']),high50=float(bands[i]['f_high_GHz']),path=str(pat),source=str(LEGACY/'03_Comparison/Common50_150GHz.csv')))
    rows.append(read(DI/'Baseline_Raw_Recalculation.json')|dict(name='Round 1'))
    return rows
def beam_diagnosis(rows,base):
    baseline()
    lookup={q['name']:q for q in rows if q['mode']=='screen'}
    names=['Control20','RearShort','RearLong','WideGround','Compact','FeedShiftMinus','FeedShiftPlus','IntermediateRearEdge','NearRearEdge','WideApertureBroadside','MovedWideAperture','RearCoupledShort','RearCoupledResonant']
    printrows=[lookup[n] for n in names if n in lookup]
    if not printrows:return
    text=table(printrows,['name','eta','D','G0','theta','phi','S11_50'],['Coarse trial','ηrad (%)','Dmax (dBi)','G+Z (dBi)','theta (°)','phi (°)','S11 (dB)'])
    with (DOC/'Beam_Squint_Diagnosis.md').open('a',encoding='utf-8') as out:out.write('\n## Controlled perturbations\n\n'+text+'\n\nIn the rear-edge experiment the signal network, branch lengths and port plane are unchanged. The large shift in YZ with the rear edge establishes finite-ground/substrate sensitivity. Because the dielectric and gold footprints change together, the experiment cannot separate dielectric edge scattering from ground-edge current. Offsets use a 2° sphere. Near +Z the azimuth is poorly conditioned. Peak directions in a given single-port solution are common to directivity and realized gain because the efficiency factor is a positive angle-independent scalar.\n')
def documentation(rows,comparisons,sel,vset,fr,audits):
    old=comparisons[2];coarse=[r for r in rows if r['mode']=='screen'];flags={k:read(Path(v)/'round2.json') for k,v in sel.items()}
    win=flags['Best_Balanced'];top=flags['Highest_Efficiency'];br=flags['Best_Broadside'];unique=list(dict.fromkeys(sel.values()));q=win;c=read(Path(win['path'])/'parameters.json');base=read(BASE/'parameters.json')
    pointcols=['name','eta','eta_total50','S11_50','D','G50','G0','theta','bandwidth50'];headers=['Design @ 150 GHz','ηrad %','ηtotal,50 %','S11 dB','Dpeak dBi','Gpeak dBi','G+Z dBi','θ°','BW GHz']
    metrics=table(comparisons,pointcols,headers)
    delta=[{'metric':k,'old':old[k],'new':q[k],'change':q[k]-old[k]} for k in ['eta','eta_total50','S11_50','D','G50','G0','theta','bandwidth50']]
    changed=[{'parameter':k,'old':base.get(k),'new':v} for k,v in c.items() if v!=base.get(k) and k not in ('mesh_near','mesh_box')]
    comp_geometry=table(changed,['parameter','old','new'],['Parameter (mm unless dimensionless)','First-round delivery','Balanced delivery'])
    powers=[]
    for rr in [old]+[read(Path(p)/'round2.json') for p in unique]:
        powers.append({**rr,**{key+'%':100*rr[key]/rr['Pacc'] for key in ['Prad','Pmetal','Pdiel','Pport']}})
    mesh=[];rob=[]
    for n,t in vset.items():
        for k in ['screen','production','dense','fresh']:
            x=t[k];mesh.append(x|dict(design=n,grid=k,cells=cells(Path(x['path']))))
        rob.append(dict(name=n,eta_range=t['eta_range'],beam_range=t['beam_range'],valid=t['accepted']))
    write(R/'Mesh_Convergence.csv',mesh)
    tol_dir=Path(read(R/'Selected_Sensitivity_Study.json')['path']) if (R/'Selected_Sensitivity_Study.json').exists() else A/'Manufacturing_Sensitivity'
    tol=[z for z in rows if z['mode']=='sensitivity' and Path(z['path']).parent==tol_dir];nom=next((z for z in tol if z['name']=='Nominal'),None)
    if nom:
        for z in tol:z['delta_eta_pp']=z['eta']-nom['eta'];z['delta_G0_dB']=z['G0']-nom['G0'];z['delta_theta_deg']=z['theta']-nom['theta'];z['delta_S11_dB']=z['S11_50']-nom['S11_50']
        write(R/'Manufacturing_Sensitivity.csv',tol)
    wt=[z for z in fr if z['name']==win['name'] and z['frequency_GHz'] in [145,150,154]];st=next(t for t in vset.values() if t['fresh']['path']==win['path'])
    support=all(z['eta']>=90 for z in [next(t for t in vset.values() if t['fresh']['path']==top['path'])[k] for k in ['production','dense','fresh']])
    metal_path=ROOT.parent/'08_Efficiency_Optimisation/07_Results_and_Figures/All_Candidates.csv'
    with metal_path.open(encoding='utf-8-sig',newline='') as fp:
        metal_rows={row['name']:row for row in csv.DictReader(fp) if row['name'] in ['H75_Length','Au3um','Au5um']}
    skin_um=1.e6/np.sqrt(np.pi*150.e9*(4*np.pi*1.e-7)*4.561e7)
    report=f"""# TELE9782 • 150 GHz 第二轮多目标优化

## 选型结果

完成 {len(coarse)} 个粗网格结构求解、{len(vset)} 套入围几何的验证及 {len(tol)} 次公差分析（含标称对照）。每个最终候选保留原生 CST 项目、同名结果目录、原始方向图及触发重新求解后的记录。

最高可信交付点为 **{top['eta']:.3f}%**，方案 {top['name']}。{'生产网格、加密网格和交付复算均达到 90%。' if support else '90% 目标未通过三次高分辨率验证。'}最小偏角候选为 {br['name']}，θ = {br['theta']:.0f}°，+Z 增益 {br['G0']:.3f} dBi。综合候选为 **{win['name']}**，交付复算值 {win['eta']:.3f}%，+Z 增益 {win['G0']:.3f} dBi，θ = {win['theta']:.0f}°。所有增益项采用 50 Ω 实现增益。结果属于给定材料模型和有限搜索空间的仿真，没有样品实测。

{metrics}

## 相对第一轮交付工程的变化

{table(delta,['metric','old','new','change'],['Metric','Round 1','Balanced','Difference'])}

## 结构与搜索

从第一轮已保存的参数化历史和真实材料克隆模型。原端口位于 −Y，端口平面、端口截面和 0.5 mm launch 参数在搜索中固定。横向中心距、贴片长宽、厚度、变压线、倒角、T 结、有限地板后缘、金属网络纵向位置以及后缘无源贴片分别在记录的试验中研究。单变量试验适于解释趋势，组合试验仅说明该参数组合的性能。所有长度单位为 mm。几何迁移会改变端口到 T 结的真实金属长度；两支路仍关于 X=0 镜像。

{comp_geometry}

金和聚酰亚胺均从母工程继承。标称 εr=3.5、tanδ=0.0027、σ=4.561×10⁷ S/m、金厚 0.002 mm。基板研究同步缩放馈线并初调贴片长度，随后基于求解的匹配频点有界调整长度与内嵌深度。制造误差阶段的材料扰动单独标记。有限宽度地板与开放边界直接进入三维计算。没有单独给表面波指定功率份额。

150 GHz、σ=4.561×10⁷ S/m、μr=1 的良导体趋肤深度为 {skin_um:.3f} μm。标称金厚 2 μm 约为 {2/skin_um:.1f} 倍趋肤深度。第一轮真实材料的同设置网格试验中，2、3、5 μm 金厚对应的辐射效率分别为 {float(metal_rows['H75_Length']['eta']):.3f}%、{float(metal_rows['Au3um']['eta']):.3f}% 和 {float(metal_rows['Au5um']['eta']):.3f}%。2 和 3 μm 的模型均为 100,920 单元，5 μm 的模型为 161,472 单元。加厚没有显示稳定效率收益，因此本轮工程保留 2 μm，另用实际求解检查制造厚度偏差。来源为 08_Efficiency_Optimisation/07_Results_and_Figures/All_Candidates.csv 中的 H75_Length、Au3um 和 Au5um；这三个历史值未参加第二轮候选排名。

## 辐射损耗与波束偏转

{table(powers,['name','Pacc','Prad','Pmetal','Pdiel','Pport','residual_pct'],['Model','Accepted W','Radiated W','Gold W','Polyimide W','Port absorption W','Residual % of accepted'])}

在综合候选上，金损占接受功率 {100*q['Pmetal']/q['Pacc']:.2f}%，介质损占 {100*q['Pdiel']/q['Pacc']:.2f}%，端口吸收占 {100*q['Pport']/q['Pacc']:.2f}%。第一轮对应值为 {100*old['Pmetal']/old['Pacc']:.2f}%、{100*old['Pdiel']/old['Pacc']:.2f}%、{100*old['Pport']/old['Pacc']:.2f}%。无损耗材料未用于上述比较。各工程 Current_Regions.csv 以面积加权对比热点，区域可有重叠，因此物理损耗解释以 CST 的全局积分为准。

Beam_Squint_Diagnosis.md 给出参考坐标、基线两支路复场、表面电流和同网格后缘实验。综合候选的全空间最大值朝 θ={q['theta']:.0f}°、φ={q['phi']:.0f}°。它在法线方向比峰值低 {q['G50']-q['G0']:.3f} dB。完整三维表单独验证了原生实现增益和方向性的峰值。对单端口模型，辐射效率与失配效率均为方向无关的标量。

## 候选筛选与 Pareto

硬门槛为 150 GHz 的 50 Ω S11≤−10 dB、Dmax≥6.5 dBi、CST 成功、闭合残差绝对值≤2%、全空间方向性积分相对误差<2%。筛选保留所有实际结果。Screen_Pareto.csv 采用相同筛选网格，在辐射效率、总效率、峰值方向性、峰值和法线实现增益、带宽、偏角及 S11 上判断支配关系。最高效率在可行集合中选择；法线候选先要求 η≥81%，再以偏角、法线增益和效率排序。综合选择采用预先固定的目标缺口评分；权重与缺口尺度可见 Round2_Search.py 的 balanced()。同一几何可承担多个角色。表格按角色保留重复行。

## 独立验证

{table(mesh,['design','grid','cells','eta','eta_total50','S11_50','D','G0','theta'],['Geometry','Solve','Cells','ηrad %','ηtotal %','S11 dB','Dpeak dBi','G+Z dBi','θ°'])}

36/54 网格先求解，38/57 网格独立重建；从保存的 36/54 模型另存交付件、关闭、重开并再次运行，最后重开检查完整 1001 点复 S11。生产、加密、交付复算三次均须通过硬门槛。工程判断所用稳定带为效率峰峰差≤1.2 个百分点、波束角峰峰差≤4°。这两个数是本研究的判据。综合设计这三个解的效率峰峰差为 {st['eta_range']:.3f} 个百分点，偏角峰峰差 {st['beam_range']:.1f}°。每个交付目录的 Reopen_Verification.json 和 Independent_Audit.json 记录原生方向图、端口、参考阻抗、Touchstone 以及功率复核。

ηrad=Prad/Paccepted，ηtotal,50=ηrad(1−|Γ50|²)，Greal,50=D+10log10(ηtotal,50)。功率表采用 CST 原生端口激励。Port absorption 和 outgoing modal power 分开处理；仅前者计入接受功率分解。CST 使用工作频率附近的色散材料无损近似求端口模，三维域内仍包含金与介质损耗。端口和边界定义在各比较组保持一致。相同端口的结果可用于几何对比；复算差异仍是绝对性能精度的限制。

## 工作频带与方向图

{table(wt,['frequency_GHz','eta_pct','total50_pct','S11_50','D','Gpeak50','G0','theta','phi'],['GHz','ηrad %','ηtotal %','S11 dB','Dpeak dBi','Gpeak dBi','G+Z dBi','θ°','φ°'])}

波束方向由真实监视点的 2° 网格选取，接近法线时 φ 对微小数值变化敏感。−10 dB 连续带宽仅在相邻原始 S 参数频点间线性定位交点。远场频率图仅标出真实监视器。E/H 主瓣宽度、前向主切面次峰、法线极化分量与全空间积分见 Radiation_Pattern_Audit.csv。法线极弱交叉极化可能受数值底噪影响；切面次峰不代表全空间最大旁瓣。

## 制造敏感性

采用假设公差，分别改变 h ±3 μm、贴片长/宽 ±5 μm、馈线宽 ±5 μm、金厚 ±0.3 μm、εr ±0.07、tanδ ±0.0004，同一粗网格、无重匹配。结果是单因素数值敏感性，不能推算制造良率。

{table(tol,['name','eta','delta_eta_pp','S11_50','G0','theta'],['Perturbation','ηrad %','Δη pp','S11 dB','G+Z dBi','θ°'])}

## 可复核的交付

推荐比较路径：{win['path']}。原始 Baseline 和全部中间 CST 工程均保留。验证和数值表位于 08_Results_and_Figures。完整执行入口与证据文件在 Reproduction_Guide.md。
"""
    (DOC/'Final_Optimisation_Report.md').write_text(report,encoding='utf-8')
def main():
    rows=all_trials();old=legacy();beam_diagnosis(rows,old[-1])
    if not (V/'Final_Selection.json').exists():return
    sel=read(V/'Final_Selection.json');vs=read(V/'Verification_Results.json')
    if 'fallback' in sel:raise RuntimeError('No stable new finalist: provide a baseline retention report from verification records')
    cmp=old+[read(Path(p)/'round2.json')|dict(name=role) for role,p in sel.items()]
    write(R/'Multiobjective_Comparison.csv',cmp);fr=[];aud=[]
    for path in dict.fromkeys(sel.values()):
        folder=Path(path);fr+=freq_rows(folder);info=final_audit(folder);aud.append(info|{'name':folder.name})
    write(R/'Final_Frequency_Monitors.csv',fr);write(R/'Radiation_Pattern_Audit.csv',aud)
    figures(rows,cmp,sel,vs);documentation(rows,cmp,sel,vs,fr,aud)
    from Round2_Supplement import supplements
    supplements(rows,cmp,sel,vs)
    from Round2_Angular_Resolution import summarize
    summarize(sel.values())
    from Explain_Final_Losses import append
    append()
if __name__=='__main__':main()

