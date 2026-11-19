# 复现顺序

1. 获取 [完整原生工程](../Large_Artifacts/ARTIFACT_DOWNLOAD_GUIDE.md)，在 Git clone 根目录解压 ZIP，ZIP 内部以 Project_Final 开头。操作前将目标 CST 工程及同名目录复制到工作位置。
2. 在 [验证清单](Required_Artifacts.md) 定位模型，先从 CSV/JSON 无求解复核，再用 CST 2024 打开保存的结果。对照 [技术工作流](../TECHNICAL_WORKFLOW.md) 做检查。
3. 使用 [第一轮原始指南](../Project_Final/08_Efficiency_Optimisation/09_Documentation/Reproduction_Guide.md) 和 [第二轮原始指南](../Project_Final/09_Multiobjective_Optimisation/10_Documentation/Reproduction_Guide.md)。脚本中的 D 盘路径是工作站历史路径，应在副本中映射至自己的安装和数据根。各脚本有不同前置输出，按指南留存参数、数据与日志。筛选模型的重建可能需要本地归档中的 companion 数据。
4. 用 [最终验证数值](../05_Final_Comparison/Tables/FINAL_VERIFIED_PERFORMANCE.csv) 对照采样表。上传审计验证文件和数值可追溯性，本次交接没有新增电磁求解。
