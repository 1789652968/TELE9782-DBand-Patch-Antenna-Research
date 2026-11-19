"""Independent port-frequency checks for balanced and high-efficiency designs: physical launch fixed."""
from Round2_Search import *
import Round2_Core as core
def check(winner,ref,output):
    stage=A/'Numerical_Port_Check';stage.mkdir(exist_ok=True)
    cfg=read_params(winner)|dict(mesh_near=20,mesh_box=30,mode_factor=.25)
    assert all(read_params(Path(ref['path']))[k]==v for k,v in cfg.items() if k!='mode_factor')
    prior=core.decorate
    def numerical(m,c):
        prior(m,c);m.add_to_history('Numerical port frequency control','Solver.SetModeFreqFactor ".25"')
    core.decorate=numerical
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:q=run(de,stage,'Mode140_'+winner.parent.name,cfg,'port_numerical_check')
    finally:de.close();core.decorate=prior
    log=next(Path(q['path']).glob('*/Result/Model.log')).read_text(errors='replace')
    messages=[s.strip() for s in log.splitlines() if 'constant approximation' in s.lower()]
    ref_log=next(Path(ref['path']).glob('*/Result/Model.log')).read_text(errors='replace')
    controls=[s.strip() for s in ref_log.splitlines() if 'F-Calc 150' in s];perturbed=[s.strip() for s in log.splitlines() if 'F-Calc 140' in s]
    assert controls and perturbed and any('150 ghz' in s.lower() for s in messages)

    dump(output,dict(nominal=ref,perturbed=q,native_evidence=controls[-1:]+perturbed[-1:]+messages[-1:],mode_solver_control_GHz=150,mode_solver_perturbation_GHz=140,material_approximation_GHz=150,delta={k:q[k]-ref[k] for k in ['eta','eta_total50','G0','theta','S11_50','Pport','residual_pct']}))
def main():
    choice=json.loads((V/'Final_Selection.json').read_text());tested=json.loads((V/'Verification_Results.json').read_text())
    if 'Best_Balanced' not in choice:return
    best=Path(choice['Best_Balanced']);top=Path(choice['Highest_Efficiency'])
    nom=Path(json.loads((R/'Selected_Sensitivity_Study.json').read_text())['path'])/'Nominal'
    if top!=best:check(top,tested[top.parent.name]['screen'],R/'Highest_Efficiency_Port_Check.json')
    check(best,json.loads((nom/'round2.json').read_text()),R/'Port_Mode_Sensitivity.json')
if __name__=='__main__':main()

