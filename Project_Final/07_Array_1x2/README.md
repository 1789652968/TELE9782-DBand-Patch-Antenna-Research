# TELE9782 · 150 GHz corporate-fed 1×2 array

Open [the engineering report](05_Documentation/Final_Report_Results.md) for the design, evidence, three-way comparison and conclusions. Start in CST Studio Suite 2024 with [the final native project](01_CST_Project/TELE9782_DBand_1x2_Array_Final.cst). Keep its same-stem results folder adjacent if transferring the project.

## Reproduce the delivered result in CST

1. In CST 2024 select File → Open and choose the final file above. The assembled signal body, ground and dielectric are under Components → antenna. Inspect the geometry history for the T and the two inset cuts.
2. Under Ports select port 1. Under Simulation inspect the 130–170 GHz transient setup and single-mode excitation. The model history requests 50 Ω. The saved S1,1 trace uses the solved port reference. For the exact 50 Ω trace use CST_50ohm.s1p exported by CST with Renormalize enabled. The original archived single used its solved modal reference.
3. Make a native Save As copy in a fresh working folder if preserving the checked deliverable, including results. Use Simulation → Start Simulation and run the time-domain solver. On completion inspect 1D Results → S-Parameters → S1,1 and Farfields → farfield (f=150) [1].
4. For the 3D pattern select total directivity or realized gain and a full sphere. Use YZ for E and XZ for H. Open 2D/3D Results → Surface Current → surface current (f=150) [1] for the current distribution. Local Ez pairs used in verification are under 02_Simulation_Results.
5. The reopened-project evidence and original-to-common-reference check are in [Verification.json](02_Simulation_Results/Verification.json) and [Reference_Comparison.json](02_Simulation_Results/Reference_Comparison.json). Matched bandwidth uses interpolated −10 dB crossings on the broadband trace.

## Contents

- [01_CST_Project](01_CST_Project) · final native CST project, its results companion and source numeric exports.
- [02_Simulation_Results](02_Simulation_Results) · solver curves, patterns, power, balance and numerical verification. [Manifest](02_Simulation_Results/Delivery_Manifest.csv) lists file lengths and SHA-256 hashes of the principal deliverables.
- [03_Comparison](03_Comparison) · original single, enlarged-ground single and final array at the same frequency and at the best available matched samples.
- [04_Automation](04_Automation/README.md) · build, solve, postprocess and reproduce.
- [05_Documentation](05_Documentation) · report, theory, validation and acceptance checklist.
- [06_Working](06_Working) · solver projects, intermediate numerical exports and run logs. The selected initial screening geometry was Transformer, final validated mesh source Refined, and exact-reference production source Final50.

The comparison reads the original validated single from the sibling directory ../02_Simulation_Results. Keep the array directory under Project_Final when regenerating the plots.