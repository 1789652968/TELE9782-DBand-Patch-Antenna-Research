# TELE9782 D-band Patch Antenna Research

UNSW TELE9782 的 150 GHz D-band microstrip antenna 研究交接档案。组员为 Hanqing Zhao 与 Ning Mao。演讲以 40 μm Polyimide 上的 Gold 单贴片为主，随后研究扩大地板单贴片和 1×2 阵列，并完成两轮阵列优化。

演讲记录的 Radiation Efficiency 是 **71.55%**。用户转述的讲评指出这项效率偏低，促成后续优化。研究依次比较基准单贴片、地板对照和原始 1×2 阵列，再用材料损耗诊断和多目标试验检查效率、匹配与方向图的取舍。[研究时间线](POST_PRESENTATION_RESEARCH_LOG.md)

| 交付设计 | ηrad | 峰值 Directivity | +Z Realized Gain | 150 GHz 偏角 |
|---|---:|---:|---:|---:|
| 原始 1×2 | 71.98% | 8.843 dBi | 7.406 dBi | 2° |
| 第一轮 · 推荐课程主交付 | 82.99% | 9.140 dBi | 7.763 dBi | 16° |
| ShiftBracket85 · 最高效率 | 85.49% | 8.486 dBi | 7.546 dBi | 12° |
| H085 · 第二轮综合候选 | 84.96% | 9.290 dBi | 7.764 dBi | 19–20° |
| ShiftNull75 · 150 GHz 法线候选 | 83.38% | 8.270 dBi | 7.436 dBi | 4° |

最高效率方案的带宽从 13.515 降至 8.717 GHz，峰值和法线实现增益均下降。法线方案到 154 GHz 偏角为 32°。保留 82.99% 阵列作为主交付是对增益、带宽、方向图和验证完整性的综合判断。90% 自定目标在纳入比较的已验证真实材料模型中仍有 4.51 个百分点差距。[最终取舍与指标](DESIGN_COMPARISON.md)

## 从这里开始

- [START_HERE](START_HERE.md)、[课程依据与研究目标](PROJECT_REQUIREMENTS_AND_OBJECTIVES.md)、[报告写作框架](07_Report_Handover/REPORT_WRITING_GUIDE.md)
- [原始证据](Project_Final/) 保持历史目录层级。06_Presentation 为讲稿和幻灯片，07、08、09 分别对应原阵列、第一轮和第二轮。01 至 05 为单贴片支撑材料，筛选和未达标案例保留在各阶段。
- [CST 工作流](TECHNICAL_WORKFLOW.md)、[复现入口](06_Reproduction/Reproduction_Guide.md)、[完整 CST 下载与校验](Large_Artifacts/ARTIFACT_DOWNLOAD_GUIDE.md)
- [源文件映射](08_Research_Audit/SOURCE_TO_REPOSITORY_MAP.csv)、[上传核查](08_Research_Audit/Upload_Verification.md)、[协作任务](07_Report_Handover/COLLABORATION_TASKS.md)

主交付与第二轮三个角色均有重开复算和网格证据。粗网格筛选、理想损耗诊断与历史 PPT 都有各自证据口径。所有性能数字来自 CST 仿真，样机测量待开展。
