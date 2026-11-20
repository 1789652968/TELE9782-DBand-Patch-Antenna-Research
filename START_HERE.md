# Ning Mao 的研究交接入口

先读这页、[演讲后研究日志](POST_PRESENTATION_RESEARCH_LOG.md) 和 [英文报告框架](07_Report_Handover/REPORT_WRITING_GUIDE.md)。随后打开 [结果对比](DESIGN_COMPARISON.md) 与 [图表索引](07_Report_Handover/FIGURE_AND_TABLE_INDEX.md)。

本项目研究 150 GHz D-band Gold / Polyimide microstrip patch。原单贴片在演讲时达到 7.460 dBi，但讲评转述指出 71.55% Radiation Efficiency 偏低。初版阵列提高了 Directivity。第一轮降低了损耗并得到 82.99%，第二轮验证了效率、增益、带宽与 Beam Squint 的取舍。课程主交付仍用第一轮原生 CST，ShiftBracket85、H085、ShiftNull75 分别用于展示最高效率、综合候选及法线校正。

按 [下载指南](Large_Artifacts/ARTIFACT_DOWNLOAD_GUIDE.md) 获取同名 CST 工程及结果。撰写报告时先从 [最终指标原值](05_Final_Comparison/Tables/FINAL_VERIFIED_PERFORMANCE.csv) 取数，再回到 [原始证据](Project_Final/) 核对 50 Ω 口径、网格和 Power Balance。先把 [待议问题](07_Report_Handover/OPEN_RESEARCH_QUESTIONS.md) 转化为讨论记录，再在分支上提交图表、方法段落或核查到的证据。

## Why We Added the 4×4 Array

Ning Mao，完成两轮 1×2 优化后，我们用一个常规 4×4 来比较增加单元数后的收益与代价。4×4 的 Directivity 更高、波束更窄；1×2 的效率和匹配更好，固定 +Z Realized Gain 略高。4×4 使用更长的 15 T-junction 馈电网络。全结构损耗积分支持比较两种设计，馈线自身贡献仍待区分。这两套设计的 CST 结果支持保留 82.99% 的 1×2 作课程主方案，4×4 用作横向研究。

## Suggested Reading Order

1. [Project Root README](README.md)
2. [Post-presentation research log](POST_PRESENTATION_RESEARCH_LOG.md)
3. [4×4 Comparative Study](4x4_Array_Comparative_Study/README.md)
4. [Design Methodology](4x4_Array_Comparative_Study/05_Documentation/Design_Methodology.md)
5. [中文比较](4x4_Array_Comparative_Study/03_Comparison/Comparison_Summary.md)
6. [Comparative Study Report](4x4_Array_Comparative_Study/05_Documentation/Comparative_Study_Report.md)
7. [Raw CST Results](4x4_Array_Comparative_Study/Native_Exports/) 和 [完整原生工程](4x4_Array_Comparative_Study/Artifact_Manifest.md)
8. [Final Report Writing Guide](07_Report_Handover/REPORT_WRITING_GUIDE.md#comparative-study-12-vs-44-patch-array)
