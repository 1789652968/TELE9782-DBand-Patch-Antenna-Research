# 4×4 设计、匹配与 CST 求解工作流

## 研究范围与实际设计

以已重开复算的 82.99% 1×2 为基准，保留贴片尺寸、基板厚度与材料参数，增加至四行四列。有限的匹配试验用于评估基本 Corporate Feed Network，研究预算覆盖几何验证、四个匹配对照与网格复核。结果适用于基本 4×4 与已优化 1×2 两个实施方案。

| 几何或设置 | 最终 4×4 |
|---|---|
| 单贴片、中心距 | W 0.667、L 0.5148 mm，X 1.12、Y 1.25 mm |
| 基板、地板 | 主板 X [−3.12, 2.40]、Y [−3.040, 2.4924] mm，含侧馈边界框 6.020 × 5.5324 mm |
| 材料 | Polyimide 0.075 mm，εr 3.5，tanδ 0.0027，150 GHz 材料参考。Gold 0.002 mm，σ 4.561 × 10⁷ S/m |
| Z 范围 | Ground [−0.002, 0]，Polyimide [0, 0.075]，顶层信号 [0.075, 0.077] mm |
| Feed / inset | 主线宽 0.1688 mm，各分路变压段 0.1031 × 0.280 mm，inset 0.165 mm，双侧缝各 0.020 mm |
| 单输入 | X-min 波导端口，朝 +X，X −3.620 mm，Y −0.865 ± 0.250 mm，Z −0.002 至 0.450 mm |
| 端口与参考阻抗 | 1 个计算模式，150 GHz 原生模态参考约 52.613 Ω，对比统一重归一到 50 Ω |
| Feed 几何 | 每路 Port-to-Inset 7.9476 mm，总中心线 41.7016 mm，15 个 T-junction |

[实际尺寸](../Design/Geometry_Parameters/Final_4x4/parameters.json) · [几何布局](../Design/Geometry_Parameters/Final_4x4/layout.json) · [CST Model History](../Design/Geometry_Parameters/Final_4x4/ModelHistory.json)

## 实际执行的建模步骤

1. 由 Python 读取 1×2 参数与已核查的 CST 模板。CST History 创建 Polyimide 主板和侧馈 launch，背面放置并并接 Gold Ground。
2. 根据四行四列的坐标创建 16 个同极化矩形贴片，在每个贴片馈入处减去两个 inset 缝。
3. 单输入干线分配至两个行组，再分至四行，随后在每行分左右贴片对，最后分为每行四个贴片。每级按等几何路径布线，15 个 T 分支均采用成对阻抗变化段。侧馈入口及离开孔径的馈电线使完整模型具有非对称性。
4. 布局脚本检查线间净距、相邻贴片间距、各贴片只接自己的 inset，以及所有导体都能从输入端到达。CST 按接触关系 Boolean union 顶层信号，背面 Gold 与顶层由基板隔开。
5. 将原模板的 Y-min 单端口旋至 X-min。X-min 为 open，其余面为 expanded open，四层 Convolution PML。设置时域六面体 PBA、130–170 GHz、1001 点以及 −60 dB 衰减准则。150 GHz 保存远场、E-field、H-field 和 Surface Current；145、154 GHz 保存附加远场监视点。
6. 从 CST 已完成的求解器数据导出 native S 参数、模态阻抗、Power Accepted、Radiated、Gold 与介质损耗、Port Absorption、150 GHz 全球 Directivity 和 Realized Gain。脚本以 2° 采样读取原生 E/H 切面所需方位和法线值，以网络阻抗变换核对 CST 直接导出的 50 Ω Touchstone。

[建模脚本](../04_Automation/Build_4x4.py) · [求解与导出脚本](../04_Automation/Run_4x4.py) · [最终 CST 求解日志](../Trials/Final_4x4/Model.log)

## 实际匹配试验

| 试验 | 修改与意图 | 150 GHz S11，50 Ω | 扫频最低 S11，50 Ω |
|---|---|---:|---:|
| Initial | 双臂 Corporate Feed，输入主线宽 0.1688 mm | −2.349 dB | −10.840 dB @ 139.76 GHz |
| Stepped feed | 距端口 0.170 mm 开始，长 0.140 mm、宽 0.045 mm 的窄截面，尝试变换入口阻抗 | −4.161 dB | −9.119 dB @ 163.12 GHz |
| Open stub | 入口偏移 0.578 mm，长 0.238 mm、宽 0.065 mm 的开路并联支节，尝试补偿无功分量 | −3.003 dB | −15.220 dB @ 162.96 GHz |
| Quarter-wave section | 额外 0.554 mm 主线、0.310 × 0.690 mm 变换段及 0.500 mm launch，以近似传输线计算设置匹配 | −1.772 dB | −11.314 dB @ 145.80 GHz |

均有 CST 成功的试验导出。开路支节和额外变换段在其他频率出现较好的 S11 谷值，150 GHz 的结果较弱。阶梯线在这四例中工作频点 S11 和 Total Efficiency 最佳，故继续做两级网格检查。最终 150 GHz S11 为 −4.114 dB，输入阻抗约 11.73 + j4.69 Ω，扫频最低点仍高于 −10 dB。更高的 26/39 网格被许可证拒绝，原生错误保留。最终工程从 23/33 成功模型复制并保留同名结果。其首次 Python 导出中断，通过重开恢复原生后处理。

[试验 CSV](../02_Simulation_Results/Verification/Matching_Trials.csv) · [所有试验原生导出与日志](../Trials/) · [数值验证](4x4_SIMULATION_VALIDATION.md)

## 复现入口

下载 [原生归档](../Artifact_Manifest.md)，保持 Final_4x4.cst 与同名目录并排。先用保存结果独立核对数值。需要重新运行时，把工程及同名目录复制至独立可写目录，按保存的 23/33 网格设置运行 CST 2024。[复现与证据来源](Reproduction_Guide.md)
