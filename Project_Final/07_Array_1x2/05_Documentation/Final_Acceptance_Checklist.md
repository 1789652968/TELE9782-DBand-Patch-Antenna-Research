# Acceptance record

| Check | Evidence |
|---|---|
| One physical input, two connected patches, shared board and finite gold | Geometry_Top.png, Port.png, Tree.json, native CST history |
| Physical transformers, equal arms and modal checks | Feed_Network_Calculations.md, Port_Mode_Check.json |
| Both elements excited | Branch_Balance.csv, Surface_Current_150.txt, Surface_Current_Map.png |
| Solver, reopened parameters, fresh run and re-read trace | Verification.json, state SUCCESS |
| D > 6.5 dBi and S11 ≤ −10 dB at 150 GHz | D 8.843 dBi, S11 -27.727 dB |
| Gain and radiation/total efficiencies | Final_Array_Performance.csv, 13 farfield monitors |
| E/H cuts and beamwidth | E_Plane.csv, H_Plane.csv, comparison figures |
| Same-geometry mesh comparison | Mesh_Convergence.csv, ΔD 0.0088 dB and Δf 0.053% |
| Power and farfield normalization | Power_Balance.csv, residual +2.693%, sphere mean 0.987345 |
| Original, ground control, final, both operating-point definitions | Single_vs_Array_150GHz.csv, Operating_Point_Comparison.csv |
| Full native model, companion, comparison plots and report | 01_CST_Project, 03_Comparison, Final_Report_Results.md |

Aspirational at 150 GHz: D≥9 dBi missed, Greal≥6.8 dBi met, S11≤−15 dB met, ηrad≥71.55% met. Physical measurements remain outside this simulation study.

## Port absorption and the complete power budget

At 150 GHz, counting radiation and dissipated power in gold and polyimide leaves 0.013444 W (2.693% of accepted power). The separate CST curve *Power Absorbed at all Ports* contributes 0.011725 W (2.349% of accepted power). The installed CST 2024 Help, *Power View → Power Absorbed at all Ports*, identifies this term as absorption by the waveguide-port boundary of field components outside the specified modal basis. It is distinct from outgoing fundamental-mode power and from material dissipation. The native curve is included as an independent export. The complete residual Paccepted − Prad − Pmetal − Pdielectric − Pport,abs is **+0.001720 W, or +0.345%**. No efficiency or farfield has been rescaled.

The single excited quasi-TEM mode remains the definition of the electrical input. The absorbed fraction quantifies another limitation of the finite launch and modeled port. The geometry, selected mode and unused-mode treatment were held consistent across the physical comparison. The reported radiation and total efficiencies retain this absorbed power in their denominators. See Power_Closure_By_Mesh.csv for both budgets on the selected meshes and ground controls.
