"""Assemble the engineering report and reproduction guide from solved cases only."""
from Efficiency_Analysis import *
def main():
    cases=data(R/'All_Candidates.csv');lookup={v['name']:v for v in cases}
    ver=read(V/'verification.json');folder=Path(ver['path']).parent;name=folder.name
    sel=read(V/'selection.json');previous=read(R/'Baseline_Power_Recomputed.json');final=ver['fresh'];fine=ver['previous'];hold=lookup[sel['holdout']];valid=read(R/'Validation.json');p=read(folder/'parameters.json');sp,curves=sphere(folder)
    comp=data(R/'Efficiency_Optimisation_Comparison.csv');a,b,c,d=[lookup[n] for n in ['A_Gold_PI','B_PEC_PI','C_Gold_NoTanD','D_PEC_NoTanD']]
    def table(rs,cols):
        def fmt(v):
            try:return f'{float(v):.3f}'
            except (ValueError,TypeError):return str(v or '—')
        return '\n'.join(['| '+' | '.join(cols)+' |','|'+'|'.join('---' for _ in cols)+'|']+['| '+' | '.join(fmt(r.get(k,'')) for k in cols)+' |' for r in rs])
    def change(k):return final[k]-previous[k]
    def pct(r,k):return 100*float(r[k])/float(r['Pacc'])
    def metric(old,new,k):return float(new[k])-float(old[k])
    def lossrows(rs):
        return [dict(case=v['name'],radiated_pct=pct(v,'Prad'),metal_pct=pct(v,'Pmetal'),dielectric_pct=pct(v,'Pdiel'),port_pct=pct(v,'Pport'),residual_pct=float(v['residual_pct'])) for v in rs]
    feed=[v for v in cases if str(F) in v['source']]
    thickness=[v for v in cases if str(T) in v['source'] and v['name']!='PortFrequency140']
    port=lookup['PortFrequency140'];portbase=lookup[sel['screen']]
    hf=abs(metric(fine,hold,'eta'));hg=abs(metric(fine,hold,'G50'));hd=abs(metric(fine,hold,'D'));fr=abs(metric(fine,hold,'fmin50'))
    recommended=change('eta')>max(hf,abs(fine['eta']-final['eta'])) and final['S11_50']<=-10 and final['D']>=6.5 and sp['theta_deg']<20 and abs(final['residual_pct'])<2
    edge=data(R/'Substrate_Edge_Diagnostics.csv') if (R/'Substrate_Edge_Diagnostics.csv').exists() else []
    obtained=min(float(hold['eta']),float(fine['eta']),final['eta'])>=80 and max(float(hold['S11_50']),float(fine['S11_50']),final['S11_50'])<=-10
    text=f"""# TELE9782 · D-band 1×2 阵列辐射效率优化

## 结论与评价口径

老师指出原单贴片的 71.55% 辐射效率偏低。此前 1×2 阵列在 150 GHz 的效率为 {previous['eta']:.3f}%。本研究以真实 Gold 和原 Polyimide 进行几何优化。最终项目从交付路径重开并重新求解后，辐射效率为 **{final['eta']:.3f}%**，相对旧阵列变化 **{change('eta'):+.3f} 个百分点**。共同 50 Ω 的 S11 为 **{final['S11_50']:.3f} dB**，峰值方向性 **{final['D']:.3f} dBi**，实现增益 **{final['G50']:.3f} dBi**。{'两套高分辨率网格和独立复算均支持 80% 目标。' if obtained else '各次结果对 80% 目标的支持见网格与复算表；不能仅凭某个筛选值认定达到目标。'} {'建议在此仿真设计空间内采用最终项目。' if recommended else '保留新候选供研究，目前不建议无条件替换旧项目。'}

所有指标取自 150 GHz 实际监视频点。ηrad=Prad/Pacc，ηm,50=1−|Γ50|²，ηtot,50=ηrad×ηm,50，Greal,50=Dmax+10log10(ηtot,50)。功率分解保持 CST 激励波的原生口径。固定 50 Ω 只影响反射、失配和实现增益的统一比较。功率未重新分配。表中 eta 和 eta_total50 的单位为 %，S11_50 为 dB，D/G50 为 dBi，bandwidth50 为 GHz，各个 P 为 W。

## 完整基线与功率核查

使用 07 下最终原生 .cst 和同名伴随目录的完整副本。Native_Provenance.json 对照文件内容并从 cst.results 直接读取七条功率结果。原生 S 参数采用约 {previous['Zref']:.3f} Ω。备份工程的入射、反射、接受、辐射功率分别为 {previous['Pin']:.6f}、{previous['Pout']:.6f}、{previous['Pacc']:.6f}、{previous['Prad']:.6f} W。金属、介质及端口吸收分别为 {previous['Pmetal']:.6f}、{previous['Pdiel']:.6f}、{previous['Pport']:.6f} W。闭合残差为 {previous['residual_pct']:.3f}% 的接受功率。原生场、S11、方向性及损耗原始曲线保存在各工程目录；同阻抗归一、波束宽度、损耗占比和比较图来自后处理。

## 材料损耗分离

A/B/C/D 都从同一验证工程克隆，在相同筛选网格参数分别重新求解。PEC 作用于信号导体与地；无损介质仅把 tanδ 设为零，保留 εr 与厚度。空的理想损耗通道仅在该材料本身无损且 CST 未生成对应曲线时记零。

{table([a,b,c,d],['name','cells','eta','S11_50','D','G50','Pmetal','Pdiel','Pport','residual_pct'])}

相对同网格 A，单独 PEC 的效率改变 {metric(a,b,'eta'):+.3f} 点，单独无损介质改变 {metric(a,c,'eta'):+.3f} 点，二者同时理想化改变 {metric(a,d,'eta'):+.3f} 点。比较支持优先研究导体损耗。材料变化也改变输入阻抗、表面电流和分配给各损耗通道的功率。D 给出本模型的理想化诊断上限；三个理想化结果均排除于最终选型之外。

## 馈电结构与匹配

中心线对称，从单一输入端口经 T 结、变压段与弯折到两片 inset。F1 同时减少支路横向跨度并把结点向贴片移动；从端口到结点的共用主干随之加长，整个效果包含新电流分布与互耦。F2 测试较宽且较短的变压段，F3 在两个外角对称削角，F4 还在 T 结内角填入小金属三角。需要时对长度和 inset 调谐。物理端口平面、主地板和边界设置保持与基线一致。下列全部候选都由 CST 完整求解。

{table(feed,['name','array_spacing','junction_y','transformer_width','transformer_length','inset_length','eta','S11_50','D','G50','Pmetal'])}

用于下一阶段的馈电几何取自 **{read(F/'selection.json')['case']}**。排序先排除失配、方向性低于门槛、严重偏轴或功率闭合异常的候选，再比较辐射效率及增益。未将失配时的高效率峰值纳入最终结论。

## 基板与真实金属厚度

h 变化时，信号金属随基板顶面移动，端口 z 截面仍为 −t 至 6h，馈线与变压线宽度按 h 缩放，贴片长度根据边缘延伸调整，再根据实际匹配谷调谐。面内物理端口位置和参考面未移动。厚度和匹配参数同时改变时，数据代表完整可用设计的性能。对比同一组几何上的 2/3/5 μm Gold 可单独考察金属厚度。σ=4.561×10⁷ S/m，150 GHz 的经典趋肤深度约 {valid['skin_depth_um']:.3f} μm。2 μm 已超过十个趋肤深度；进一步加厚的仿真变化还包含表面阻抗、边缘场和网格表示的影响。

{table(thickness,['name','substrate_h','metal_thickness','patch_length','feed_width','inset_length','eta','S11_50','D','G50','Pmetal','Pdiel','Rin','Xin','fmin50'])}

基板侧缘内侧 0.03、0.06、0.09 mm、z=h/2 的 Ez 幅度按接受功率归一，下表亦列全空间远场 70–110° 天顶角范围的辐射份额。这两个量反映近边缘场和低仰角辐射的变化；包含空间辐射与边缘衍射，不能唯一给出某个表面波模的功率。

{table(edge,['case','h_mm','edge_Ez_RMS_Vm_per_sqrtW','near_horizon_radiated_fraction_70_to_110_deg','theta_deg'])}

本轮保持 Polyimide 的 εr=3.5、tanδ=0.0027。对这一材料组合已有明确的效率变化依据，未以低频材料规格替代 D-band 实测数据。工艺上的薄膜厚度、粗糙度、介质各向异性与温度变化仍需实测。

## 最终工程与功率变化

最终阵列间距 {p['array_spacing']:.3f} mm，每片 {p['patch_width']:.3f} × {p['patch_length']:.4f} mm，inset 深度 {p['inset_length']:.4f} mm，基板厚 {p['substrate_h']:.3f} mm，Gold 厚 {1000*p['metal_thickness']:.1f} μm。主馈线宽 {p['feed_width']:.4f} mm，变压段 {p['transformer_width']:.4f} × {p['transformer_length']:.3f} mm；T 结位置 y={p['junction_y']:.3f} mm。miter={bool(p.get('miter'))}，T 三角补偿={bool(p.get('fillet'))}。库内所有架构保持单端口和实体相连的信号体，实际表面电流和左右馈点场用于最终核查。

{table(comp[:4],['name','eta','eta_total50','S11_50','D','G50','bandwidth50','E_HPBW_deg','H_HPBW_deg'])}

以接受功率为分母的百分比分解如下。

{table(lossrows([previous,final]),['case','radiated_pct','metal_pct','dielectric_pct','port_pct','residual_pct'])}

相对旧阵列，金属耗散占比变化 {pct(final,'Pmetal')-pct(previous,'Pmetal'):+.3f} 点，介质耗散占比变化 {pct(final,'Pdiel')-pct(previous,'Pdiel'):+.3f} 点，端口吸收占比变化 {pct(final,'Pport')-pct(previous,'Pport'):+.3f} 点。各项功率的实际变化解释了效率的净改进。较宽的馈线、基板厚度改变引起的导体电流和介质储能变化是物理解释，数据仅能直接分解整副天线的损耗，无法从单端口总功率唯一分配 T 结和每个弯折的局部损耗。

最终 50 Ω 匹配带 **{final['low50']:.3f}–{final['high50']:.3f} GHz**。较旧阵列带宽变化 {change('bandwidth50'):+.3f} GHz，方向性 {change('D'):+.3f} dB，实现增益 {change('G50'):+.3f} dB。主峰 θ={sp['theta_deg']:.0f}°、φ={sp['phi_deg']:.0f}°，2° 角度采样。E/H 面半功率宽度分别为 {sp['E_HPBW_deg']:.2f}°、{sp['H_HPBW_deg']:.2f}°。次级前向局部峰相对各切面主峰，E 面 {sp['E_other_forward_peak_relative_dB']}、H 面 {sp['H_other_forward_peak_relative_dB']} dB；None 表示该采样切面没有额外局部最大值。

## 数值验证与端口近似

{table([lookup[sel['screen']],lookup[sel['source']],hold,lookup[name]],['name','cells','eta','S11_50','D','G50','fmin50','sphere_mean','residual_pct'])}

两套高分辨率几何相同。效率相差 {hf:.3f} 点、方向性 {hd:.3f} dB、实现增益 {hg:.3f} dB，匹配最低点相差 {fr:.3f} GHz。生产工程含结果另存后关闭重开，执行全新求解，再次关闭重开。求解状态 {ver['solver']['state']}。原生复数 S11 在第一次重开、全新求解、最终重开时的最大全带差依次为 {ver['max_S11_complex_delta_on_first_open']:.4g}、{ver['max_S11_complex_delta_on_fresh_solve']:.4g}、{ver['max_S11_complex_delta_on_last_open']:.4g}。最终 CST 原生固定 50 Ω Touchstone 与独立换算的最大复数误差为 {valid['touchstone_max_complex_error']:.3g}。

CST 基线日志指明端口模式求解器在 150 GHz 以常量近似色散材料并忽略截面模态求解中的损耗项。体求解仍保留真实 σ 和 tanδ。PortFrequency140 在相同几何和筛选网格仅将端口模式计算频率移至 140 GHz，继续读取 150 GHz 辐射结果，未移动或扩大物理端口。相对 {portbase['name']}，效率变化 {metric(portbase,port,'eta'):+.3f} 点、S11 变化 {metric(portbase,port,'S11_50'):+.3f} dB、端口吸收变化 {metric(portbase,port,'Pport'):+.6f} W。该诊断的原生日志同时记录 F-Calc 140 和材料常量近似仍在 150 GHz 取值。它只检验端口模式计算频率敏感性，不能代替显式含损耗的独立端口本征模求解。重复求解的差异亦列于 verification.json。

最终球面方向性线性积分均值 {sp['sphere_mean']:.5f}。输入 {final['Pin']:.6f} W，反射 {final['Pout']:.6f} W，接受 {final['Pacc']:.6f} W，辐射 {final['Prad']:.6f} W，Gold {final['Pmetal']:.6f} W，Polyimide {final['Pdiel']:.6f} W，端口非表示模式吸收 {final['Pport']:.6f} W，闭合残差 {final['residual_pct']:.3f}%。两个馈臂四对等位置复电场的最大幅度差 {valid['max_branch_amplitude_difference_dB']:.4f} dB，最大相位差 {valid['max_branch_phase_difference_deg']:.3f}°。数据说明两臂均被激励；此局部场测试不等价于校准的独立前向功率计量。

## 图表及工程限制

"""
    for n in ['Radiation_Efficiency_Comparison','Metal_Loss_Comparison','Dielectric_Loss_Comparison','S11_Comparison','Directivity_Comparison','Realized_Gain_Comparison','Power_Breakdown','Final_3D_Farfield','E_Plane_Comparison','H_Plane_Comparison','Surface_Current']:
        text+=f'\n![{n}](../07_Results_and_Figures/{n}.png)\n'
    text+='\n实际制造前应以 150 GHz 介质及金属薄膜实测值更新模型，并检查关键线宽、基板厚度和蚀刻公差。当前结论适用于本材料假设、有限地板和理想端口激励的全波仿真。\n'
    (DOC/'Efficiency_Optimisation_Report.md').write_text(text,encoding='utf-8')
    guide=f"""# 复现效率优化研究

建议首先从 06_Final_Candidate/{name}/{name}.cst 打开最终模型，保留相邻同名伴随目录。CST Studio Suite 2024 中可查看原生 S1,1、farfield (f=150) [1]、E 场与 surface current。File → Save As 后在独立副本中运行时域求解，可保留交付文件和归档结果。全空间输出使用全局包络积分面与 2° 采样。最终口径的 50 Ω 曲线可使用同目录 CST_50ohm.s1p。

## 脚本和数据

08_Automation 中的 Array_Build、Array_Run、Array_Audit、Array_Results_Extraction 和 Reference_ModelHistory 来自原工程。Efficiency_CST.py 从 01_Baseline_Copy 的原生模型及建模历史创建独立项目，调整参数，调用 CST 接口求解并复用原生结果导出。运行时勿指向原 07 工程写入。新参数及理想化标签保存在每个 case 的 parameters.json，completed.json 只在求解成功并导出角度数据后生成。

在相同目录结构的研究副本中，从 08_Automation 运行。CST 使用安装目录下 Opera/code/bin/python.exe，数值处理使用 NumPy 2 和 Matplotlib 环境。CST 工程与导出曲线的来源为本地完整工程。要从头重现，应使用新的研究副本并仅预置 01_Baseline_Copy 和 08_Automation、其余阶段空目录；已有 completed.json 的 case 会被复用。原单贴片和旧阵列三模型对比仍读取 Project_Final 下相邻的已验证结果。

1. 用 CST 的 Python 运行 Check_Baseline.py、Efficiency_CST.py，核对备份并顺序求解 A–D。
2. 用同一解释器运行 Efficiency_Study.py，完成馈线、厚度、重新匹配、最终细网格及独立网格、140 GHz 端口模式敏感性实验。
3. 用同一解释器运行 Efficiency_Edge_Fields.py、Efficiency_Verify.py。前者从已存监视器提取边缘场；后者另存最终文件、关闭重开、复算并重新读取结果。
4. 用数值分析环境依次执行 Efficiency_Analysis.py 与 Efficiency_Report.py，重建 07_Results_and_Figures 和 09_Documentation。CSV 的布局由脚本定义。All_Candidates.csv 含不满足匹配要求的筛选结果，不能作为可用设计排序直接采用。

## 检查入口

- 01_Baseline_Copy/Native_Provenance.json：备份散列及 cst.results 直接读取的基线功率。
- 06_Final_Candidate/verification.json：两次重开、复算状态、端口、参数、全部远场监视器及 S11 差值。
- 07_Results_and_Figures/Validation.json：独立 50 Ω 校核、功率、球面积分、支路幅相和趋肤深度。
- 02–06 各案例的 .cst、同名结果目录、原生曲线、farfield 角度表与求解日志。最终 Project 保存 130–170 GHz 扫频，只有离散 farfield monitor 对应独立远场值。
"""
    (DOC/'Reproduction_Guide.md').write_text(guide,encoding='utf-8')
if __name__=='__main__':main()

