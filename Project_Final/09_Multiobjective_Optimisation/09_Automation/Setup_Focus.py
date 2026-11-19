from pathlib import Path
p=Path(__file__).with_name('Round2_Search.py')
s=p.read_text(encoding='utf-8-sig').replace("(Y,'NearRearEdge',dict(rear_delta=-.42)),","""(Y,'NearRearEdge',dict(rear_delta=-.42)),(Y,'IntermediateRearEdge',dict(rear_delta=-.23)),
          (Y,'WideApertureBroadside',tune|dict(rear_delta=-.30,ground_width=3.05,patch_width=.82,array_spacing=1.22,inset_length=.15)),
          (Y,'MovedWideAperture',tune|dict(shift_y=-.16,rear_delta=-.46,junction_y=-.355,ground_width=3.05,patch_width=.82,array_spacing=1.22,inset_length=.15)),""").replace("    run(de,A,'CombinedObjectives',boost", """    if boost.get('strip') and boost.get('shift_y',0)+boost['patch_length']/2+boost.get('strip_gap',.08)+boost['strip']>=boost['ground_length']/2+boost.get('rear_delta',0):
        boost.pop('strip',None)
    run(de,A,'CombinedObjectives',boost""")
p.write_text(s,encoding='utf-8')
p=Path(__file__).with_name('Round2_Analysis.py');s=p.read_text(encoding='utf-8-sig').replace("ky=a[:,5]+1j*a[:,6];","y=y-c.get('shift_y',0);ky=a[:,5]+1j*a[:,6];")
p.write_text(s,encoding='utf-8')

