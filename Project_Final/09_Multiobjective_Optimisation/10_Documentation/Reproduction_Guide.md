# 复现 TELE9782 150 GHz 第二轮多目标优化

## 查看与复核

1. 在 07_Final_Candidates/Final_Selection.json 查看角色到实际目录的映射。打开交付目录内与目录同名的 .cst，同时保留同名原生结果文件夹。基线完整备份在 01_Baseline_Backup。Baseline_Backup_Check.csv 给出源文件与备份的逐文件 SHA256。
2. 使用 CST Studio Suite 2024，Time Domain、130–170 GHz、单一 y-min 波导端口和开放边界。读取实际模型历史中的 Gold 和 Polyimide (lossy) 定义以及完整参数。各候选 parameters.json 给出参数，扩展几何（后缘、平移或无源片）的尺寸还写入独立模型历史。长度单位 mm，频率 GHz，功率 W，增益 dBi。
3. 在交付工程的副本上运行求解，避免改写已核查数据。查看 Model.log 的稳态终止、网格数和端口模消息。读取 1D Results 下的 S-Parameters、Reference Impedance 和 Power/Excitation [1]，以及 Farfields 下的 145、150、154 GHz 三维结果。各 1D 表每行保留原始实部及虚部。E/H 场、表面电流及点场使用 150 GHz 的原生监视器。
4. 使用原生复 Γ 与实参考阻抗计算 Zin=Zref(1+Γ)/(1−Γ)，再用 Γ50=(Zin−50)/(Zin+50) 核对 CST_50ohm.s1p。检查峰值及 +Z 实现增益，并比较归一化前后结果。核对 Prad/Pacc 与远场 ηrad、全空间方向性积分、接受功率闭合和原生实现增益的角度。Independent_Audit.json 记录审计值。
5. 完整方向图为 2° 步进的 CST ASCII 球面采样。+Z 对应 θ=0°。E 面取 φ=90°/270°，H 面取 φ=0°/180°。Radiation_Pattern_Audit.csv 给出 HPBW；Full_Sphere_Audit.csv 中的次峰采用前半空间内偏离主峰超过 10° 的局部最大值，空白表示该定义下未检出。法线交叉极化采用 Y 为共极化的 Ludwig-3 分解。近场相位图参照每个模型 |Ez| 最大的采样点，低于最大幅度 3% 的点掩蔽。

## 从工作目录复现

CST 运行时为 D:\TELE9782\CST Studio Suite 2024\Opera\code\bin\python.exe。数值绘图使用 C:\Users\Admin\AppData\Local\spyder-6\envs\spyder-runtime\python.exe（numpy、matplotlib），将后者目录及 Library\bin 放在 PATH 前面。第三方工具无需网络。每次只运行一个求解任务。

- 以本目录结构为模板，新建单独的实验工作目录，复制 01_Baseline_Backup、09_Automation 和空的其余阶段目录。脚本以自身上级目录为根。保留原始 07 与 08 路径以便生成历史对照。
- 在 09_Automation 中使用 CST Python 执行 Round2_Core.py 重放初筛。Round2_Search.py 读取已完成的初筛记录，进行自适应联合优化、三种角色选择、两种网格、保存重开复算及公差研究。独立的密网格采用 38/57，交付文件采用 36/54。脚本验证参数完全相同后才复用 completed 结果；从空候选目录运行可触发真正的新求解。
- 对现有数据仅重新生成比较表和工程报告，可用数值绘图 Python 运行 Round2_Delivery.py。需要重新导出高密度复电场样本时，在完成求解后运行 CST Python 的 Round2_Fields.py。该步骤在独立的历史/场视图副本中读取原生三维结果。Round2_Report.py 作为完整后处理入口先导出场，再调用交付生成程序。
- PowerShell 入口 Continue_Study.ps1 可在初筛已启动后接续后续任务，原始日志位于 09_Automation。若脚本中断，先读取相应 *.err 和候选的 error.json。setup_ready 标记记录已完整建立的几何，round2.json 仅在真实求解和所需导出均结束时写入。保留失败目录作为审计记录。

## 证据位置

08_Results_and_Figures 汇总优化试验、选型、收敛、频率、公差、近场和远场数据。各个求解目录内，.cst 同名目录的 Result/Model.log 是求解器日志，Model/3D/ModelHistory.json 记录物理模型。summary.json 保存原生远场监视器统计及消息，1D Results_*.csv 为原生一维导出。Farfield_*_Sphere.txt 为 CST 原生全空间输出。round2.json 和汇总表为可复算的后处理。图中频率点取实际求解监视器，不在缺失频点构造方向图。

## 本次中断恢复与精细定位

Round2_Resume.py 是本轮交付所用的续跑入口。完成 Round2_Core.py 初筛后，若从空目录重建，先在 CST Python 会话用 Round2_Search.focused(de) 完成联合筛选及 Round2_Search.final_jobs(de) 进行初选验证。已有 H085 的生产和加密结果时，可直接运行 Round2_Resume.py。它先核对成功求解的原生复 S11 与原导出 1001 个采样值，在独立 CST 连接补齐图像中断时未完成的数值导出。之后按实测方向相反的两个位置补做几何夹逼，再选择和复算入围候选。Round2_Local_Bracket.py 记录最后一次位置细化。故障保存在 H085_Delivery/error.json。原生求解成功和图片导出错误在审计表中分别记录。

Resume_Publish.py 是本次交付的后处理入口。在搜索结束后，它先做独立端口模式频率试验，读取历史工程副本和最终候选的原生仿真场，再生成最终报告与图表。日志为 Resume.log、Resume.err、Publish.log、Publish.err。本轮完整搜索不需要重复执行已完成的历史脚本 Round2_Targeted.py。

### 从本次交付文件复查

系统重启前已保存 ShiftNull75 的原生交付工程、成功求解记录和重开验证。Recover_ShiftNull_Touchstone.py 只重新导出 50 Ω Touchstone，并以保存的原生复 S11 独立换算复核全部 1001 个频点。原中断片段以 .partial 扩展名保留。此项恢复没有增加一次电磁求解。

本轮完成后的完整工程入口以 07_Final_Candidates/Final_Selection.json 为准。打开任一候选时保留与 .cst 同名的原生目录。比较复算前后的数值时，请先复制工程及同名目录到新的工作位置。Round2_Port.py 在物理端口固定时分别复核综合方案和最高效率方案。Round2_Fields.py 从已保存的原生结果另外导出 1° 球面和复电场网格。Final_Frequency_Monitors.csv 仅包含实际存在的求解监视点；原生一维频扫为 130–170 GHz。

制造敏感性采用 20/30 网格与该网格的标称实算对比。每次扰动保留其原生工程、全频段复 S 参数和功率。制造试验汇总的远场工作点取 150 GHz。Delivery_File_Check.py 用绘图 Python 执行，复核交付工程、推荐项目哈希、文件数量、图片可打开性、复算链和原始工程 SHA256。
