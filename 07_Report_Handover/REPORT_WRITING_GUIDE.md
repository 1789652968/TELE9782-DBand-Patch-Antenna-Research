# English technical report research guide

Use the official TELE9782 rubric when the original brief becomes available. Cite the current simulation record through repository-relative paths, then supply the required academic references in the submitted report.

| Section | Discuss and calculate | Evidence and figures | Confirm before submission |
|---|---|---|---|
| Introduction | 150 GHz D-band, planar fabrication, single-patch baseline and array research | [Deck](../Project_Final/06_Presentation/TELE9782_DBand_Patch_Presentation.pptx), [research log](../POST_PRESENTATION_RESEARCH_LOG.md) | Report date and official title |
| Objectives and Requirements | Directivity and plotted outputs, lecturer feedback, internal 80/90% objectives | [Requirements](../PROJECT_REQUIREMENTS_AND_OBJECTIVES.md) | Exact course wording from brief |
| Theoretical Background | TM₁₀; εeff; fringing correction; Leff≈λ₀/(2√εeff); D=4πU/Prad; mismatch | Deck appendix and [array theory](../Project_Final/07_Array_1x2/05_Documentation/Array_Design_Theory.md) | Academic source and applicability at 150 GHz |
| Initial Antenna Design | W, L, inset, dielectric and conductor, uniform launch, original and enlarged ground | [Original parameter file](../Project_Final/01_CST_Project/parameters.json), original geometry and E/H cuts in index | Specify units, nominal material assumptions |
| Setup and Methodology | Single-mode port, reference plane, boundaries, mesh, solver, farfield monitor, actual workflow | [Workflow](../TECHNICAL_WORKFLOW.md), native ModelHistory in artifacts | Independent access test to CST |
| Baseline Performance | 150 GHz gain and efficiency, resonance and match; explain native vs 50 Ω historical values | [Original comparison](../Project_Final/07_Array_1x2/03_Comparison/Common50_150GHz.csv), [summary](../01_Presentation_Baseline/Baseline_Summary.md) | Use fixed-frequency values and continuous −10 dB band |
| Radiation Efficiency Optimisation | Accepted/radiated/loss terms, PEC and lossless diagnostic controls, feed length and substrate | [Round 1 report](../Project_Final/08_Efficiency_Optimisation/09_Documentation/Efficiency_Optimisation_Report.md), Power Breakdown | Treat idealised runs as controls |
| Multi-Objective Optimisation | Real material search, failure examples, spacing/shift and finite ground, Pareto, OAT | [Round 2 report](../Project_Final/09_Multiobjective_Optimisation/10_Documentation/Final_Optimisation_Report.md), Beam and Pareto figures | Cite 39 screens and 68 trials with role labels |
| Performance Comparison | ηrad=Prad/Pacc, ηtotal=ηrad(1−\|Γ50\|²), Grealized=D+10log₁₀ηtotal, peak vs +Z | [Final CSV](../05_Final_Comparison/Tables/FINAL_VERIFIED_PERFORMANCE.csv), [design comparison](../DESIGN_COMPARISON.md) | Separate preferred submission from research extrema |
| Numerical Verification | Reopen-and-resolve, mesh convergence, power closure, spherical integral, Touchstone cross-check | [Verification JSON](../Project_Final/09_Multiobjective_Optimisation/07_Final_Candidates/Verification_Results.json), Mesh Convergence | Do not average across grids or change reference plane |
| Limitations and Future Work | Nominal Au/PI, port approximations, frequency-dependent squint, process variation, measurement pending | [Open questions](OPEN_RESEARCH_QUESTIONS.md), [frequency monitors](../Project_Final/09_Multiobjective_Optimisation/08_Results_and_Figures/Final_Frequency_Monitors.csv) | Replace assumptions if material or calibration data become available |
| Conclusion | Confirm directivity requirement, report validated efficiency and 150 GHz beam correction, justify course design | [Design decision](../DESIGN_COMPARISON.md) | Keep screen, fresh result and recommendation distinguishable |
| References | Cite course brief when obtained, antenna theory and material assumptions in the body | Deck app. G lists Balanis 4th ed., ch. 14 as historical starting reference | Confirm edition, page and a traceable D-band materials source |

[Figure and table index](FIGURE_AND_TABLE_INDEX.md)
