# 复现效率优化研究

建议首先从 06_Final_Candidate/TELE9782_DBand_Efficiency_Final/TELE9782_DBand_Efficiency_Final.cst 打开最终模型，保留相邻同名伴随目录。CST Studio Suite 2024 中可查看原生 S1,1、farfield (f=150) [1]、E 场与 surface current。File → Save As 后在独立副本中运行时域求解，可保留交付文件和归档结果。全空间输出使用全局包络积分面与 2° 采样。最终口径的 50 Ω 曲线可使用同目录 CST_50ohm.s1p。

## 脚本和数据

08_Automation 中的 Array_Build、Array_Run、Array_Audit、Array_Results_Extraction 和 Reference_ModelHistory 来自原工程。Efficiency_CST.py 从 01_Baseline_Copy 的原生模型及建模历史创建独立项目，调整参数，调用 CST 接口求解并复用原生结果导出。运行时勿指向原 07 工程写入。新参数及理想化标签保存在每个 case 的 parameters.json，completed.json 只在求解成功并导出角度数据后生成。

在相同目录结构的研究副本中，从 08_Automation 运行。CST 使用安装目录下 Opera/code/bin/python.exe，数值处理使用 NumPy 2 和 Matplotlib 环境。CST 工程与导出曲线的来源为本地完整工程。要从头重现，应使用新的研究副本并仅预置 01_Baseline_Copy 和 08_Automation、其余阶段空目录；已有 completed.json 的 case 会被复用。原单贴片和旧阵列三模型对比仍读取 Project_Final 下相邻的已验证结果。

1. 用 CST 的 Python 运行 Check_Baseline.py、Efficiency_CST.py，核对备份并顺序求解 A–D。
2. 用同一解释器运行 Efficiency_Study.py，完成馈线、厚度、重新匹配、最终细网格及独立网格、140 GHz 端口模式敏感性实验。
3. 用同一解释器运行 Efficiency_Edge_Fields.py、Efficiency_Verify.py。前者从已存监视器提取边缘场；后者另存最终文件、关闭重开、复算并重新读取结果。
4. 用数值分析环境依次执行 Efficiency_Analysis.py 与 Efficiency_Report.py，重建 07_Results_and_Figures 和 09_Documentation。CSV 的布局由脚本定义。All_Candidates.csv 含不满足匹配要求的筛选结果，不能作为可用设计排序直接采用。

## 检查入口

- 01_Baseline_Copy/Native_Provenance.json：备份散列及 cst.results 直接读取的基线功率。
- 06_Final_Candidate/verification.json：两次重开、复算状态、端口、参数、全部远场监视器及 S11 差值。
- 07_Results_and_Figures/Validation.json：独立 50 Ω 校核、功率、球面积分、支路幅相和趋肤深度。
- 02–06 各案例的 .cst、同名结果目录、原生曲线、farfield 角度表与求解日志。最终 Project 保存 130–170 GHz 扫频，只有离散 farfield monitor 对应独立远场值。
