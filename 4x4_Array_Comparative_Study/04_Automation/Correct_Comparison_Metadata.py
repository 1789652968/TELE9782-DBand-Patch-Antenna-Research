"""Correct derived centreline metadata and make the recovered export scope explicit."""
from pathlib import Path
import json, math
root=Path(__file__).resolve().parents[1];auto=root/'04_Automation'
f=auto/'Build_4x4.py'
s=f.read_text(encoding='utf-8-sig').replace('for i,a in enumerate(lines):','for index,a in enumerate(lines):').replace('for b in lines[i+1:]:','for b in lines[index+1:]:')
f.write_text(s,encoding='utf-8')
for p in (root/'01_CST_Project').glob('*/layout.json'):
    d=json.loads(p.read_text());c=json.loads((p.parent/'parameters.json').read_text())
    xc=[x['x'] for x in d['patches']];yc=[x['y'] for x in d['patches']]
    pitch_x=(max(xc)-min(xc))/3;pitch_y=(max(yc)-min(yc))/3
    path=(c['first_split_x']-d['port_x'])+pitch_y+(c['row_split_x']-c['first_split_x'])+pitch_y/2-c['row_split_x']
    path+=c['inlet_rail_separation']+pitch_x+c['stage3_separation']+pitch_x/2+c['stage4_offset']-c['patch_length']/2+c['inset_length']
    assert 6<path<10
    if not math.isclose(d['equal_path_to_inset_mm'],path,abs_tol=1e-10):
        d['equal_path_to_inset_mm']=path
        p.write_text(json.dumps(d,indent=2),encoding='utf-8')
for n in ('Licensed_23_33_4x4','Final_4x4'):
    f=root/'01_CST_Project'/n/'Export_Complete.json';e=json.loads(f.read_text())
    e['wall_scope']='export_only';e['native_solver_run_reused']=True
    f.write_text(json.dumps(e,indent=2),encoding='utf-8')
f=auto/'Run_4x4.py';s=f.read_text(encoding='utf-8-sig')
s=s.replace("wall_seconds=round(time.time()-start,1)))", "wall_seconds=round(time.time()-start,1),wall_scope='export_only' if extract else 'solve_and_export',native_solver_run_reused=extract))")
f.write_text(s,encoding='utf-8')
f=auto/'Extract_Results.py';s=f.read_text(encoding='utf-8-sig').replace("run_plus_export_wall_seconds=ver.get('wall_seconds'),",
"run_plus_export_wall_seconds=ver.get('wall_seconds') if ver.get('wall_scope')!='export_only' else None,\n        recovered_export_wall_seconds=ver.get('wall_seconds') if ver.get('wall_scope')=='export_only' else None,")
f.write_text(s,encoding='utf-8')
f=auto/'Write_Reports.py';s=f.read_text(encoding='utf-8-sig')
s=s.replace("('Port absorption','port_absorption_W')","('Port absorption, native signed entry','port_absorption_W')")
s=s.replace("power+=f\"| {title}", "power+=f\"| {title}")
needle="    dc=b['radiation_efficiency_pct']-a['radiation_efficiency_pct']"
s=s.replace(needle,"""    port_en=''
    port_cn=''
    if b['port_absorption_W']<0:
        no_port=b['balance_residual_W']+b['port_absorption_W']
        port_en=f"The native 4×4 port-absorption term is signed at {b['port_absorption_W']*1e3:.3f} mW. A passive port cannot dissipate negative power. We retain the solver value as a numerical port-balance term. The closure difference from radiated, metal and dielectric terms alone is {no_port*1e3:.3f} mW ({100*no_port/b['accepted_W']:.3f}% of accepted power)."
        port_cn=f"CST 的 4×4 Port Absorption 原始项为 {b['port_absorption_W']*1e3:.3f} mW。无源端口的物理耗散应为非负，因此此值按带符号的数值平衡项保留。从接受功率扣除辐射、金属和介质项后的差额为 {no_port*1e3:.3f} mW。"
"""+needle)
s=s.replace("The gold, dielectric and port-loss fractions change by {dm:+.3f}, {dp:+.3f} and {dl:+.3f} percentage points respectively.","The gold and dielectric accepted-power fractions change by {dm:+.3f} and {dp:+.3f} percentage points. {port_en}")
s=s.replace("金属、介质和端口吸收占接受功率的变化为 {dm:+.2f}、{dp:+.2f}、{dl:+.2f} 个百分点。","金属、介质损耗占接受功率的比例分别变化 {dm:+.2f}、{dp:+.2f} 个百分点。{port_cn}")
f.write_text(s,encoding='utf-8')

