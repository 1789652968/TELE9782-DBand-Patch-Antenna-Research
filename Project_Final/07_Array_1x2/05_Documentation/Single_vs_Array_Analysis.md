# Single versus array

## Engineering conclusion at 150 GHz

The final array achieves **8.843 dBi peak directivity** and **7.408 dBi peak realized gain**, compared with 7.460 and 5.804 dBi for the original. Relative to the single patch these are +1.383 dB and +1.603 dB. Peak radiation intensity at the same available input power changes by a factor of 1.447. The original already met the 6.5 dBi assignment. The measured change in H-plane beamwidth is -30.96° and in E-plane width +21.26°.

Radiation efficiency changes by +0.43 percentage points and total efficiency by +3.56 points. The small nominal radiation-efficiency advantage over the original is smaller than the observed mesh variation and does not establish a robust efficiency improvement. Native S11 changes by -14.30 dB. The −10 dB bandwidth changes by +0.634 GHz. The two-patch board occupies 3.75 mm² of main ground compared with 1.96 mm² originally. An implementation aimed at peak link gain and H-plane spatial selectivity benefits from the array. The original has a smaller footprint and a simpler, straight feed. Neither result has been validated on fabricated hardware.

## Fixed-frequency comparison

| Metric | Original | Enlarged single | Final array | Array − original |
|---|---|---|---|---|
| Dmax_dBi | 7.460 | 7.963 | 8.843 | 1.383 |
| D_broadside_dBi | 7.428 | 7.686 | 8.841 | 1.413 |
| realized_gain_dBi | 5.804 | 6.614 | 7.408 | 1.603 |
| S11_dB | -13.424 | -27.320 | -27.727 | -14.303 |
| S11_50_dB | -13.476 | -27.043 | -27.802 | -14.327 |
| realized_50_dBi | 5.807 | 6.614 | 7.408 | 1.601 |
| rad_eff_pct | 71.553 | 73.429 | 71.981 | 0.428 |
| total_eff_pct | 68.301 | 73.293 | 71.860 | 3.559 |
| fmin_GHz | 148.840 | 149.880 | 149.800 | 0.960 |
| f_low_GHz | 147.106 | 148.160 | 147.596 | 0.490 |
| f_high_GHz | 150.619 | 151.630 | 151.743 | 1.124 |
| BW_GHz | 3.513 | 3.470 | 4.147 | 0.634 |
| FBW_percent | 2.360 | 2.315 | 2.771 | 0.411 |
| E_HPBW_deg | 83.266 | 74.448 | 104.529 | 21.262 |
| H_HPBW_deg | 74.010 | 74.956 | 43.051 | -30.959 |
| theta_deg | 4.000 | 10.000 | 2.000 | -2.000 |
| phi_deg | 264.000 | 268.000 | 82.000 | -182.000 |

Footprint including the launch is 2.21 mm² (original) and 4.00 mm² (array). The main beam lies 2° from +z at φ=82° on the sampled array sphere. Broadside realized gain is 7.406 dBi. Among several near-equal angular samples, peak azimuth is precision-sensitive near the pole. The E-plane −3 dB crossings are -47.24° and 57.29°. H-plane crossings are -21.52° and 21.53°, interpolated between adjacent 2° samples relative to each cut's own peak. Angular CSVs retain all rear lobes and nulls. The plots clip the ordinate below their displayed floor.

Changing only the single-patch board size and feed extension changed peak directivity by +0.503 dB and realized gain by +0.810 dB. Adding the complete two-patch design on that board changed them by a further +0.880 and +0.794 dB. This control identifies the board contribution with the single radiator. Interactions make a unique element-only decomposition impossible.

The original and array dissipate respectively 0.08954 and 0.08528 W in metal, and 0.04264 and 0.04113 W in dielectric, at the common 0.5 W stimulated normalization. The solver records whole-antenna dissipation. It does not isolate T-junction loss. The feed and coupling change input impedance and stored fields. Distinct dissipation and mismatch contributions can therefore move in different directions.

## Handpicked operating point versus extrema

| design | criterion | f_GHz | S11_dB | Dmax_dBi | realized_gain_dBi |
|---|---|---|---|---|---|
| Original single patch | Best realized gain among matched monitors | 149.000 | -30.146 | 7.410 | 5.982 |
| Original single patch | Highest gain among all monitors | 149.000 | -30.146 | 7.410 | 5.982 |
| Original single patch | Highest directivity among all monitors | 154.000 | -3.444 | 7.570 | 3.088 |
| Single on array ground | Best realized gain among matched monitors | 150.000 | -27.320 | 7.963 | 6.614 |
| Single on array ground | Highest gain among all monitors | 150.000 | -27.320 | 7.963 | 6.614 |
| Single on array ground | Highest directivity among all monitors | 151.000 | -13.495 | 7.970 | 6.404 |
| Corporate-fed array | Best realized gain among matched monitors | 149.000 | -17.996 | 8.950 | 7.515 |
| Corporate-fed array | Highest gain among all monitors | 149.000 | -17.996 | 8.950 | 7.515 |
| Corporate-fed array | Highest directivity among all monitors | 140.000 | -2.871 | 9.224 | 4.351 |

