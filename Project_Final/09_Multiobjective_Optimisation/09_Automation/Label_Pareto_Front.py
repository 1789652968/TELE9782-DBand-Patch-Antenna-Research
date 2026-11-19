from pathlib import Path
p=Path(__file__).with_name('Round2_Report.py');s=p.read_text(encoding='utf-8-sig')
needle="    for q in [v['fresh'] for v in vset.values()]:plt.scatter(q['theta'],q['eta'],s=130,marker='*',label=q['name'])"
if needle in s:
    s=s.replace(needle,"""    front=[q for q in eligible if q['pareto_same_screen_grid']]
    if front:plt.scatter([q['theta'] for q in front],[q['eta'] for q in front],s=90,facecolors='none',edgecolors='#20262b',linewidths=.85,label='Screen: nondominated across 8 objectives')
"""+needle)
    p.write_text(s,encoding='utf-8')

