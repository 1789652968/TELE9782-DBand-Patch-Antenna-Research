# 150 GHz 对比摘要

CST 2024 完成真实求解。优化 1×2 的辐射效率为 82.99%，4×4 为 74.36%，变化 **-8.64 个百分点**。4×4 相对 1×2 的 Directivity、峰值 Realized Gain、+Z Realized Gain 变化为 **+2.92、+0.40、-0.10 dB**。150 GHz 的 −10 dB 匹配带宽变化为 -13.51 GHz。以下 S11 和增益统一 50 Ω。

| Metric at 150 GHz | Optimised 1×2 | Basic 4×4 |
|---|---:|---:|
| Patch count | 2 | 16 |
| Radiation efficiency (%) | 82.994 | 74.356 |
| Total efficiency, 50 Ω (%) | 81.366 | 45.522 |
| 150 GHz S11, 50 Ω (dB) | -17.074 | -4.114 |
| Directivity (dBi) | 9.140 | 12.058 |
| Peak realized gain, 50 Ω (dBi) | 8.244 | 8.640 |
| +Z realized gain, 50 Ω (dBi) | 7.763 | 7.662 |
| Beam offset θ (°) | 16.0 | 6.0 |
| Peak azimuth φ (°) | 90.0 | 266.0 |
| E-plane HPBW (°) | 88.22 | 22.50 |
| H-plane HPBW (°) | 48.06 | 25.50 |
| −10 dB band containing 150 GHz (GHz) | 13.515 | 无 |
| Main board width × length (mm) | 2.500 × 1.500 | 5.520 × 5.532 |
| Footprint bounding box incl. launch (mm) | 2.500 × 2.000 | 6.020 × 5.532 |
| T-junctions | 1 | 15 |
| Centreline total, incl. launch (mm) | 2.590 | 41.702 |
| Port to each inset tip (mm) | 1.718 | 7.948 |
| Mesh cells | 574,464 | 781,200 |
| CST solver elapsed (s) | 352 | 1149 |

## 损耗和结构

金属、介质损耗占接受功率的比例分别变化 +5.92、+5.79 个百分点。CST 的 4×4 Port Absorption 原始项为 -0.939 mW。无源端口的物理耗散应为非负，因此此值按带符号的数值平衡项保留。从接受功率扣除辐射、金属和介质项后的差额为 1.201 mW。下表保留绝对值和比例。4×4 有更大的板、15 个 T 结及更长的等几何路径。全结构积分损耗包含辐射体和馈线，馈电网络贡献属于结构解释，单靠这些总量无法定出馈线自身损耗。

| CST term | 1×2 (mW) | 4×4 (mW) | 1×2 (% accepted) | 4×4 (% accepted) |
|---|---:|---:|---:|---:|
| Accepted | 492.233 | 296.613 | 100.000 | 100.000 |
| Radiated | 408.523 | 220.550 | 82.994 | 74.356 |
| Gold | 39.154 | 41.164 | 7.954 | 13.878 |
| Polyimide | 27.414 | 33.698 | 5.569 | 11.361 |
| Port absorption, native signed entry | 15.388 | -0.939 | 3.126 | -0.317 |
| Closure residual | 1.754 | 2.140 | 0.356 | 0.721 |


## 用于课程报告

按此 4×4 与已验证 1×2 的横向数据进行比较。1×2 是原课程交付基线，4×4 提供阵列规模、方向性与损耗之间的真实对照。应当同时引用 50 Ω 的峰值和 +Z Gain、匹配带宽与网格敏感性。若侧重孔径增益，使用表中相应列解释 4×4 的得失。效率的变化不能推广为单元数的独立效应。

The final two grids met the study’s screening tolerances for efficiency, gain, beam and matching. 本机 CST 的许可证上限为 100 万单元，26/39 设置在求解前被拒绝并保留原生错误记录。下方为许可范围内的实际网格复核。

[英文研究报告](../05_Documentation/Comparative_Study_Report.md) · [全指标 CSV](Array_1x2_vs_4x4_Comparison.csv) · [图表](Comparison_Figures/)

[Power Loss 与 50 Ω 失配分解](../05_Documentation/4x4_POWER_LOSS_ANALYSIS.md) · [网格与复核](../05_Documentation/4x4_SIMULATION_VALIDATION.md)
