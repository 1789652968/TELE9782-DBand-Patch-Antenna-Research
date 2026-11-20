from pathlib import Path
p=Path(__file__).resolve().parent
report=p/'Write_Reports.py';x=report.read_text(encoding='utf-8-sig')
needle="    trials='| Screen case"
i=x.index(needle)
x=x[:i]+"""    lic=read(V/'License_Constraint.json')
    license_note=f"CST rejected the attempted 26/39 grid before time stepping because the installed license caps the model at {lic['maximum_mesh_cells']:,} mesh cells. The successful 4×4 resolution and mesh-sensitivity data above reflect that constraint. They support comparison of these validated models, with a finer-grid extrapolation beyond the licensed limit still untested."
"""+x[i:]
x=x.replace("{criterion} The final geometry", "{criterion} {license_note} The final geometry")
x=x.replace("{criterion}\n\n[英文","{criterion} 本机 CST 的许可证上限为 100 万单元，26/39 设置在求解前被拒绝并保留原生错误记录。下方为许可范围内的实际网格复核。\n\n[英文")
x=x.replace("Their phase and magnitude include coupling and reflected waves.","Their phase and magnitude include coupling and reflected waves. The largest phase deviation from the circular mean was {q['maximum_abs_relative_phase_deg']:.1f}°.")
x=x.replace("The study supports retaining the validated 1×2 as the established course delivery when those demonstrated metrics and implementation simplicity define the objective.", "The 1×2 remains an established course delivery for broadly matched operation and a compact implementation. The result supports using the complete performance table to select a design when realized gain or beam width dominates.")
report.write_text(x,encoding='utf-8')

