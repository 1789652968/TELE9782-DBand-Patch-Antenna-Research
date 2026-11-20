# 演讲后研究日志

阶段顺序来自带日期的 PPT、原阵列 Execution Log、Round 1 / 2 求解脚本、原生 Model.log、CSV 和重开记录。PPT 标注 2026-11-17。并行试验之间的精确先后以各自日志为准，部分历史操作的具体时间未记录。

## Stage 0 · Presentation baseline

CST 2024 的单端口、均匀 microstrip launch、Gold / Polyimide 矩形 inset-fed patch 针对 150 GHz TM₁₀。理论初值 W=0.666、L=0.520 mm，最终 W=0.667、L=0.513 mm，基板 40 μm，Gold 2 μm。Open boundaries、Hex/PBA time-domain、130–170 GHz、13 个远场 monitor、−60 dB decay 和 global enclosing surface 构成演讲验证。150 GHz 的 Directivity 7.460 dBi，Realized Gain 5.804 dBi，ηrad 71.55%。教师反馈来自组内转述，效率偏低成为后续研究动机。[历史基线](01_Presentation_Baseline/Baseline_Summary.md)

## Stage 1 · 原始 1×2 阵列与性能核查

先读取原单贴片几何与网格基线，将单贴片放到阵列大板上形成 GroundControl，以区分 finite-ground 与阵列作用。随后求解单端口、对称 T 分支馈电的两片阵列，筛选 feed、transformer、inset 和五种 spacing。脚本与执行日志将 Transformer 标为早期筛选点，Refined 用于交付前网格比较。Final50 设显式参考，再将复数 S11 与原生 Touchstone 独立重归一，保存交付后重开复算。表面电流、功率和远场积分用于解释方向图。

同 50 Ω 口径下，原单贴片为 71.553% / 7.460 dBi，扩大地板单贴片为 73.429% / 7.963 dBi，原 1×2 为 71.981% / 8.843 dBi。原阵列的总效率 71.862%，S11 −27.802 dB，峰值实现增益 7.408 dBi，带宽 4.107 GHz。Directivity 的优势显著，接受功率中的辐射比例改善有限。[原阵列执行日志](Project_Final/07_Array_1x2/05_Documentation/Execution_Log.md) · [原阵列报告](Project_Final/07_Array_1x2/05_Documentation/Final_Report_Results.md) · [共同参考对比](Project_Final/07_Array_1x2/03_Comparison/Common50_150GHz.csv)

## Stage 2 · 第一轮辐射效率优化

以接受功率为分母，原交付阵列辐射、金属、介质、端口吸收与闭合差依次为 71.981%、17.085%、8.241%、2.349%、0.345%。在同一粗网格用 Gold / lossy PI、PEC / lossy PI、Gold / lossless PI、PEC / lossless PI 去耦，ηrad 依次为 74.208%、87.789%、80.890%、96.527%。这组理想化诊断支持优先处理金属损耗，PEC 结果仅用于机理对照，且各对照改变场分布，不能把增量线性相加。

F1_ShortArms 缩短 T 结至馈点路径约 1.039 → 0.873 mm，spacing 缩至 1.12 mm 并移动 junction。后续加宽变压线、倒角和 T 结试验降低部分损耗，S11 也发生变化，未全部保留。基板按 30、50、60、75 μm 试验并调整 feed/transformer/inset 与贴片长度。H75 未重调时 86.003% 但 S11 −9.100 dB，H75_Length 重调改善匹配。3 μm 金与 2 μm 效率相近，5 μm 在不同实际网格单元数下未显示稳定收益。最终保留 75 μm 原 Polyimide 和 2 μm 真实 Gold。

Fine、IndependentMesh、重开交付复算分别 83.438%、83.519%、82.994%。后者的功率预算为金属 7.954%、介质 5.569%、端口 3.126%、闭合差 0.356%，全空间线性 Directivity 均值约 1.001。与原交付阵列相比，金属损耗降低最明显。重开文件达到总效率 81.366%、S11 −17.074 dB、Directivity 9.140 dBi、峰值实现增益 8.244 dBi、+Z 7.763 dBi 和带宽 13.515 GHz。主瓣由约 2° 变为 16°，形成第二轮问题。[第一轮报告](Project_Final/08_Efficiency_Optimisation/09_Documentation/Efficiency_Optimisation_Report.md) · [全部候选](Project_Final/08_Efficiency_Optimisation/07_Results_and_Figures/All_Candidates.csv) · [第一轮复现](Project_Final/08_Efficiency_Optimisation/09_Documentation/Reproduction_Guide.md)

