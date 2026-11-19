# Corporate-feed calculations

Two inset patch loads of nominal 50 Ω connected directly in parallel present 25 Ω. In Option A each approximately quarter-wave branch has nominal impedance √(50×100) = 70.71 Ω. Its input at the T is approximately 70.71²/50 = 100 Ω. Two transformed branches in parallel give 50 Ω. Option B would instead place a common √(25×50) = 35.36 Ω quarter-wave section before the T and run 50 Ω branches. The wider common section changes the available routing and needs independent full-wave validation. Option A met the operating-point objectives and was taken through full-wave development. Option B was evaluated analytically.

## Physical dimensions

For u = w/h, εeff uses (εr+1)/2 + (εr−1)/2 [(1+12/u)^−½ + δ], where δ = 0.04(1−u)² for u<1, else zero. For u<1, Z0 = (60/√εeff) ln(8/u+u/4). For u≥1, Z0 = 120π / [√εeff (u+1.393+0.667 ln(u+1.444))]. Solving these zero-thickness equations on the 0.040 mm polyimide gives the following starting values.

| Impedance (Ω) | Width (mm) | εeff | λg/4 (mm) |
|---:|---:|---:|---:|
| 50.00 | 0.09111 | 2.7493 | 0.30134 |
| 70.71 | 0.04943 | 2.6320 | 0.30799 |
| 100.00 | 0.02287 | 2.5257 | 0.31440 |
| 35.36 | 0.15212 | 2.8632 | 0.29529 |

The built trunk and 50 Ω outlet sections are 0.090 mm wide. The initial branches were 0.049 mm × 0.308 mm. Selected physical width × length is **0.055 × 0.280 mm**, giving 66.94 Ω and 82.1° on the quasi-static isolated-line approximation. At the junction y=-0.53 mm, the straight transformer extends along ±x and meets the 0.090 mm section. The nominal horizontal distance from T center to bend center is 0.600 mm. Both routed paths from T center to the inset endpoint are 1.038 mm on the centerline. The straight 50 Ω continuation, right-angle unmitered bends, finite metallization, and T overlap load the transformers. Narrow-line length includes the fraction overlapping the T. Electrical tuning used the complete connected antenna.

## Native modal check

| CST section at 150 GHz | Modal line Z (Ω) | CST effective permittivity | Propagation constant, raw Re + j Im | λg/4 from εeff (mm) |
|---|---:|---:|---|---:|
| Trunk | 49.431 | 2.83122 | 0 + j 5289.77 (Propagation Constant / 1/m) | 0.29695 |
| NominalTransformer | 68.585 | 2.67508 | 0 + j 5141.85 (Propagation Constant / 1/m) | 0.30549 |
| SelectedTransformer | 64.785 | 2.70160 | 0 + j 5167.27 (Propagation Constant / 1/m) | 0.30399 |

The mode-only diagnostics reuse the launch dielectric, ground, signal thickness, port aperture and final mesh settings. Only the strip width changes at the diagnostic cross-section. These uniform-line modal data describe the local line. The actual transformer is embedded between a T junction, a bend and a coupled patch load. Paired complex Ez exports compare the two loaded arms at equal physical reference planes.
