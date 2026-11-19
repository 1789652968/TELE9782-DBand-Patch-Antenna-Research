from pathlib import Path
p=Path(__file__).with_name('Round2_Search.py');s=p.read_text(encoding='utf-8')
s=s.replace("    if not viable:\n        others=", """    # Replace failed nominations individually, so a missing high-efficiency role is not masked by a passing broadside model.
    for role,initial in pre.items():
        if stable(tested[initial['name']]) or len(tested)>=len(chosen)+2:continue
        remaining=[v for v in coarse if good(v) and v['name'] not in tested and v['name']!='Control20']
        if not remaining:continue
        alt=roles(remaining)[role];tested[alt['name']]=validate(alt['name'],alt);dump(V/'Verification_Results.json',tested)
    viable=[t['fresh'] for t in tested.values() if stable(t)]
    if not viable:
        others=""")
p.write_text(s,encoding='utf-8')

