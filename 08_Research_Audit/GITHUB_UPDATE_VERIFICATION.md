# 4×4 研究整合 · GitHub 上传复核

| 核查项 | 实际结果 |
|---|---|
| Existing repository | [TELE9782-DBand-Patch-Antenna-Research](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research) |
| Visibility / branch | Public / main |
| 4×4 integration commit | [c70888169b472c44d1df97d561d740388cf644b1](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/commit/c70888169b472c44d1df97d561d740388cf644b1) |
| Integration files | 新增 317 个，修改 11 个，主提交后共 5538 个 tracked files |
| Git content size | 新增 64,312,641 bytes，修改文件完整内容 42,891 bytes，本次主提交合计 64,355,532 bytes（未压缩文件大小） |
| LFS | 0 objects，0 bytes。既有 Git LFS 支持，本次附档使用 Release |
| Release | [4×4 comparative study](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/tag/cst-4x4-comparative-study-v1)，历史 Release 保留 |
| Anonymous attachment | [Final_4x4_Native_CST.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-4x4-comparative-study-v1/Final_4x4_Native_CST.zip)，219,838,486 bytes，550 个成员 |
| Downloaded SHA256 | `c44722650b2c30d7c6b15d615b6ebf311721b9f070c6f9cc55f83b637a8cc94c` |

本页在主提交和实际下载核查之后单独提交，因此表中列出的是集成提交的哈希和文件统计。

## 检查方式

- 从公开远程匿名浅克隆，通过 sparse checkout 拉取 4×4 与修改的交接文档，逐一用 SHA256 核对新增与修改的所有文件。重查了 323 条源证据映射、249 个本次涉及文档的本地相对链接。解码核对 12 张 PNG，并匿名请求 6 个 README、CSV、报告指南和关键图片的远端内容。公开渲染后的报告指南包含 4×4 章节锚点。主提交只改动 4×4 资料、交接文档和一条附件忽略规则，原 Project_Final/ 历史证据保持原样。
- 按保存值重新计算 150 GHz 的 ηrad、50 Ω ηtotal 和功率闭合。Comparison CSV 数字字段与 Final_Metrics.json 和 CST 原生功率导出一致。4×4 130–170 GHz 的 1001 点 S11 均高于 −10 dB，最佳 −9.267 dB @ 163.20 GHz。
- 对匿名下载的 ZIP 逐字节计算 SHA256。使用 CST 2024 打开临时解压副本，从 CST 原生数据库读取 1001 点 S11，独立转换得到 150 GHz S11 -4.114149 dB（50 Ω）、ηrad 74.35601969%、带符号功率闭合残差 2.140061 mW。成功选取 150 GHz 的原生 Farfield、E-field、H-field 与 Surface Current。复核过程沿用原求解结果。
- 对 5,221 个旧 tracked files 做基本凭据模式检查，对拟发布文件、ZIP 成员和 CST 容器进行凭据、私人联系方式及工作站信息检查。新增内容没有发现密钥或令牌命中。两个日志的工作站主机名已替换。初始工程内部含本机用户目录，其二进制工程保留本地。新增材料限定于项目原创工程、脚本、结果与文档。检查范围为当前树及本次附件。

## 保留在本地的资料

初始 CST 二进制（87,808 bytes）以及非交付试验的完整 companion 数据未发布，原始几何参数、ModelHistory、原生数值导出、solver logs 以及失败或被拒试验证据均可在相应 Git 目录查阅。最终 23/33 网格已随 Final_4x4 附件提供，对应工作目录的重复缓存保留本地。旧工程、历史提交、标签和公开设置均保留。

[4×4 研究](../4x4_Array_Comparative_Study/README.md) · [完整原生附件与成员清单](../4x4_Array_Comparative_Study/Artifact_Manifest.md) · [来源映射](../4x4_Array_Comparative_Study/SOURCE_FILE_SHA256.csv) · [公开排除项](../4x4_Array_Comparative_Study/EXCLUDED_SOURCE_FILES.csv)
