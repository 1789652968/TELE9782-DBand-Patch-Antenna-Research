# 完整 CST 工程下载

小型证据和对应原生几何入口随 Git 提供。完整 Model、Result 和其他项目依赖使用公开仓库的 Release ZIP。每个包包含原生 .cst 和与其同名的 companion 目录。可在 Git clone 根目录或单独短路径解压，保持 Project_Final 内层结构。在 CST 2024 中打开对应 .cst，历史结果从 Result 读取。求解应在副本运行。

| ZIP | 角色 |
|---|---|
| [TELE9782_DBand_Patch_Final.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-research-archive-v1/TELE9782_DBand_Patch_Final.zip) | 演讲单贴片 |
| [GroundControl.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-research-archive-v1/GroundControl.zip) | 相同扩大地板下的单贴片对照 |
| [TELE9782_DBand_1x2_Array_Final.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-research-archive-v1/TELE9782_DBand_1x2_Array_Final.zip) | 原始已验证阵列 |
| [TELE9782_DBand_Efficiency_Final.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-research-archive-v1/TELE9782_DBand_Efficiency_Final.zip) | **推荐课程主交付** |
| [ShiftBracket85_Delivery.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-research-archive-v1/ShiftBracket85_Delivery.zip) | 最高辐射效率方案 |
| [H085_Delivery.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-research-archive-v1/H085_Delivery.zip) | 第二轮综合候选 |
| [ShiftNull75_Delivery.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-research-archive-v1/ShiftNull75_Delivery.zip) | 150 GHz 法线候选 |
| [WideGround_Delivery.zip](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/download/cst-research-archive-v1/WideGround_Delivery.zip) | 第四套高分辨率入围对照 |

无需登录，可直接在 [GitHub Release](https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research/releases/tag/cst-research-archive-v1) 下载。请在 [附件清单](RELEASE_ASSETS.csv) 核对压缩字节数，再用 PowerShell 的 `Get-FileHash -Algorithm SHA256` 对照 SHA256。[源文件映射](../08_Research_Audit/SOURCE_TO_REPOSITORY_MAP.csv) 列出每个压缩包的成员。中间筛选项目保留小型几何、脚本、原生导出与日志，其剩余原生目录在本地源映射中标出。上传状态和实际下载链接见 [上传核查](../08_Research_Audit/Upload_Verification.md)。

## 4×4 对照组

[4×4 原生工程与 SHA256](../4x4_Array_Comparative_Study/Artifact_Manifest.md) 提供独立 Release 和完整同名 companion（550 个 ZIP 成员）。解压后在 CST 2024 打开 `01_CST_Project/Final_4x4/Final_4x4.cst`。与已有 Project_Final 中的 1×2 附件可分别解压。本项保留上述历史 Release 不变。
