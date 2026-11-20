# 4×4 comparison figures

All angular patterns and field quantities below come from the saved CST solutions. Units and gain reference should appear in the report captions. The derived figures can be regenerated with [Plot_Handover_Figures.py](../04_Automation/Plot_Handover_Figures.py).

| Figure | Design and range | Quantity and source | Report use |
|---|---|---|---|
| [CST geometry](../03_Comparison/Comparison_Figures/4x4_Geometry_CST.png) | Final 4×4 geometry, designed for 150 GHz | Native CST screenshot in [Native_Exports](../Native_Exports/) | Show the 16 patch board and side-fed network |
| [Corporate feed and input](Corporate_Feed_and_Port_Layout.png) | Final 4×4, x/y coordinates in mm | Plan view derived from [saved layout](../Design/Geometry_Parameters/Final_4x4/layout.json) | Identify 15 junctions and the X-min port. This is a geometry diagram |
| [50 Ω S11 sweep](../03_Comparison/Comparison_Figures/S11_50ohm.png) | Both, 130–170 GHz | dB, [common 50 Ω S11 CSVs](../02_Simulation_Results/S_Parameters/) | Discuss the 150 GHz marker and −10 dB threshold |
| [Full-sphere Directivity](../03_Comparison/Comparison_Figures/4x4_3D_Directivity.png) | 4×4, 150 GHz | dBi, [CST farfield](../Native_Exports/Farfield_150_Sphere.txt) | Show the pattern peak and orientation |
| [Full-sphere Realized Gain](../03_Comparison/Comparison_Figures/4x4_3D_Realized_Gain_50ohm.png) | 4×4, 150 GHz | dBi, CST [native gain sphere](../Native_Exports/RealizedGain_Native_150_Sphere.txt) converted to 50 Ω | Show available gain with mismatch included |
| [E-plane and H-plane](../03_Comparison/Comparison_Figures/E_H_Planes.png) | Both, 150 GHz | dBi versus signed θ in degrees, [four cut CSVs](../02_Simulation_Results/Farfield/) | Compare beamwidths and distinguish +Z from the sampled maximum |
| [Surface current](../03_Comparison/Comparison_Figures/4x4_Surface_Current_150.png) | 4×4, 150 GHz | A/m, [CST surface-current export](../Native_Exports/Surface_Current_150.txt) | Show excitation and current distribution |
| [Patch excitation probes](Patch_Excitation_150GHz.png) | 4×4, 150 GHz | Local `Ez` magnitude V/m and phase relative to circular mean in degrees, [16 probe samples](../02_Simulation_Results/Farfield/Patch_Feed_Probes_150.csv) | Net field evidence including reflections and mutual coupling |
| [Efficiency, Directivity and gain](Efficiency_Directivity_Gain_Comparison.png) | Both, 150 GHz | ηrad / ηtotal in %, Directivity and Peak / +Z Realized Gain in dBi, [comparison CSV](../03_Comparison/Array_1x2_vs_4x4_Comparison.csv) | Use in results and final design decision |
| [Absolute and normalised power loss](../03_Comparison/Comparison_Figures/Power_Absolute_and_Normalized.png) | Both, 150 GHz | mW and % Accepted, [Power Balance CSV](../02_Simulation_Results/Power_Loss/Power_Balance_150.csv) | Compare full-structure Gold, dielectric and signed port terms |
| [Mesh sensitivity](Mesh_Sensitivity_150GHz.png) | Stepped-feed 4×4, 150 GHz | Cell count, ηrad %, Directivity dBi, S11 dB, [mesh CSV](../02_Simulation_Results/Verification/Mesh_Sensitivity.csv) | Cite the two finest measured grids and the licence limitation |
