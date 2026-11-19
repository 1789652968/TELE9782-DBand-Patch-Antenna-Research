from pathlib import Path
d=Path(__file__).resolve().parent
p=d/'Round2_Angular_Resolution.py';s=p.read_text(encoding='utf-8-sig')
needle='def export(p,folder):'
if 'def complete_angular(' not in s:
    s=s.replace(needle,'''def complete_angular(path):
    if not path.is_file():return False
    with path.open(errors='replace') as f:
        next(f,None);next(f,None)
        n=sum(1 for line in f if line.strip() and len(line.split())==8)
    return n in (181*360,181*361)
'''+needle)
    s=s.replace("if path.exists() and path.stat().st_size>5000000:return","if complete_angular(path):return")
    s=s.replace("a=a[a[:,1]<360];w=", "assert len(a)==len(th)*len(ph) and len(th)==181 and len(ph) in (360,361)\n        a=a[a[:,1]<360];w=")
    p.write_text(s,encoding='utf-8')
p=d/'Round2_Fields.py';s=p.read_text(encoding='utf-8-sig')
if 'from Round2_Angular_Resolution import complete_angular' not in s:
    s=s.replace('import shutil','import shutil\nfrom Round2_Angular_Resolution import complete_angular')
    s=s.replace("and (folder/'Farfield_150_1deg_Directivity.txt').exists()", "and complete_angular(folder/'Farfield_150_1deg_Directivity.txt')")
    p.write_text(s,encoding='utf-8')