The selection criterion above uses realized gain at genuinely simulated monitors satisfying S11 ≤ −10 dB. The lowest broadband S11 occurs at 148.84 GHz (single) and 149.80 GHz (array). The two selections and the minima answer different questions. Lines on frequency plots connect discrete farfield monitor solutions.

## Spacing, coupling and excitation

| case | spacing_mm | Zre150_ohm | Zim150_ohm | fmin_GHz | H_HPBW_deg | left_patch_Krms_A_per_m | right_patch_Krms_A_per_m |
|---|---|---|---|---|---|---|---|
| Spacing90 | 0.900 | 55.184 | -3.246 | 150.120 | 53.124 | 57.243 | 57.153 |
| Transformer | 1.000 | 40.821 | -8.012 | 151.040 | 49.594 | 54.561 | 54.475 |
| Spacing110 | 1.100 | 29.821 | -2.603 | 151.880 | 46.250 | 52.230 | 52.179 |
| Spacing120 | 1.200 | 23.898 | 5.225 | 152.320 | 43.212 | 48.805 | 48.819 |
| Spacing130 | 1.300 | 24.689 | 13.589 | 152.120 | 40.557 | 49.644 | 49.573 |
| 02_Simulation_Results | 1.200 | 49.801 | -4.063 | 149.800 | 43.051 | 198.452 | 199.322 |

The coarse spacing comparison retains common ground, inset, transformer and vertical feed dimensions. Increasing spacing lengthens each horizontal 50 Ω continuation by half the change in spacing. The measured change in Zin, resonance, current and radiation therefore includes mutual fields and routing changes. A one-port antenna has no independent external element-to-element S21. The exported local Ez values originate at four matched reference-plane pairs 0.020 mm above the ground. The maximum absolute final right/left amplitude difference is **0.0026 dB**, and phase difference **0.034°**. These are loaded local field ratios. They support balanced excitation without assigning independently calibrated forward powers to the branches. The current table averages |K|² over equal central patch rectangles, using the native facet areas at the top metal surface.

Among the final forward cut samples, the strongest additional local maximum relative to the H-cut peak is -17.16 (dB if present). The E-cut value is absent. These checks apply to the sampled principal cuts. The global maximum and full 3D sphere also establish the main-beam direction.

### Resonance retuning and the production choice

The 1.20 mm screening case gave 9.175 dBi and -8.96 dB S11 at 150 GHz. Increasing its patch length to 0.513 mm produced 9.050 dBi, 7.650 dBi realized gain and -16.25 dB S11 on the same coarse grid. The finer-grid comparison selected **Refined** as the physical production source. The Final50 production source retained its geometry and resolution. The jump from 218,776 to 474,240 cells changed peak directivity by 0.233 dB and the minimum-S11 frequency by 1.56 GHz. An independently solved 38/57 holdout grid checks the stability of the 36/54 production mesh. Mesh_Convergence.csv contains every grid on this geometry, including the earlier nonmonotonic shift. Independently re-referencing the freshly solved broadband trace to 50 Ω recovers the CST-native 50 Ω Touchstone export with maximum complex reflection error 6.9088e-08.

### Common 50 Ω reference, 150 GHz

| Design | S11 dB | D dBi | Greal dBi | ηrad % | ηtotal % |
|---|---|---|---|---|---|
| Original | -13.476 | 7.460 | 5.807 | 71.553 | 68.339 |
| Enlarged ground | -27.043 | 7.963 | 6.614 | 73.429 | 73.284 |
| Final array | -27.802 | 8.843 | 7.408 | 71.981 | 71.862 |

### Final array monitor samples

| GHz | S11 dB | D dBi | Greal dBi | ηrad % | ηtotal % |
|---|---|---|---|---|---|
| 130.000 | -1.716 | 9.012 | 1.572 | 55.241 | 18.028 |
| 140.000 | -2.871 | 9.224 | 4.351 | 67.317 | 32.561 |
| 146.000 | -6.502 | 9.156 | 6.705 | 73.252 | 56.862 |
| 147.000 | -8.355 | 9.105 | 7.088 | 73.608 | 62.857 |
| 148.000 | -11.493 | 9.038 | 7.385 | 73.575 | 68.358 |
| 149.000 | -17.996 | 8.950 | 7.515 | 73.030 | 71.871 |
| 150.000 | -27.727 | 8.843 | 7.408 | 71.981 | 71.860 |
| 151.000 | -13.955 | 8.717 | 7.021 | 70.500 | 67.664 |
| 152.000 | -9.021 | 8.581 | 6.364 | 68.616 | 60.020 |
| 153.000 | -6.281 | 8.442 | 5.491 | 66.304 | 50.693 |
| 154.000 | -4.598 | 8.307 | 4.491 | 63.590 | 41.530 |
| 160.000 | -1.482 | 7.379 | -1.277 | 47.144 | 13.626 |
| 170.000 | -0.842 | 4.863 | -7.378 | 33.863 | 5.969 |

These are maxima over angle at each stated monitor frequency. The 150 GHz fixed comparison uses independently calculated angular cuts and broadside data. The broadband S11 trace has 1001 samples.
