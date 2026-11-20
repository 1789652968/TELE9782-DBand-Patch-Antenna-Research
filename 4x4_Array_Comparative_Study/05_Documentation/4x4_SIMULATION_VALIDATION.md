# 4×4 CST 数值验证

## 求解状态和网格重复性

最终原生 CST 2024 Model.log 记录时域求解于 2026-11-20 16:25:07（本地日志 +1100）完成，Total simulation time 1149 s。完成后 Python 导出连接丢失，重开保存的工程后恢复原生导出（80.6 s，仅导出）。后续保存的 Final_4x4 保留该成功求解的原生结果，另执行只读重开确认 1D 数据一致。重开读取和网格复核均有记录。

| 阶梯输入网格 | Cells | Radiation Efficiency | Directivity | S11 50 Ω | +Z Gain 50 Ω | θpeak |
|---|---:|---:|---:|---:|---:|---:|
| 20/30 筛选 | 686,760 | 74.140% | 12.416 dBi | −4.161 dB | 7.929 dBi | 6° |
| 22/32 粗终验 | 764,940 | 74.328% | 12.025 dBi | −4.107 dB | 7.636 dBi | 6° |
| 23/33 交付 | 781,200 | 74.356% | 12.058 dBi | −4.114 dB | 7.662 dBi | 6° |

两级细网格差为 +0.0284 个百分点、+0.0335 dB Directivity、−0.0073 dB S11、+0.0263 dB +Z Gain。粗筛的 Directivity 与最终仍有约 0.36 dB 差异。26/39 网格在求解前触发 1,000,000-cell 的许可证上限。两级细网格支持在现有许可条件下的有限敏感性检查，更精细网格和外推仍未开展。

[Mesh Sensitivity](../02_Simulation_Results/Verification/Mesh_Sensitivity.csv) · [被拒网格日志](../Trials/Refined_4x4/Model.log) · [交付日志](../Trials/Final_4x4/Model.log) · [重开原生读回](../02_Simulation_Results/Verification/Native_Database_Readback.json)

## 端口、功率和远场

- 单个 X-min 端口的原生模态参考约为 52.613 Ω。日志记录 150 GHz 色散材料端口模式采用常量近似并忽略端口模式损耗项，模型内部仍使用有损材料。CST 直接 50 Ω Touchstone 与独立重归一的最大复数 Γ 差 6.92×10⁻⁸（1001 点）；单独的端口位置/模式敏感性研究未开展。
- Radiation Efficiency = 220.550/296.613 = 74.356%，与 CST farfield 效率监视值一致。CST 带符号端口项保留后，功率闭合残差为 0.7215% Accepted。原生远场 Realized Gain 独立重归一与派生峰值差约 0.00044 dB。
- 150 GHz 球面积分的线性 Directivity 均值为 1.02146（相对理想值 1 约 +2.15%）。最终角度网格为 2°，因此主波束 θ=6°、φ=266° 是采样峰值，不能视为亚角度精度。全远场 Peak Gain 8.640 dBi；固定 +Z Gain 7.662 dBi。
- CST 表面电流和每个 inset 前的 16 个复数 Ez 样点均保留。|Ez| 约 3443–8421 V/m，相差 7.77 dB，阶段内相对 circular mean 最大偏差 18.59°。几何路径等长和实际场幅相是两项不同证据。该口附近的净场含反射与耦合，不能作为独立行波的分支功率或相位标定。
- 本研究结果来自仿真。报告以有限网格、基本匹配测试和 150 GHz 工作点为条件，保留对端口模式、制造和复杂馈电机理的进一步验证空间。

[16 个复数探针](../02_Simulation_Results/Farfield/Patch_Feed_Probes_150.csv) · [原生 S1P](../Native_Exports/CST_50ohm.s1p) · [原生全远场](../Native_Exports/Farfield_150_Sphere.txt) · [Power Balance](4x4_POWER_LOSS_ANALYSIS.md)
