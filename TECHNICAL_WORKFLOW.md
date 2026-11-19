# CST 技术工作流

## 有证据的历史操作

演讲的 troubleshooting 先修正 uniform launch 与端口方向，再用 inset sweep 移动匹配，重建参数化有限地板。原阵列 Execution Log 记录 Transformer / Refined / Final50 和保存重开。Round 1 的 Efficiency_CST、Efficiency_Study、Efficiency_Verify 实施损耗实验及交付核验。Round 2 的 Round2_Core / Geometry / Search / Resume 调用 CST API 写参数、重建 history、启动求解并导出；Round2_Fields 和角分辨率程序处理已存储监视器，Recover_ShiftNull_Touchstone 恢复导出。实际持久操作在 companion 的 Model/3D/ModelHistory.json 与 Result/Model.log 中。[原阵列脚本](Project_Final/07_Array_1x2/04_Automation/) · [第一轮脚本](Project_Final/08_Efficiency_Optimisation/08_Automation/) · [第二轮脚本](Project_Final/09_Multiobjective_Optimisation/09_Automation/)

## 在 CST Studio Suite 2024 复现

1. 解压指定 Release 工程，保持 .cst 与同名目录相邻。保留原档，用副本在可写路径打开。检查 Parameters、Model History 和 units，核对 substrate_h、patch_width / length、array_spacing、junction_y、feed_width、transformer 和 inset。检查有损 Polyimide、有限导电率 Gold、2 μm 金属厚度。
2. 在组件和边界设置检查有限 ground、launch 的 y-min 单波导端口、单 quasi-TEM mode、参考面和 open boundaries。核对 130–170 GHz time-domain、原监视器、网格参数。模型版本之间的设置以各自原生历史为准。
3. 在 1D Results 读复 S11、Accepted、Radiated、Metal、Dielectric 和 Port Absorption。归一到 50 Ω 前保留原 modal reference。电压波假设下 Zin=Zref(1+Γ)/(1−Γ)，Γ50=(Zin−50)/(Zin+50)，S11=20log₁₀|Γ50|。用原生 50 Ω S1P 交叉验证，报告包含 150 GHz 的连续 −10 dB 区间。
4. ηrad=Prad/Pacc，ηtotal,50=ηrad(1−|Γ50|²)，Grealized,50=D+10log₁₀(ηtotal,50)。θ=0° 读 +Z，球面最大值读峰值。辐射、金属、介质与端口吸收从接受功率闭合；避免把 outgoing/reflected power 重复计入。均匀球积分以 sinθ 加权，线性 Directivity 全空间均值应接近 1。
5. 从 Farfields 查看 3D、Directivity 和 Realized Gain；固定相同切面导出 E-plane yz（φ=90°/270°）和 H-plane xz（φ=0°/180°），在 Field Monitors 看 150 GHz Surface Current 和复电场。用 2°/1° 球面网格追踪最大点，报告抽样间隔。记录 145、150、154 GHz 的偏角和匹配依赖。
6. 在独立副本按原网格设置求解，另建细网格，读取 cell 数与 solver 完成记录。保存、关闭、重开后重新求解，比较 1001 点复 S11、功率、增益、偏角和 far-field integrals。先看 [复现路径与环境](06_Reproduction/Reproduction_Guide.md) 再运行脚本。
