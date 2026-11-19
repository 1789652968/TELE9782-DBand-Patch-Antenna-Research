"""Verify configuration from the actual saved companion history and final solver logs."""
from Array_Results_Extraction import *
def main():
    model=P/'TELE9782_DBand_1x2_Array_Final';hist=read(model/'Model/3D/ModelHistory.json')['history']
    commands='\n'.join('\n'.join(h['code']) for h in hist)
    tokens=['.Sigma "4.561e+007"','.Epsilon "eps_r"','.TanD "loss_tangent"','.TanDFreq "150"','.MeshType "PBA"','.MonitorFarFieldsNearToModel "False"','.SteadyStateLimit "-60"','.CalculationType "TD-S"','.Orientation "ymin"','.PortNumber "1"','.NumberOfModes "1"','.Ymin "open"','Solver.FrequencyRange "130", "170"','Solver.AutoNormImpedance "True"','Solver.NormingImpedance "50"']
    for side in ['left','right']:
        for part in ['patch','feed','bend','xf']:tokens.append(f'Solid.Add "antenna:trunk", "antenna:{part}{side}"')
    hchecks={s:(s in commands) for s in tokens}
    mlog=(model/'Result/Model.log').read_text(errors='replace')
    actual={s:s in mlog for s in ['Steady state energy criterion met, solver finished successfully.','Perfect Boundary Approximation (PBA)']}
    tree=read(R/'Tree.json')
    per={}
    for f in [130,140,*range(146,155),160,170]:
        per[str(f)]='Farfields\\farfield (f='+str(f)+') [1]' in tree
    payload=dict(native_commands=hchecks,solver_log=actual,readable_farfields=per,files=['Model/3D/ModelHistory.json','Result/Model.log'],material_definition_source=str(model/'Model/3D/ModelHistory.json'))
    (R/'Saved_Model_Configuration_Check.json').write_text(json.dumps(payload,indent=2))
    assert all(hchecks.values()) and all(actual.values()) and all(per.values()),payload
if __name__=='__main__':main()
