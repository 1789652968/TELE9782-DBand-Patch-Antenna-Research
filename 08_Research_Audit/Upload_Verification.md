# GitHub 上传与完整性核查

初次归档时仓库为 Private，默认分支为 main。随后按项目组要求改为公开。已通过无登录请求复核仓库主页、Release 附件列表和推荐工程 ZIP 的下载响应。初始档案提交为 [152a3c1025dda386d0a9c55a7cecb1b047583b8c](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/commit/152a3c1025dda386d0a9c55a7cecb1b047583b8c)。从 GitHub 单独克隆该提交，运行 git fsck，并逐个核对映射表中全部上传源文件的 SHA256。档案快照含 5,220 个文件、628,858,636 字节。这个统计基于初始档案提交。完成查验后再提交此页、原生场读回记录与链接。

Git 未使用 LFS，核验得到零 LFS 指针。Release 总计 8 个附件、1,085,531,393 字节。逐一从 GitHub 下载，以实际响应内容核对大小和 SHA256。每个 ZIP 在本地制作时对所有成员逐一核对原文件 SHA256。[GitHub Release](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/tag/cst-research-archive-v1)

| 附件 | 字节数 | SHA256 |
|---|---:|---|
| [GroundControl.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-research-archive-v1/GroundControl.zip) | 60,572,110 | 77818736dc161d7237d377d6577bfcfeb5c626e42aba96ea046c234e22f68ba4 |
| [H085_Delivery.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-research-archive-v1/H085_Delivery.zip) | 163,317,997 | 2693f6df020ed7dc9e7885cd58855b41626e7a87920e7e93783c3b703e364a2e |
| [ShiftBracket85_Delivery.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-research-archive-v1/ShiftBracket85_Delivery.zip) | 163,456,580 | ea55e79c2d53f52af55d8e885663373fdc2e1ed193ef0d1664bf66d280ab202b |
| [ShiftNull75_Delivery.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-research-archive-v1/ShiftNull75_Delivery.zip) | 161,086,872 | ae399cb7516833fd7dad7e83ab335e435a57a36dc70c210297fca1285f4aa3cb |
| [TELE9782_DBand_1x2_Array_Final.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-research-archive-v1/TELE9782_DBand_1x2_Array_Final.zip) | 135,363,608 | fdf0082ac6ad88174a77c08141282e7820245fcf1de190ef62c202b979f8def9 |
| [TELE9782_DBand_Efficiency_Final.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-research-archive-v1/TELE9782_DBand_Efficiency_Final.zip) | 159,266,503 | 236117e546bf13d479a44ddf19155358a28353c2218b0a9458e6a151cd5bf95c |
| [TELE9782_DBand_Patch_Final.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-research-archive-v1/TELE9782_DBand_Patch_Final.zip) | 77,195,885 | c9a9e87f767f9eb131dba95c068b25851ed9d40776d352771c03a9126b5f6f4e |
| [WideGround_Delivery.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-research-archive-v1/WideGround_Delivery.zip) | 165,271,838 | 272b6516fc4c43f705d97e23d3d37c3c42c47e5f6195503e16684f0997c41b01 |

CST 2024 从八份解压副本读到原始复数 S11，每个工程 1001 点。进一步打开原生模型并读取 150 GHz Farfield，核对可用的 Surface Current 节点。全过程采用独立副本，属于已保存结果的复查。[1D 读回](Native_Archive_CST_Readback.json) · [Farfield 与电流读回](Native_Field_Readback.json)

原始清单共 54,199 项。仅本地 44,819 项、9,034,895,960 字节，包含完全相同副本及未归档的筛选 Companion、重建缓存和临时文件。主要交付和对照模型的原生 Model 与 Result 随附件提供。各中间试验的小型模型、参数、求解日志和数值导出保留在 Git。实际账户 LFS 剩余用量未获得授权接口数据，选择 Release 避免占用 LFS。[源文件映射](SOURCE_TO_REPOSITORY_MAP.csv) · [全工程文件清单](FILE_INVENTORY.csv)

本次自动扫描 17 份新交接文档的相对链接，并在归档的 Markdown 中记录 0 个缺失目标。已检查关键文本和 Office 文档的常见秘密凭据格式。由文件表核对了 39 个几何筛选、68 条第二轮试验、15 条公差和 28 张汇总图。[证据缺口](MISSING_OR_UNVERIFIED_FILES.md)