## Stage 3 · 第二轮多目标试验

用同网格控制和独立验证分离 substrate、patch、feed、spacing、ground、+Y 刚性平移、rear/parasitic 结构、端口 F-Calc 与公差。导体保留真实 Gold。脚本先筛选可调用 CST 模型，按 ηrad、ηtotal、S11、带宽、峰值与法线增益、方向性和偏角比较前沿。离开匹配区或数值门槛的候选仍保留。H110 的粗网格 ηrad 约 88.02%，S11 约 −8.48 dB；加深 inset 的 H110DeepInset 未把这一趋势转成合格的高效率方案。最终数值限制体现为材料/端口残损与匹配、带宽、方向图之间的共同约束，在已测几何范围内无稳定 90% 解。

总计 39 个 screen、4 套各 3 次 production / dense / fresh、15 次 sensitivity（含标称）、2 次 port_numerical_check，合计 68 条，28 张汇总图。用最终验证记录复核各数。场图和端口测试解释 16° 主要位于 E-plane；双支路样本未显示足以单独解释偏转的相差。离散扫描验证 ground / launch / 辐射组合的敏感性，并采用 +Y 平移做广侧夹逼。CST 端口 F-Calc 140/150 对最高效率候选的粗网格 ηrad 影响约 +0.028 个百分点。积分和等参考波形同时保留。重启截断的 ShiftNull75 S1P 从成功保存的原生工程恢复，1001 个复数点独立核对。[全部试验](Project_Final/09_Multiobjective_Optimisation/08_Results_and_Figures/All_Optimisation_Trials.csv) · [最终报告](Project_Final/09_Multiobjective_Optimisation/10_Documentation/Final_Optimisation_Report.md) · [Beam Squint 诊断](Project_Final/09_Multiobjective_Optimisation/10_Documentation/Beam_Squint_Diagnosis.md) · [重开验证](Project_Final/09_Multiobjective_Optimisation/07_Final_Candidates/Verification_Results.json)

## Stage 4 · 交付候选

ShiftBracket85 加厚基板至 85 μm、调整贴片和馈线并平移 +Y 0.159 mm，得到 85.49% / 12°，增益与带宽低于上一轮。H085 使用 85 μm、0.5102 mm 贴片长度与 0.1913 mm feed，84.96% / 19–20°，峰值增益和带宽最好于三项所选角色。ShiftNull75 保持 75 μm、沿 +Y 平移 0.1876 mm，83.38% / 4°，S11 −20.70 dB；154 GHz 的偏角达 32°。WideGround 也经过三次高分辨率验证，选择记录保留它的完整链。[候选比较](DESIGN_COMPARISON.md)

## Stage 5 · 课程主交付

保留第一轮 82.99% 工程。85.49% 相对提升 2.50 个百分点，但峰值实现增益下降约 0.557 dB、+Z 下降约 0.218 dB、带宽少约 4.798 GHz；12° 虽改善，仍离法线有距离。H085 的 +Z 持平而偏转增加。ShiftNull75 在工作点校正偏角的同时降低 +Z 和带宽，并有频率限制。判断综合了指标、工作点与频带的差异，所有角色和弃选数据均供正式报告比较。[推荐记录](Project_Final/09_Multiobjective_Optimisation/07_Final_Candidates/Recommended_Project.json)

## 原生日志锚点

以下为各模型的原生日志中最后一次写入 parametric 1D results 的工作站时间。PPT 标注 11 月 17 日。原单贴片为 2026-11-11 08:43:41，原阵列为 2026-11-19 02:50:12，第一轮交付为 2026-11-19 13:21:33，第二轮 ShiftNull75 交付复算为 2026-11-19 20:34:16。它们是记录时间节点。各阶段的开始或会面时间以当时材料为准。
