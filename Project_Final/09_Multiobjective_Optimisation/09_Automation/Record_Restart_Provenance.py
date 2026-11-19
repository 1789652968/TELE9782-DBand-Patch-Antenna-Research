from pathlib import Path
d=Path(__file__).resolve().parents[1]/'10_Documentation/Reproduction_Guide.md'
s=d.read_text(encoding='utf-8-sig')
if 'Recover_ShiftNull_Touchstone.py' not in s:
    s+="""
### 从本次交付文件复查

系统重启前已保存 ShiftNull75 的原生交付工程、成功求解记录和重开验证。Recover_ShiftNull_Touchstone.py 只重新导出 50 Ω Touchstone，并以保存的原生复 S11 独立换算复核全部 1001 个频点。原中断片段以 .partial 扩展名保留。此项恢复没有增加一次电磁求解。

本轮完成后的完整工程入口以 07_Final_Candidates/Final_Selection.json 为准。打开任一候选时保留与 .cst 同名的原生目录。比较复算前后的数值时，请先复制工程及同名目录到新的工作位置。Round2_Port.py 在物理端口固定时分别复核综合方案和最高效率方案。Round2_Fields.py 从已保存的原生结果另外导出 1° 球面和复电场网格。Final_Frequency_Monitors.csv 仅包含实际存在的求解监视点；原生一维频扫为 130–170 GHz。

制造敏感性采用 20/30 网格与该网格的标称实算对比。每次扰动保留其原生工程、全频段复 S 参数和功率。制造试验汇总的远场工作点取 150 GHz。Delivery_File_Check.py 用绘图 Python 执行，复核交付工程、推荐项目哈希、文件数量、图片可打开性、复算链和原始工程 SHA256。
"""
    d.write_text(s,encoding='utf-8')

