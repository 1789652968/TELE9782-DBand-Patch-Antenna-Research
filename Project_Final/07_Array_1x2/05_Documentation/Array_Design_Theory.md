# Array design theory

The assignment requires directivity above 6.5 dBi in 130–170 GHz. The validated single inset-fed patch supplies the starting element. Its width is 0.667 mm, its length is 0.513 mm, and its inset is 0.190 mm. We keep its metals, substrate and polarization to make a meaningful comparison at 150 GHz.

## Resonant length

The transmission-line estimate uses W = c/(2f) sqrt(2/(εr+1)), effective permittivity εeff = (εr+1)/2 + (εr−1)/(2 sqrt(1+12h/W)), and open-edge extension ΔL/h = 0.412 (εeff+0.3)(W/h+0.264) / ((εeff−0.258)(W/h+0.8)). At 150 GHz this gives W = 0.6662 mm and L ≈ 0.5204 mm. For the selected array element W = 0.667 mm, L = 0.513 mm, εeff = 3.2032 and ΔL = 0.01900 mm. The half-wave estimate c/[2(L+2ΔL)√εeff] gives **152.00 GHz**. The full assembled antenna has minimum S11 at **149.80 GHz**, a difference of 2.20 GHz (1.45% of estimate). The S11 minimum characterises impedance matching of the driven assembly. Coupled elements, bends, transformers and finite ground affect this frequency.

## Aperture and beam

Elements occupy x = ±0.6 mm with the same y coordinate and orientation. At 150 GHz λ0 = 1.9986 mm. The initial spacing of 1.00 mm corresponds to 0.500λ0. The selected 1.20 mm spacing is 0.600λ0, leaving an edge gap of 0.533 mm and a side clearance of 0.317 mm on each side. For in-phase excitations the ideal two-source array factor is 2 cos(πd sinθ cosφ/λ0). In XZ it varies with angle. In YZ it is constant. This predicts the plane most likely to narrow. All reported pattern values instead come from the full CST model with finite ground and feed scattering. Broadside y polarisation is checked using Eφ and Eθ at θ=0°, φ=0° in the angular export.

A doubled number of radiators alone does not determine the change in realized gain. Directivity normalizes angular radiation by radiated power. Multiplication by radiation efficiency and accepted-power fraction converts it to realized gain. The three-model comparison separates ground-size and excitation effects to the extent supported by one enlarged-ground control.
