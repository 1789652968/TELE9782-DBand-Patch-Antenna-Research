from pathlib import Path
here=Path(__file__).resolve().parent
p=here/'Build_4x4.py';s=p.read_text(encoding='utf-8-sig')
old="    line('trunk',(port,-s0),(x1,-s0),w,w/2)"
new="""    if 'match_width' in c:
        a=port+c['match_start'];b=a+c['match_length']
        assert port+.16<=a and b<=x1-.08
        assert .045<=c['match_width']<=.25
        line('trunk',(port,-s0),(a,-s0),w)
        line('input_transformer',(a,-s0),(b,-s0),c['match_width'])
        line('input_to_divider',(b,-s0),(x1,-s0),w,w/2)
    else:
        line('trunk',(port,-s0),(x1,-s0),w,w/2)"""
s=s.replace(old,new)
s=s.replace("    legs=[]","    legs=[]") # Topology is guarded further below.
s=s.replace("metal=[];patches=[];legs=[]","metal=[];patches=[];legs=[];segments={}")
s=s.replace("        legs.append(math.hypot(bx-ax,by-ay))", "        legs.append(math.hypot(bx-ax,by-ay));segments[label]=(a,bb)")
needle="    visited={0}; frontier=[0]"
add="""    lines=[a for a in metal if a['kind']=='feed']
    for i,a in enumerate(lines):
        for b in lines[i+1:]:
            if touches(a,b):
                assert any(math.dist(j,k)<1.e-8 for j in segments[a['name']] for k in segments[b['name']]),(a['name'],b['name'])
"""
if add not in s:s=s.replace(needle,add+needle)
p.write_text(s,encoding='utf-8')
p=here/'Extract_Results.py';s=p.read_text(encoding='utf-8-sig')
s=s.replace(r"Calculation time in seconds:\s*([\d,.]+)",r"Total simulation time:\s*([\d,.]+)")
needle="    return res,(f,db),"
s=s.replace(needle,"""    res['maximum_port_extension_mm']=c['launch_length']
    res['bounding_width_mm']=res['board_width_mm']+(c['launch_length'] if geometry else 0)
    res['bounding_length_mm']=res['board_length_mm']+(0 if geometry else c['launch_length'])
    return res,(f,db),""")
p.write_text(s,encoding='utf-8')

