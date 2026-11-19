# 150 GHz beam-squint diagnosis

The delivery archive and the round-two backup have identical SHA256. The audit uses the complete CST 2024 results, the native 2° theta/phi full-sphere export, and complex surface-current and electric-field exports. The two patch centers lie on X at ±0.560 mm. The waveguide port and common feed enter from −Y. Theta is measured from +Z; phi is measured from +X toward +Y.

| Quantity | Saved 82.99% delivery |
|---|---:|
| Native peak directivity | 9.1400 dBi |
| Sampled peak direction | theta 16°, phi 90°, in the YZ (E) plane |
| Directivity / realized gain (50 ohm) at +Z | 8.659 / 7.763 dBi |
| Peak realized gain (50 ohm) | 8.244 dBi |
| E/H half-power beamwidth | 88.22° / 48.06° |
| +/-Z axial front/back | 19.17 dB |
| Directivity sphere integral / 4π | 1.000706 |

At four mirrored feed locations the largest right/left Ez difference is 0.000907 dB and 0.001151°. The area-weighted longitudinal current in 3 mirrored feed windows differs by up to 0.2411 dB and 0.3781°. The current windows combine sampled facets within each stated region, so the estimate depends on spatial sampling. These are local phasors; neither method separates forward and reflected waves. See the two paired CSVs in 02_Diagnostics.

The measured imbalance across X is too small to explain a 16° tilt along Y. The complete aperture includes the one-sided launch, divider, inset slots and fields scattered by the finite substrate and ground. Their Y asymmetry can change the E-plane phase distribution while preserving left/right symmetry. The pattern alone cannot uniquely allocate the tilt between them. Controlled geometric perturbations are tabulated separately at the same mesh setting.

The highest regional sampled RMS surface current is inset contact (593.1 A/m). Regions are diagnostic windows, may overlap, and do not partition metal loss. Compare the solver's integrated loss in metals between runs. The baseline allocates 7.95% of accepted power to gold, 5.57% to polyimide, 3.13% to port absorption and 0.356% to the remaining closure residual.

## Controlled perturbations

| Coarse trial | ηrad (%) | Dmax (dBi) | G+Z (dBi) | theta (°) | phi (°) | S11 (dB) |
| --- | --- | --- | --- | --- | --- | --- |
| Control20 | 84.571 | 9.177 | 7.794 | 18.000 | 90.000 | -14.511 |
| RearShort | 82.793 | 8.538 | 7.542 | 2.000 | 86.000 | -14.060 |
| RearLong | 84.272 | 9.202 | 6.930 | 26.000 | 90.000 | -13.894 |
| WideGround | 84.588 | 9.355 | 7.885 | 18.000 | 90.000 | -14.617 |
| Compact | 71.363 | 9.420 | 4.345 | 10.000 | 90.000 | -2.641 |
| FeedShiftMinus | 82.659 | 9.860 | 7.540 | 24.000 | 90.000 | -16.209 |
| FeedShiftPlus | 85.017 | 8.369 | 7.425 | 12.000 | 270.000 | -15.236 |
| IntermediateRearEdge | 83.451 | 8.566 | 7.630 | 4.000 | 86.000 | -15.436 |
| NearRearEdge | 82.749 | 8.721 | 7.543 | 2.000 | 86.000 | -11.197 |
| WideApertureBroadside | 74.687 | 6.584 | -1.592 | 48.000 | 90.000 | -3.418 |
| MovedWideAperture | 64.988 | 6.180 | 0.028 | 44.000 | 90.000 | -3.833 |
| RearCoupledShort | 85.108 | 10.080 | 7.758 | 24.000 | 88.000 | -18.095 |
| RearCoupledResonant | 80.397 | 8.763 | 5.088 | 34.000 | 90.000 | -11.361 |

In the rear-edge experiment the signal network, branch lengths and port plane are unchanged. The large shift in YZ with the rear edge establishes finite-ground/substrate sensitivity. Because the dielectric and gold footprints change together, the experiment cannot separate dielectric edge scattering from ground-edge current. Offsets use a 2° sphere. Near +Z the azimuth is poorly conditioned. Peak directions in a given single-port solution are common to directivity and realized gain because the efficiency factor is a positive angle-independent scalar.

## Near-edge field asymmetry

| Model | Patch | +Y / −Y |Ez| (dB) | Arg(Ez,+Y / Ez,−Y) (°) |
| --- | --- | --- | --- |
| PreviousArray | left | -1.042 | -176.952 |
| PreviousArray | right | -1.042 | -176.952 |
| FirstOptimised | left | -1.443 | -177.395 |
| FirstOptimised | right | -1.443 | -177.396 |
| ShiftBracket85_Delivery | left | -1.229 | -178.443 |
| ShiftBracket85_Delivery | right | -1.229 | -178.435 |
| H085_Delivery | left | -1.190 | -178.252 |
| H085_Delivery | right | -1.191 | -178.244 |
| ShiftNull75_Delivery | left | -1.491 | -177.595 |
| ShiftNull75_Delivery | right | -1.491 | -177.596 |

Four points per edge at x offsets ±0.20W and ±0.33W, 4 μm inside the patch and halfway through the substrate, exclude the central inset. Values are the complex means of the local longitudinal electric field. This diagnostic compares the two radiating edges inside each patch. Its phase is the raw Ez phase, before applying an equivalent-slot normal convention. It does not isolate feed-line radiation, finite-ground radiation or their interference in the far field.
