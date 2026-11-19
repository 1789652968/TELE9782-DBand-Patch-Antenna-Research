"""Corridor check for the inset feed and dispatch the full deliverables entry point."""
from pathlib import Path
p=Path(__file__).with_name('Round2_Search.py')
s=p.read_text(encoding='utf-8-sig').replace("    for st,name,c in jobs:run(de,st,name,c)","""    for st,name,c in jobs:
        if name in ('ShortFeedWide','MovedWideAperture'):
            c['junction_y']=round(min(c['junction_y'],-c['patch_length']/2-c['feed_width']/2-.02),4)
            c['shift_y']=round(max(c['shift_y'],-.747-c['junction_y']+c['feed_width']/2),4)
        run(de,st,name,c)""")
s=s.replace("    if boost.get('strip') and", """    min_rear=boost.get('shift_y',0)+boost['patch_length']/2-boost['ground_length']/2+.015
    if boost.get('rear_delta',0)<min_rear:boost['rear_delta']=round(min_rear,4)
    if boost.get('strip') and""")
p.write_text(s,encoding='utf-8')
p=Path(__file__).with_name('Round2_Report.py')
with p.open('a',encoding='utf-8') as f:f.write("""
if __name__=='__main__':
    import subprocess
    from Round2_Delivery import main
    if (V/'Final_Selection.json').exists():
        subprocess.run([str(ROOT.parents[1]/'CST Studio Suite 2024/Opera/code/bin/python.exe'),'-u',str(Path(__file__).with_name('Round2_Fields.py'))],check=True)
    main()
""")

