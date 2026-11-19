# 交付设计比较

150 GHz 的 50 Ω 数据采用各阶段交付工程，效率以百分比记录。偏角列在可用时并列 2° / 1° 角度采样结果。表格的生成与数值核验以原始 CSV、重开 JSON 和 50 Ω 归一公式为依据。PDF/PPT 的历史显示值保存在原件。

| 设计 | ηrad % | ηtotal % | S11 dB | Peak D dBi | Peak RG dBi | +Z RG dBi | 偏角 ° | 带宽 GHz |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| [原单贴片](Project_Final/01_CST_Project/TELE9782_DBand_Patch_Final.cst) | 71.553 | 68.339 | -13.476 | 7.460 | 5.807 | 5.775 | 4 | 3.490 |
| [原 1×2](Project_Final/07_Array_1x2/01_CST_Project/TELE9782_DBand_1x2_Array_Final.cst) | 71.981 | 71.862 | -27.802 | 8.843 | 7.408 | 7.406 | 2 | 4.107 |
| [第一轮 · 主交付](Project_Final/08_Efficiency_Optimisation/06_Final_Candidate/TELE9782_DBand_Efficiency_Final/TELE9782_DBand_Efficiency_Final.cst) | 82.994 | 81.366 | -17.074 | 9.140 | 8.244 | 7.763 | 16 | 13.515 |
| [ShiftBracket85 · 最高效率](Project_Final/09_Multiobjective_Optimisation/07_Final_Candidates/ShiftBracket85/ShiftBracket85_Delivery/ShiftBracket85_Delivery.cst) | 85.495 | 83.193 | -15.699 | 8.486 | 7.687 | 7.546 | 12/12 | 8.717 |
| [H085 · 综合](Project_Final/09_Multiobjective_Optimisation/07_Final_Candidates/H085/H085_Delivery/H085_Delivery.cst) | 84.961 | 82.769 | -15.884 | 9.290 | 8.469 | 7.764 | 20/19 | 14.713 |
| [ShiftNull75 · 法线](Project_Final/09_Multiobjective_Optimisation/07_Final_Candidates/ShiftNull75/ShiftNull75_Delivery/ShiftNull75_Delivery.cst) | 83.381 | 82.672 | -20.704 | 8.270 | 7.443 | 7.436 | 4/4 | 11.001 |

## 取舍与选型

- **第一轮 82.99% 阵列**是课程推荐主交付。其宽度、峰值与法线增益与匹配均经过网格和保存重开验证。16° 主瓣偏转应在报告中披露。
- **ShiftBracket85** 在真实材料重开解中得到 85.49%。加厚基板与平移重调降低了金属损耗与端口吸收。重开解相对上一轮的 Peak/+Z Realized Gain 分别少约 0.56/0.22 dB，带宽少 4.80 GHz。
- **H085** 是第二轮综合候选。效率、峰值 gain、带宽提高，法线增益基本相同，偏角增至 19–20°。建议用于展示目标权重和方向稳定性的冲突。
- **ShiftNull75** 在 150 GHz 有 4°、S11 −20.70 dB；+Z 增益较上一轮低约 0.33 dB，带宽少 2.51 GHz。在 145、150、154 GHz 的偏角为 0°、4°、32°。
- **WideGround** 为第四套高分辨率对照。其三组验证完整，供分析地板加宽的限度。

[最终指标 CSV](05_Final_Comparison/Tables/FINAL_VERIFIED_PERFORMANCE.csv) · [第二轮原始对比表](Project_Final/09_Multiobjective_Optimisation/08_Results_and_Figures/Multiobjective_Comparison.csv) · [第一轮原始报告](Project_Final/08_Efficiency_Optimisation/09_Documentation/Efficiency_Optimisation_Report.md) · [第二轮重开验证](Project_Final/09_Multiobjective_Optimisation/07_Final_Candidates/Verification_Results.json) · [1° 角度对照](Project_Final/09_Multiobjective_Optimisation/08_Results_and_Figures/Angular_Resolution_Check.csv) · [145/150/154 GHz](Project_Final/09_Multiobjective_Optimisation/08_Results_and_Figures/Final_Frequency_Monitors.csv)
