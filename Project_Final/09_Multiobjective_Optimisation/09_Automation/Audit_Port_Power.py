from pathlib import Path
p=Path(__file__).with_name('Round2_Report.py');s=p.read_text(encoding='utf-8-sig')
needle='    out=dict(final_boundary='
addition='''    native_gamma=(complex(q['Rin'],q['Xin'])-q['Zref'])/(complex(q['Rin'],q['Xin'])+q['Zref'])
    accepted_closure=q['Pin']-q['Pout']-q['Pacc']
    reflected_power_identity=q['Pout']/q['Pin']-abs(native_gamma)**2
    assert abs(accepted_closure)/q['Pin']<.0001 and abs(reflected_power_identity)<.0001
'''
if '    accepted_closure=' not in s:
    s=s.replace(needle,addition+"    out=dict(stimulated_minus_outgoing_minus_accepted_W=accepted_closure,outgoing_fraction_minus_native_reflection=reflected_power_identity,final_boundary=")
p.write_text(s,encoding='utf-8')

