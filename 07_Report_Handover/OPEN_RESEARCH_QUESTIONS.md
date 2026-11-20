# 待共同讨论的问题

| 议题 | 已有证据 | 下一项所需证据 |
|---|---|---|
| 82.99% 是否仍是课程主交付 | [四方案取舍](../DESIGN_COMPARISON.md) | 按正式 rubric 复核对 broadside、带宽、增益的优先顺序 |
| 16° Beam Squint 的机制 | [工作频率场与地板敏感性](../Project_Final/09_Multiobjective_Optimisation/10_Documentation/Beam_Squint_Diagnosis.md) | 单独控制 finite-ground、launch、feed 或重新取样验证贡献 |
| 85.49% 的意义与 90% 差距 | [功率及网格证据](../Project_Final/09_Multiobjective_Optimisation/10_Documentation/Final_Optimisation_Report.md) | 明确此几何搜索的覆盖范围，材料和功率模型的外推范围 |
| 频率稳定性与样机 | [145/150/154 GHz 监视数据](../Project_Final/09_Multiobjective_Optimisation/08_Results_and_Figures/Final_Frequency_Monitors.csv) | 必要时补更密 monitor，对加工件做校准测量 |
| Port absorption 和材料 | [同几何模式计算对照](../Project_Final/09_Multiobjective_Optimisation/08_Results_and_Figures/Highest_Efficiency_Port_Check.json) | 独立材料表征、参考面/port size 控制及去嵌入实验 |

## 4×4 comparative results

1. How much of the measured full-structure loss difference can be isolated to transmission lines, junctions, or radiating patches by separately integrating each region? [Power Loss Analysis](../4x4_Array_Comparative_Study/05_Documentation/4x4_POWER_LOSS_ANALYSIS.md)
2. How would a 4×4 matched at 150 GHz change peak and broadside gain and bandwidth? Current conclusions are conditional on the basic stepped-feed model. [Matching trials](../4x4_Array_Comparative_Study/02_Simulation_Results/Verification/Matching_Trials.csv)
3. How much of the field spread arises from coupling, standing waves, or the side-fed trunk? Discuss probe planes, reference directions and de-embedded branch measurements. [Probe data](../4x4_Array_Comparative_Study/02_Simulation_Results/Farfield/Patch_Feed_Probes_150.csv)
4. Is the smaller 4×4 offset worth a roughly 0.10 dB lower broadside gain and the lack of a matched band at 150 GHz? Discuss what the course report should prioritize. [Design comparison](../DESIGN_COMPARISON.md)
