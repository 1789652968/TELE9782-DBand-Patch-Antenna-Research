"""Write engineering reports from the independently reproduced 4x4 and 1x2 data."""
from pathlib import Path
import json
import shutil
import hashlib
import csv
import re
import sys
from Extract_Results import ROOT,BASE,RESULTS,COMP,read,write_json,write
V=RESULTS/'Verification';D=ROOT/'05_Documentation'
def main():
    d=read(V/'Final_Metrics.json');a=d['baseline'];b=d['array4x4'];q=d['feed_probes']
    m=read(V/'Mesh_Selection.json');selection=read(V/'Selection.json')
    rawfolder=ROOT/'01_CST_Project/Final_4x4'
    c=read(rawfolder/'parameters.json');c0=read(ROOT/'01_CST_Project/Initial_4x4/parameters.json')
    assert all(x['solver_state']=='SUCCESS' for x in m['meshes'])
    assert min(a['radiation_efficiency_pct'],b['radiation_efficiency_pct'])>0
    assert q['connected_patch_probes']==16 and q['minimum_Ez_Vm']>0
    assert (V/'Native_Database_Readback.json').is_file()
    names=[
        ('Patch count','patch_count','d'),('Radiation efficiency (%)','radiation_efficiency_pct','.3f'),('Total efficiency, 50 Ω (%)','total_efficiency_50ohm_pct','.3f'),
        ('150 GHz S11, 50 Ω (dB)','s11_50ohm_dB','.3f'),('Directivity (dBi)','directivity_dBi','.3f'),('Peak realized gain, 50 Ω (dBi)','peak_realized_gain_50ohm_dBi','.3f'),
        ('+Z realized gain, 50 Ω (dBi)','plus_z_realized_gain_50ohm_dBi','.3f'),('Beam offset θ (°)','beam_theta_deg','.1f'),('Peak azimuth φ (°)','beam_phi_deg','.1f'),
        ('E-plane HPBW (°)','e_plane_hpbw_deg','.2f'),('H-plane HPBW (°)','h_plane_hpbw_deg','.2f'),('−10 dB band containing 150 GHz (GHz)','bandwidth_10dB_GHz','.3f'),
        ('Main board width × length (mm)','shape',''),('Footprint bounding box incl. launch (mm)','box',''),('T-junctions','T_junctions','d'),('Centreline total, incl. launch (mm)','feed_total_centerline_mm','.3f'),
        ('Port to each inset tip (mm)','port_to_inset_centerline_mm','.3f'),('Mesh cells','mesh_cells',',d'),('CST solver elapsed (s)','reported_solver_calculation_seconds','.0f')]
    def fmt(z,k,syntax):
        if k=='shape':return f"{z['board_width_mm']:.3f} × {z['board_length_mm']:.3f}"
        if k=='box':return f"{z['bounding_width_mm']:.3f} × {z['bounding_length_mm']:.3f}"
        return format(z[k],syntax) if z[k] is not None else '—'
    table='| Metric at 150 GHz | Optimised 1×2 | Basic 4×4 |\n|---|---:|---:|\n'+'\n'.join(f'| {n} | {fmt(a,k,s)} | {fmt(b,k,s)} |' for n,k,s in names)
    power='| CST term | 1×2 (mW) | 4×4 (mW) | 1×2 (% accepted) | 4×4 (% accepted) |\n|---|---:|---:|---:|---:|\n'
    for title,key in [('Accepted','accepted_W'),('Radiated','radiated_W'),('Gold','metal_loss_W'),('Polyimide','dielectric_loss_W'),('Port absorption, native signed entry','port_absorption_W'),('Closure residual','balance_residual_W')]:
        power+=f"| {title} | {a[key]*1000:.3f} | {b[key]*1000:.3f} | {a[key]/a['accepted_W']*100:.3f} | {b[key]/b['accepted_W']*100:.3f} |\n"
    mesh='| Case | Cells | ηrad (%) | S11 (dB) | Directivity (dBi) | +Z gain (dBi) | Offset (°) |\n|---|---:|---:|---:|---:|---:|---:|\n'
    for z in m['meshes']:
        mesh+=f"| {z['design']} | {z['mesh_cells']:,} | {z['radiation_efficiency_pct']:.3f} | {z['s11_50ohm_dB']:.3f} | {z['directivity_dBi']:.3f} | {z['plus_z_realized_gain_50ohm_dBi']:.3f} | {z['beam_theta_deg']:.1f} |\n"
    lic=read(V/'License_Constraint.json')
    license_note=f"CST rejected the attempted 26/39 grid before time stepping because the installed license caps the model at {lic['maximum_mesh_cells']:,} mesh cells. The successful 4×4 resolution and mesh-sensitivity data above reflect that constraint. They support comparison of these validated models, with a finer-grid extrapolation beyond the licensed limit still untested."
    trials='| Screen case | ηrad (%) | S11 at 150 GHz (dB) | Best S11 (dB) | Frequency of best match (GHz) |\n|---|---:|---:|---:|---:|\n'
    for z in selection['screen_trials']:
        trials+=f"| {z['design']} | {z['radiation_efficiency_pct']:.3f} | {z['s11_50ohm_dB']:.3f} | {z['best_s11_50ohm_dB']:.3f} | {z['best_match_freq_GHz']:.3f} |\n"
    port_en=''
    port_cn=''
    if b['port_absorption_W']<0:
        no_port=b['balance_residual_W']+b['port_absorption_W']
        port_en=f"The native 4×4 port-absorption term is signed at {b['port_absorption_W']*1e3:.3f} mW. A passive port cannot dissipate negative power. We retain the solver value as a numerical port-balance term. The closure difference from radiated, metal and dielectric terms alone is {no_port*1e3:.3f} mW ({100*no_port/b['accepted_W']:.3f}% of accepted power)."
        port_cn=f"CST 的 4×4 Port Absorption 原始项为 {b['port_absorption_W']*1e3:.3f} mW。无源端口的物理耗散应为非负，因此此值按带符号的数值平衡项保留。从接受功率扣除辐射、金属和介质项后的差额为 {no_port*1e3:.3f} mW。"
    dc=b['radiation_efficiency_pct']-a['radiation_efficiency_pct'];dd=b['directivity_dBi']-a['directivity_dBi'];dg=b['peak_realized_gain_50ohm_dBi']-a['peak_realized_gain_50ohm_dBi'];dz=b['plus_z_realized_gain_50ohm_dBi']-a['plus_z_realized_gain_50ohm_dBi']
    dm=b['metal_loss_pct_accepted']-a['metal_loss_pct_accepted'];dp=b['dielectric_loss_pct_accepted']-a['dielectric_loss_pct_accepted'];dl=b['port_absorption_pct_accepted']-a['port_absorption_pct_accepted']
    dbw=b['bandwidth_10dB_GHz']-a['bandwidth_10dB_GHz']
    dmatching=[f"{k} = {z:.5g}" for k,z in selection['matching_changes'].items()]
    changes='The retained geometry includes these basic matching settings. '+', '.join(dmatching)+'.' if dmatching else 'The initial geometry met the screening match requirement, so its physical dimensions were kept.'
    intervals=f"The contiguous matched band ran from {b['band_lower_GHz']:.3f} to {b['band_upper_GHz']:.3f} GHz." if b['band_lower_GHz'] is not None else 'There is no contiguous −10 dB interval containing 150 GHz.'
    match='The refined result meets the −10 dB comparison threshold.' if b['s11_50ohm_dB']<=-10 else 'The refined result misses −10 dB at the working point, so mismatch affects this particular comparison.'
    criterion='The final two grids met the study’s screening tolerances for efficiency, gain, beam and matching.' if m['comparable_mesh_pair'] else 'The final two meshes showed unresolved sensitivity under the predeclared tolerances. Treat exact numbers as mesh-dependent and use the displayed spread.'
    report=f"""# Comparative study of 1×2 and 4×4 D-band patch arrays

## 1. Objective

Test whether a conventional 16-patch array provides enough usable gain at 150 GHz to justify changes in losses, matched bandwidth, board size, and feed complexity relative to a validated two-element array.

## 2. Design configurations

The optimised 1×2 uses the saved first-round delivery model. The 4×4 uses identical patch orientation with 1.12 mm X pitch and 1.25 mm Y pitch. A single-layer corporate network splits first between rows and then into patch pairs. Side entry provides clearance between the feed and radiating edges, and all sixteen ideal centreline paths are equal. The off-aperture feed is physically asymmetric. Both arrays use the same nominal 75 μm Polyimide (εr = 3.5, tanδ = 0.0027) and 2 μm Gold (σ = 4.561 × 10⁷ S/m).

{changes}

{trials}

## 3. Simulation conditions

CST Studio Suite 2024, hexahedral time-domain solver, 130–170 GHz sweep, open boundaries, −60 dB decay criterion, single waveguide excitation. The 4×4 uses the X-min port; the 1×2 uses Y-min. Results use the measured native impedance and the same 50 Ω reference. No fresh solve was applied to the archived 1×2.

{mesh}

{criterion} {license_note} The final geometry was saved with its native companion and independently re-opened. The native and converted 50 Ω S1P signals agreed within {b['touchstone_max_complex_delta']:.2e} in complex Γ. The mean linear sphere directivity was {b['directivity_sphere_mean']:.5f}, residual accepted power was {b['balance_residual_pct_accepted']:.3f}%, and recorded 150 GHz radiation efficiency agreed with Prad/Pacc within {abs(b['radiation_efficiency_minus_monitor_pp']):.3g} percentage points. Sixteen complex Ez probes were present, from {q['minimum_Ez_Vm']:.1f} to {q['maximum_Ez_Vm']:.1f} V/m (spread {q['magnitude_spread_dB']:.2f} dB). These local fields and surface current demonstrate excitation on the connected routed network. Their phase and magnitude include coupling and reflected waves. The largest phase deviation from the circular mean was {q['maximum_abs_relative_phase_deg']:.1f}°. [Field samples](../02_Simulation_Results/Farfield/Patch_Feed_Probes_150.csv) · [Native readback](../02_Simulation_Results/Verification/Native_Database_Readback.json)

## 4. Performance comparison

{table}

[Complete numerical table](../03_Comparison/Array_1x2_vs_4x4_Comparison.csv) · [E/H patterns](../03_Comparison/Comparison_Figures/E_H_Planes.png) · [3D directivity](../03_Comparison/Comparison_Figures/4x4_3D_Directivity.png) · [3D gain at 50 Ω](../03_Comparison/Comparison_Figures/4x4_3D_Realized_Gain_50ohm.png)

## 5. Radiation efficiency

The change in ηrad is {dc:+.3f} percentage points. CST absolute powers are shown at their native excitations. The accepted-power fractions provide the meaningful loss comparison across different matches.

{power}

## 6. Feed network loss

The gold and dielectric accepted-power fractions change by {dm:+.3f} and {dp:+.3f} percentage points. {port_en} The routed line is longer and contains more junctions and stepped transformers. The full-structure Gold and Polyimide totals include the radiator, ground and feed, and support a net loss comparison. They do not resolve feed-only dissipation. The local current map locates excitation and concentration without partitioning loss by component. [Power breakdown](../03_Comparison/Comparison_Figures/Power_Absolute_and_Normalized.png) · [Surface current](../03_Comparison/Comparison_Figures/4x4_Surface_Current_150.png)

## 7. Directivity and gain

The change in peak directivity is {dd:+.3f} dB. The corresponding peak realized gain and fixed-axis gain changes are {dg:+.3f} and {dz:+.3f} dB. These gains account for dissipation and mismatch. The reported direction was sampled every {b['angular_step_deg']:g}°; the cut HPBW values refer to the strongest forward peak in each named cut. A cut peak and the global maximum may point in different directions.

## 8. Bandwidth comparison

{match} {intervals} The working-point bandwidth changes by {dbw:+.3f} GHz. The lower and upper band edges are obtained by interpolation on the native 1001-point complex sweep after converting to 50 Ω. [S11 trace](../03_Comparison/Comparison_Figures/S11_50ohm.png)

## 9. Complexity trade-off

Compare fifteen split junctions and {b['feed_total_centerline_mm']:.3f} mm of line centreline with one junction and {a['feed_total_centerline_mm']:.3f} mm. The narrower transformers and repeated inset gaps impose alignment and etch requirements. Both are single-layer layouts. The recorded mesh counts and times are included for resource context; wall time also depends on work-station conditions and solver grid.

## 10. Discussion

These measurements compare two realisable simulation configurations. The aperture, feed, board and port orientation differ, so the observed changes combine more than element count. A report may treat efficiency, matched bandwidth, and structure simplicity as separate considerations from beam concentration and realized gain. The assumed Gold and Polyimide properties and open-boundary model are common to this pair. Fabricated samples and per-component feed loss measurements are future evidence.

## 11. Conclusion

At 150 GHz, the 1×2 achieves {a['radiation_efficiency_pct']:.2f}% radiation efficiency and {a['peak_realized_gain_50ohm_dBi']:.2f} dBi peak realized gain. The 4×4 achieves {b['radiation_efficiency_pct']:.2f}% and {b['peak_realized_gain_50ohm_dBi']:.2f} dBi. The 1×2 remains an established course delivery for broadly matched operation and a compact implementation. The result supports using the complete performance table to select a design when realized gain or beam width dominates. The accompanying 4×4 results quantify what the change in aperture achieves and what it costs for this routed design.
"""
    (D/'Comparative_Study_Report.md').write_text(report,encoding='utf-8')
    summary=f"""# 150 GHz 对比摘要

CST 2024 完成真实求解。优化 1×2 的辐射效率为 {a['radiation_efficiency_pct']:.2f}%，4×4 为 {b['radiation_efficiency_pct']:.2f}%，变化 **{dc:+.2f} 个百分点**。4×4 相对 1×2 的 Directivity、峰值 Realized Gain、+Z Realized Gain 变化为 **{dd:+.2f}、{dg:+.2f}、{dz:+.2f} dB**。150 GHz 的 −10 dB 匹配带宽变化为 {dbw:+.2f} GHz。以下 S11 和增益统一 50 Ω。

{table}

## 损耗和结构

金属、介质损耗占接受功率的比例分别变化 {dm:+.2f}、{dp:+.2f} 个百分点。{port_cn}下表保留绝对值和比例。4×4 有更大的板、{b['T_junctions']} 个 T 结及更长的等几何路径。全结构积分损耗包含辐射体和馈线，馈电网络贡献属于结构解释，单靠这些总量无法定出馈线自身损耗。

{power}

## 用于课程报告

按此 4×4 与已验证 1×2 的横向数据进行比较。1×2 是原课程交付基线，4×4 提供阵列规模、方向性与损耗之间的真实对照。应当同时引用 50 Ω 的峰值和 +Z Gain、匹配带宽与网格敏感性。若侧重孔径增益，使用表中相应列解释 4×4 的得失。效率的变化不能推广为单元数的独立效应。

{criterion} 本机 CST 的许可证上限为 100 万单元，26/39 设置在求解前被拒绝并保留原生错误记录。下方为许可范围内的实际网格复核。

[英文研究报告](../05_Documentation/Comparative_Study_Report.md) · [全指标 CSV](Array_1x2_vs_4x4_Comparison.csv) · [图表](Comparison_Figures/)
"""
    (COMP/'Comparison_Summary.md').write_text(summary,encoding='utf-8')
    print('REPORTS COMPLETE')
if __name__=='__main__':main()

