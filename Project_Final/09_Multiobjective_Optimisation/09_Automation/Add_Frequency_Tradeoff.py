from pathlib import Path
d=Path(__file__).resolve().parent;p=d/'Explain_Final_Losses.py';s=p.read_text(encoding='utf-8-sig')
if '三项候选的频率稳定性' not in s:
    s+="""
        import csv
        with (R/'Final_Frequency_Monitors.csv').open(encoding='utf-8-sig',newline='') as src:
            measured=[row for row in csv.DictReader(src) if float(row['frequency_GHz']) in (145,150,154)]
        f.write('\\n## 三项候选的频率稳定性\\n\\n|交付候选|频率 GHz|主瓣偏角 °|+Z 实现增益 dBi|S11 dB，50 Ω|\\n|---|---:|---:|---:|---:|\\n')
        for row in measured:
            f.write(f"|{row['name']}|{float(row['frequency_GHz']):.0f}|{float(row['theta']):.0f}|{float(row['G0']):.3f}|{float(row['S11_50']):.2f}|\\n")
        far=next(row for row in measured if row['name']==br['name'] and float(row['frequency_GHz'])==154)
        f.write(f"\\n法线候选在 154 GHz 的实算偏角为 {float(far['theta']):.0f}°，此时 S11 为 {float(far['S11_50']):.2f} dB。150 GHz 工作点的偏角改善不能外推到整个匹配频带。\\n")
"""
    p.write_text(s,encoding='utf-8')

