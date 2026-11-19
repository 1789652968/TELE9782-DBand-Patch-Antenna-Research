# 项目要求与研究目标

## 课程依据

现存 [PPT](Project_Final/06_Presentation/TELE9782_DBand_Patch_Presentation.pptx) 第 2 页记录了 D-band 130–170 GHz 设计与扫频范围、150 GHz nominal design point 和 maximum Directivity **>6.5 dBi**。并要求比较解析与仿真匹配频率，绘制 S11、−10 dB 带宽、Directivity、Realized Gain、Radiation Efficiency 和 E/H-plane。该页属于团队对课程要求的历史转录。正式 Project brief 或 rubric、允许的具体阵列范围和提交格式仍需用课程原文确认。实际验收应检验 150 GHz 同一工作点的方向性与匹配，整段 130–170 GHz 连续匹配属于另一个目标。

## 演讲反馈与自定目标

约 71.55% 的效率取自 PPT 第 9 页。教师对这一数值偏低的评价来自项目组转述，现有文件未发现录音或原始书面讲评。第一轮自行设定 ηrad 尽量 ≥80%，保住 6.5 dBi、增益与匹配。第二轮尝试 ≥90%，同时保持匹配、Directivity 与带宽，提高峰值和 +Z Realized Gain，减小 Beam Squint，并检查制造公差。这些效率目标是内部优化目标。

## 验证与局限

CST Studio Suite 2024、150 GHz 工作点、统一 50 Ω。按接受功率归一的 ηrad 与含失配的 ηtotal 分别记录。峰值增益取全空间极大值，+Z 取 θ=0°。对照 modal reference 与 50 Ω Touchstone、port mode 和 reference plane，核查网格、全空间归一、闭合残差与保存重开复算。见 [技术工作流](TECHNICAL_WORKFLOW.md)。

真实金属和有损介质的工程模型采用 nominal Polyimide εr 3.5、tanδ 0.0027 和 σ=4.561×10⁷ S/m 的 Gold，厚度随试验注明。150 GHz 的材料色散及加工偏差仍有不确定性。实际样机测量待补。单频偏角改善具有频率依赖性，第二轮未达到 90%。
