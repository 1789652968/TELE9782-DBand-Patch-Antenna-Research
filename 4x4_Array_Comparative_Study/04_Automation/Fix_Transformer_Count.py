from pathlib import Path
p=Path(__file__).with_name('Build_4x4.py');s=p.read_text(encoding='utf-8')
s=s.replace("sum(x['name'].endswith('_transformer') for x in metal)","sum(x['name'].startswith('level') and x['name'].endswith('_transformer') for x in metal)")
p.write_text(s,encoding='utf-8')

