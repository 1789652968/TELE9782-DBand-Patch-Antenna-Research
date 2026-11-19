from pathlib import Path
d=Path(__file__).resolve().parent;p=d/'Round2_Port.py';s=p.read_text(encoding='utf-8-sig')
old="    assert any('140 ghz' in s.lower() for s in messages),messages"
new="""    ref_log=next(Path(ref['path']).glob('*/Result/Model.log')).read_text(errors='replace')
    controls=[s.strip() for s in ref_log.splitlines() if 'F-Calc 150' in s];perturbed=[s.strip() for s in log.splitlines() if 'F-Calc 140' in s]
    assert controls and perturbed and any('150 ghz' in s.lower() for s in messages)
"""
s=s.replace(old,new).replace('native_evidence=messages[-2:]','native_evidence=controls[-1:]+perturbed[-1:]+messages[-1:],mode_solver_control_GHz=150,mode_solver_perturbation_GHz=140,material_approximation_GHz=150')
p.write_text(s,encoding='utf-8')
p=d/'Explain_Final_Losses.py';s=p.read_text(encoding='utf-8-sig')
s=s.replace('该试验只检验模式频率设置的敏感性，','CST 日志的 F-Calc 分别为 150 和 140；两次计算都在 150 GHz 对端口截面材料取常量近似。该试验只检验模式频率设置的敏感性，')
p.write_text(s,encoding='utf-8')

