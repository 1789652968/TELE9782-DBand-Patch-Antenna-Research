"""Close the full CST power budget including absorbed unrepresented port fields."""
from Array_Results_Extraction import *
def budget(folder,base):
    power=r'1D Results\Power\Excitation [1]\Power Absorbed at all Ports'
    x,y=load_curve(raw(folder),power);out=[]
    for v in base:
        v=dict(v);pa=np.interp(v['f_GHz'],x,y.real);rem=v['power_balance_residual_W']-pa
        v.update(Pport_unrepresented_modes_absorbed_W=pa,residual_before_port_absorption_W=v['power_balance_residual_W'],closed_power_residual_W=rem,closed_power_residual_pct_accepted=100*rem/v['Paccepted_W'])
        out.append(v)
    return out
def main():
    checks=budget(P,read(P/'numerical_audit.json')['farfield_checks']);write(R/'Power_Balance.csv',checks)
    history=[];paths=[ORIG,W/'GroundControl']
    model=read(W/'engineering_selection.json');paths += [W/model['previous_mesh'],W/model['selected_mesh'],W/'MeshHoldout',P]
    for d in paths:
        a=read((ORIG/'numerical_audit.json') if d==ORIG else (d/'numerical_audit.json')) if (d/'numerical_audit.json').exists() else audit(d)
        row=next(v for v in budget(d,a['farfield_checks']) if v['f_GHz']==150);history.append(dict(case=('Original' if d==ORIG else d.name),**row))
    write(R/'Power_Closure_By_Mesh.csv',history)
    v=next(v for v in checks if v['f_GHz']==150);diff=100*v['Pport_unrepresented_modes_absorbed_W']/v['Paccepted_W']
    note=f"""## Port absorption and the complete power budget

At 150 GHz, counting radiation and dissipated power in gold and polyimide leaves {v['residual_before_port_absorption_W']:.6f} W ({v['power_balance_residual_percent_accepted']:.3f}% of accepted power). The separate CST curve *Power Absorbed at all Ports* contributes {v['Pport_unrepresented_modes_absorbed_W']:.6f} W ({diff:.3f}% of accepted power). The installed CST 2024 Help, *Power View → Power Absorbed at all Ports*, identifies this term as absorption by the waveguide-port boundary of field components outside the specified modal basis. It is distinct from outgoing fundamental-mode power and from material dissipation. The native curve is included as an independent export. The complete residual Paccepted − Prad − Pmetal − Pdielectric − Pport,abs is **{v['closed_power_residual_W']:+.6f} W, or {v['closed_power_residual_pct_accepted']:+.3f}%**. No efficiency or farfield has been rescaled.

The single excited quasi-TEM mode remains the definition of the electrical input. The absorbed fraction quantifies another limitation of the finite launch and modeled port. The geometry, selected mode and unused-mode treatment were held consistent across the physical comparison. The reported radiation and total efficiencies retain this absorbed power in their denominators. See Power_Closure_By_Mesh.csv for both budgets on the selected meshes and ground controls."""
    (DOC/'Port_Power_Closure.md').write_text(note+'\n',encoding='utf-8')
    for name in ['Simulation_Validation.md','Final_Report_Results.md','Final_Acceptance_Checklist.md']:
        f=DOC/name;text=f.read_text(encoding='utf-8')
        if '## Port absorption and the complete power budget' not in text:
            if name=='Final_Report_Results.md':text=text.replace('## Limitations',note+'\n\n## Limitations')
            else:text+='\n'+note+'\n'
            f.write_text(text,encoding='utf-8')
if __name__=='__main__':main()

