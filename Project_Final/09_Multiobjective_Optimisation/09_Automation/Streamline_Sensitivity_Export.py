from pathlib import Path
d=Path(__file__).resolve().parent
p=d/'Array_Build.py';s=p.read_text(encoding='utf-8-sig')
if 'export_frequencies=None' not in s:
    s=s.replace('def extract(p, label=None):','def extract(p, label=None, export_frequencies=None):')
    s=s.replace("            m.SelectTreeItem(item)\n            ff.Reset()", "            if export_frequencies is not None and f not in export_frequencies:continue\n            m.SelectTreeItem(item)\n            ff.Reset()",1)
    s=s.replace('def run(p):','def run(p,export_frequencies=None):').replace('    return extract(p)\n','    return extract(p,export_frequencies=export_frequencies)\n')
    p.write_text(s,encoding='utf-8')
p=d/'Round2_Core.py';s=p.read_text(encoding='utf-8-sig')
s=s.replace("    p.save();dump(folder/'round2.json',v);","    dump(folder/'round2.json',v);").replace("s,data=b.run(p);assert", "s,data=b.run(p,export_frequencies={150} if mode=='sensitivity' else None);assert")
p.write_text(s,encoding='utf-8')

