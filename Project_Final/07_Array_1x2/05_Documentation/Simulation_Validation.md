# Numerical validation

The delivered model was saved with native results, closed, opened from its final pathname, freshly solved, closed and opened again. Parameters were compared with the selected build. One port and 13 farfield monitors were found. CST returned **SUCCESS**. The full S11 trace has 1001 samples. Maximum complex differences were 0 on initial reopen, 0.00702 after fresh solve, 0 on second reopen, and 0 between the exported CSV and reopened trace. Peak directivity across all 13 monitors changed by at most 0.0079415 dB on rerun. At 150 GHz the fresh solve moves peak directivity by +0.00194 dB, realized gain by −0.04791 dB and the S11 minimum by one 0.04 GHz sample. The solver log records that the repeat reused the prior port-adaptation result. The differences exceed the initial very tight software repeatability check. Their exact numerical cause has not been isolated. Opening the completed project reads back the saved trace exactly. All final figures use the fresh solve.

## Same-geometry mesh sensitivity

| Mesh | Cells | Steps/wave | Steps/box | fmin GHz | S11 dB | D dBi | Greal dBi | ηrad % |
|---|---|---|---|---|---|---|---|---|
| Spacing120_Retuned | 103740.000 | 20.000 | 30.000 | 150.920 | -16.255 | 9.050 | 7.650 | 74.208 |
| RetunedFine | 218776.000 | 30.000 | 45.000 | 151.320 | -13.045 | 9.074 | 7.598 | 74.903 |
| Refined | 474240.000 | 36.000 | 54.000 | 149.760 | -27.153 | 8.841 | 7.456 | 72.829 |
| MeshHoldout | 523614.000 | 38.000 | 57.000 | 149.840 | -29.359 | 8.850 | 7.470 | 72.863 |

Between the two densest grids, the absolute changes were 0.0088 dB in directivity at 150 GHz, 0.0142 dB in realized gain, 0.034 points in radiation efficiency, and 0.053% in minimum-S11 frequency. The indicative limits of 0.2 dB for directivity and 1% in resonance are both met. The matched-band edges and depth of a narrow S11 minimum remain mesh-sensitive. Finite mesh precision is separate from fabrication uncertainty.

## Power, passivity and angular normalization

CST incident, reflected, accepted and radiated powers at 150 GHz are 0.500000, 0.000844, 0.499156 and 0.359298 W. Gold and dielectric dissipation are 0.085280 and 0.041134 W. Accepted minus radiated and dissipated power is +0.013444 W, or +2.693% of accepted power. The largest |S11| in the native broadband sweep is 0.907589. The realized-gain identity residual at 150 GHz is +0.000000 dB.

The 2° full-sphere export was converted from dBi to linear directivity, weighted by sinθ, closed periodically in φ, and integrated by the trapezoidal rule. Its mean over 4π is 0.987345, discrepancy 1.265%. The calculation uses the unscaled angular samples. `Power_Balance.csv` gives per-monitor values. CST loss curves in the raw export may have coarser frequency sampling than S11. Interpolated power checks away from native loss samples have lower evidential weight than the 150 GHz check.

Final CST warning messages: 1 warning occurred., This software is licensed for non-commercial use only.. The commercial-use notice describes licensing. Solver completion, power residual and sphere integration are checked independently.

## Port absorption and the complete power budget

At 150 GHz, counting radiation and dissipated power in gold and polyimide leaves 0.013444 W (2.693% of accepted power). The separate CST curve *Power Absorbed at all Ports* contributes 0.011725 W (2.349% of accepted power). The installed CST 2024 Help, *Power View → Power Absorbed at all Ports*, identifies this term as absorption by the waveguide-port boundary of field components outside the specified modal basis. It is distinct from outgoing fundamental-mode power and from material dissipation. The native curve is included as an independent export. The complete residual Paccepted − Prad − Pmetal − Pdielectric − Pport,abs is **+0.001720 W, or +0.345%**. No efficiency or farfield has been rescaled.

The single excited quasi-TEM mode remains the definition of the electrical input. The absorbed fraction quantifies another limitation of the finite launch and modeled port. The geometry, selected mode and unused-mode treatment were held consistent across the physical comparison. The reported radiation and total efficiencies retain this absorbed power in their denominators. See Power_Closure_By_Mesh.csv for both budgets on the selected meshes and ground controls.
