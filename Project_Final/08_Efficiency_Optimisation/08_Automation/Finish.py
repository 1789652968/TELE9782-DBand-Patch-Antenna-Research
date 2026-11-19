"""Wait for final solver checkpoints, audit native configuration and produce the deliverables."""
from Efficiency_Analysis import *
import hashlib, time
def main():
    while not (V/'verification.json').exists() or not (R/'Edge_Exports_Complete.txt').exists():time.sleep(12)
    v=read(V/'verification.json');p=Path(v['path']);hist=read(p.with_suffix('')/'Model/3D/ModelHistory.json');commands='\n'.join('\n'.join(v['code']) for v in hist['history'])
    checks={k:k in commands for k in ['.Sigma "4.561e+007"','.TanD "loss_tangent"','.Orientation "ymin"','.NumberOfModes "1"','.MonitorFarFieldsNearToModel "False"','.SteadyStateLimit "-60"','.CalculationType "TD-S"','.MeshType "PBA"','Solid.Add "antenna:trunk", "antenna:patchleft"','Solid.Add "antenna:trunk", "antenna:patchright"']}
    tree=read(p.parent/'Tree.json');params=v['parameters_read'];checks['continued_gold_conductors']=not re.search(r'Solid\.ChangeMaterial[^\n]*PEC',commands,re.I)
    checks['real_polyimide']=abs(params['loss_tangent']-.0027)<1e-9 and params['eps_r']==3.5
    checks['ground_substrate_signal_present']=all('Components\\antenna\\'+s in tree for s in ['ground','substrate','trunk'])
    logs=(p.with_suffix('')/'Result/Model.log').read_text(errors='replace').splitlines()
    dump(R/'Native_Config_Check.json',dict(checks=checks,log_evidence=[l.strip() for l in logs if any(w in l.lower() for w in ['constant approximation','number of mesh cells','energy criterion met','adaptive port meshing skipped','parallel working threads'])],port=v['ports'],monitors=v['farfield_monitors'],sample_count=len(data(p.parent/'1D Results_S-Parameters_S1,1.csv'))))
    assert all(checks.values()),checks
    from Efficiency_Analysis import main as post
    from Efficiency_Report import main as report
    post();report()
    from Efficiency_Paired_Mesh import extra
    extra()
    rr=DOC/'Efficiency_Optimisation_Report.md'; assert (DOC/'Reproduction_Guide.md').stat().st_size>500
    for img in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',rr.read_text(encoding='utf-8')):assert (DOC/img).stat().st_size>2000
    geom=read(p.parent/'parameters.json');v=read(p.parent/'completed.json')
    final=dict(path=str(p),summary=v,native_model_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),case_count=len(data(R/'All_Candidates.csv')),config_checked=True,report=str(rr))
    dump(R/'Delivery_Check.json',final);print('DELIVERY_CHECKED',p,flush=True)
if __name__=='__main__':main()

