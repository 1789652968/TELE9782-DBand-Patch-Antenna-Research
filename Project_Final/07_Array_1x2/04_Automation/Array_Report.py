"""Assemble a report from the verified project, numerical audit and the two control models."""
from Array_Design_Notes import *
import shutil
def table(rows,keys,names=None):
    def fmt(v):return f'{v:.3f}' if isinstance(v,(float,np.floating)) else str(v)
    return '\n'.join(['| '+' | '.join(names or keys)+' |','|'+'|'.join('---' for k in keys)+'|']+['| '+' | '.join(fmt(v.get(k,'')) for k in keys)+' |' for v in rows])
def rows(path):
    with path.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def numtable(path,keys,names=None):
    def conv(x):
        try:return float(x)
        except (ValueError,TypeError):return x
    return table([{k:conv(v) for k,v in r.items()} for r in rows(path)],keys,names)
def main():
    theory,feed=write_theory()
    met=read(C/'Comparison_Metrics.json');s=met['original'];c=met['ground_control'];a=met['array'];p=read(P/'parameters.json');ver=read(R/'Verification.json')
    checks=read(P/'numerical_audit.json');pw=next(v for v in checks['farfield_checks'] if v['f_GHz']==150)
    with (ORIG/'Power_Consistency.csv').open(encoding='utf-8-sig') as f:spw=next(v for v in csv.DictReader(f) if float(v['f_GHz'])==150)
    history=rows(R/'Optimisation_History.csv');mesh=rows(R/'Mesh_Convergence.csv');m0,m1=mesh[-2:]
    dD=abs(float(m1['Dmax_dBi'])-float(m0['Dmax_dBi']));df=100*abs(float(m1['fmin_GHz'])-float(m0['fmin_GHz']))/float(m1['fmin_GHz']);dg=abs(float(m1['realized_gain_dBi'])-float(m0['realized_gain_dBi']));deff=abs(float(m1['rad_eff_pct'])-float(m0['rad_eff_pct']))
    br=field_rows(R);ab=max(abs(v['right_minus_left_dB']) for v in br);ph=max(abs(v['right_minus_left_deg']) for v in br)
    delta=lambda k:a[k]-s[k]
    base=read(W/'selection.json');case=base['name'];ff=frequency(P);sel=max([v for v in ff if v['S11_dB']<=-10],key=lambda v:v['realized_gain_dBi'])
    native=read(P/'summary.json');warnings=sorted(set(v['text'].strip() for v in native['messages'] if v['type']=='WARNING'))
    historytab=numtable(R/'Optimisation_History.csv',['name','array_spacing','patch_length','inset_length','transformer_width','transformer_length','cells','S11_dB','Dmax_dBi','realized_gain_dBi'],['Case','d mm','L mm','Inset mm','Wt mm','Lt mm','Cells','S11 dB','D dBi','Greal dBi'])
    meshtext=numtable(R/'Mesh_Convergence.csv',['name','cells','mesh_near','mesh_box','fmin_GHz','S11_dB','Dmax_dBi','realized_gain_dBi','rad_eff_pct'],['Mesh','Cells','Steps/wave','Steps/box','fmin GHz','S11 dB','D dBi','Greal dBi','ηrad %'])
    opttab=numtable(C/'Operating_Point_Comparison.csv',['design','criterion','f_GHz','S11_dB','Dmax_dBi','realized_gain_dBi'])
    ratio=10**(delta('realized_gain_dBi')/10)
    evaltext=f"""## Engineering conclusion at 150 GHz

The final array achieves **{a['Dmax_dBi']:.3f} dBi peak directivity** and **{a['realized_gain_dBi']:.3f} dBi peak realized gain**, compared with {s['Dmax_dBi']:.3f} and {s['realized_gain_dBi']:.3f} dBi for the original. Relative to the single patch these are {delta('Dmax_dBi'):+.3f} dB and {delta('realized_gain_dBi'):+.3f} dB. Peak radiation intensity at the same available input power changes by a factor of {ratio:.3f}. The original already met the 6.5 dBi assignment. The measured change in H-plane beamwidth is {delta('H_HPBW_deg'):+.2f}° and in E-plane width {delta('E_HPBW_deg'):+.2f}°.

Radiation efficiency changes by {delta('rad_eff_pct'):+.2f} percentage points and total efficiency by {delta('total_eff_pct'):+.2f} points. The small nominal radiation-efficiency advantage over the original is smaller than the observed mesh variation and does not establish a robust efficiency improvement. Native S11 changes by {delta('S11_dB'):+.2f} dB. The −10 dB bandwidth changes by {delta('BW_GHz'):+.3f} GHz. The two-patch board occupies {a['main_ground_mm2']:.2f} mm² of main ground compared with {s['main_ground_mm2']:.2f} mm² originally. An implementation aimed at peak link gain and H-plane spatial selectivity benefits from the array. The original has a smaller footprint and a simpler, straight feed. Neither result has been validated on fabricated hardware."""
    implementation=f"""# CST implementation

The parameterized construction joins two slotted gold patches, two outlet lines, two bends and both horizontal transformers to one signal solid named `antenna:trunk`. The signal conductor sits at z={p['substrate_h']:.3f}–{p['substrate_h']+p['metal_thickness']:.3f} mm. The common ground at z=−{p['metal_thickness']:.3f}–0 mm is electrically separate. Polyimide fills the intervening {p['substrate_h']:.3f} mm. The ground and polyimide each include the 0.50 × 0.50 mm launch. Main ground is {p['ground_width']:.2f} × {p['ground_length']:.2f} mm. Gold uses σ=4.561×10⁷ S/m and Polyimide εr={p['eps_r']:g}, tanδ={p['loss_tangent']:g} referenced at 150 GHz. The inset depth is {p['inset_length']:.3f} mm and each side clearance 0.020 mm. Dimensions and solid names are available in `parameters.json` and `Tree.json`.

One physical, single-mode microstrip waveguide port is located at y=−{p['ground_length']/2+p['launch_length']:.3f} mm and faces inward along +y. Its aperture spans x=±0.25 mm, z=−0.002 to 0.240 mm. Solver settings are TD-S, hexahedral mesh with PBA, 130–170 GHz, energy decay target −60 dB, open radiation boundaries, quarter-wavelength open-space reference at 130 GHz, and the global enclosing farfield surface. The delivered native S1,1 trace has a solved reference of {a['reference_ohm']:.4f} Ω. The original single's native reference is {s['reference_ohm']:.4f} Ω and the final physical trunk's modal impedance appears in Port_Mode_Check.json. `AutoNormImpedance=False` in the original and screening histories. The production history explicitly requests AutoNormImpedance=True and NormingImpedance=50. Reading the saved project nevertheless shows an unchanged modal-reference S1,1. The independently verified CST Touchstone export is the authoritative fixed-50-Ω trace. The common 50 Ω comparison uses Zin=Zref(1+Γ)/(1−Γ) and Γ50=(Zin−50)/(Zin+50). Common-reference realized gain uses D×ηrad×(1−|Γ50|²).

Field monitors store E/H/current at 150 GHz and 13 farfields at 130, 140, 146–154, 160 and 170 GHz. The 2° full-sphere exports sample total directivity. At θ=0°, φ=0°, Eφ and Eθ are {a['broadside_Ephi_dBi']:.2f} and {a['broadside_Etheta_dBi']:.2f} dBi. Eφ points along y here. E-plane comparisons use YZ and H-plane comparisons use XZ. Signed positive angles point toward +y and +x respectively. Native model views and field exports are in `02_Simulation_Results`.

The original 04_Automation directory was absent in this local final package. The construction and result readers derive from the previously published project automation copy. An enlarged-ground control rebuilds the single original patch with its 0.513 mm length, 0.190 mm inset and straight feeder. Extending the board length also increases its straight feed by 0.050 mm. Differences between control and array include the feed, element retuning and mutual fields."""
    put('CST_Implementation.md',implementation)
    verification=f"""# Numerical validation

The delivered model was saved with native results, closed, opened from its final pathname, freshly solved, closed and opened again. Parameters were compared with the selected build. One port and {len(ver['monitors'])} farfield monitors were found. CST returned **{ver['solver']['state']}**. The full S11 trace has {ver['sample_count']} samples. Maximum complex differences were {ver['before_rerun_complex_delta']:.3g} on initial reopen, {ver['rerun_complex_delta']:.3g} after fresh solve, {ver['after_reopen_complex_delta']:.3g} on second reopen, and {ver['exported_csv_complex_delta']:.3g} between the exported CSV and reopened trace. Peak directivity across all 13 monitors changed by at most {ver['farfields_rerun_max_deltas_dB']['Dmax_dBi']:.5g} dB on rerun. At 150 GHz the fresh solve moves peak directivity by +0.00194 dB, realized gain by −0.04791 dB and the S11 minimum by one 0.04 GHz sample. The solver log records that the repeat reused the prior port-adaptation result. The differences exceed the initial very tight software repeatability check. Their exact numerical cause has not been isolated. Opening the completed project reads back the saved trace exactly. All final figures use the fresh solve.

## Same-geometry mesh sensitivity

{meshtext}

Between the two densest grids, the absolute changes were {dD:.4f} dB in directivity at 150 GHz, {dg:.4f} dB in realized gain, {deff:.3f} points in radiation efficiency, and {df:.3f}% in minimum-S11 frequency. The indicative limits of 0.2 dB for directivity and 1% in resonance are {'both met' if dD<.2 and df<1 else 'not both met'}. The matched-band edges and depth of a narrow S11 minimum remain mesh-sensitive. Finite mesh precision is separate from fabrication uncertainty.

## Power, passivity and angular normalization

CST incident, reflected, accepted and radiated powers at 150 GHz are {pw['Pstim_W']:.6f}, {pw['Poutgoing_W']:.6f}, {pw['Paccepted_W']:.6f} and {pw['Prad_W']:.6f} W. Gold and dielectric dissipation are {pw['Pmetal_W']:.6f} and {pw['Pdielectric_W']:.6f} W. Accepted minus radiated and dissipated power is {pw['power_balance_residual_W']:+.6f} W, or {pw['power_balance_residual_percent_accepted']:+.3f}% of accepted power. The largest |S11| in the native broadband sweep is {checks['max_abs_S11']:.6f}. The realized-gain identity residual at 150 GHz is {pw['gain_identity_residual_dB']:+.6f} dB.

The 2° full-sphere export was converted from dBi to linear directivity, weighted by sinθ, closed periodically in φ, and integrated by the trapezoidal rule. Its mean over 4π is {a['sphere_mean']:.6f}, discrepancy {100*abs(a['sphere_mean']-1):.3f}%. The calculation uses the unscaled angular samples. `Power_Balance.csv` gives per-monitor values. CST loss curves in the raw export may have coarser frequency sampling than S11. Interpolated power checks away from native loss samples have lower evidential weight than the 150 GHz check.

Final CST warning messages: {', '.join(warnings)}. The commercial-use notice describes licensing. Solver completion, power residual and sphere integration are checked independently."""
    put('Simulation_Validation.md',verification)
    compkeys=['Dmax_dBi','D_broadside_dBi','realized_gain_dBi','S11_dB','S11_50_dB','realized_50_dBi','rad_eff_pct','total_eff_pct','fmin_GHz','f_low_GHz','f_high_GHz','BW_GHz','FBW_percent','E_HPBW_deg','H_HPBW_deg','theta_deg','phi_deg']
    comp=table([dict(metric=k,single=s[k],control=c[k],array=a[k],delta=delta(k)) for k in compkeys],['metric','single','control','array','delta'],['Metric','Original','Enlarged single','Final array','Array − original'])
    coupling=numtable(C/'Spacing_Field_and_Pattern_Study.csv',['case','spacing_mm','Zre150_ohm','Zim150_ohm','fmin_GHz','H_HPBW_deg','left_patch_Krms_A_per_m','right_patch_Krms_A_per_m'])
    analysis=f"""# Single versus array

{evaltext}

## Fixed-frequency comparison

{comp}

Footprint including the launch is {s['with_launch_area_mm2']:.2f} mm² (original) and {a['with_launch_area_mm2']:.2f} mm² (array). The main beam lies {a['theta_deg']:.0f}° from +z at φ={a['phi_deg']:.0f}° on the sampled array sphere. Broadside realized gain is {a['realized_broadside_dBi']:.3f} dBi. Among several near-equal angular samples, peak azimuth is precision-sensitive near the pole. The E-plane −3 dB crossings are {a['E_low_deg']:.2f}° and {a['E_high_deg']:.2f}°. H-plane crossings are {a['H_low_deg']:.2f}° and {a['H_high_deg']:.2f}°, interpolated between adjacent 2° samples relative to each cut's own peak. Angular CSVs retain all rear lobes and nulls. The plots clip the ordinate below their displayed floor.

Changing only the single-patch board size and feed extension changed peak directivity by {c['Dmax_dBi']-s['Dmax_dBi']:+.3f} dB and realized gain by {c['realized_gain_dBi']-s['realized_gain_dBi']:+.3f} dB. Adding the complete two-patch design on that board changed them by a further {a['Dmax_dBi']-c['Dmax_dBi']:+.3f} and {a['realized_gain_dBi']-c['realized_gain_dBi']:+.3f} dB. This control identifies the board contribution with the single radiator. Interactions make a unique element-only decomposition impossible.

The original and array dissipate respectively {float(spw['Pmetal_W']):.5f} and {pw['Pmetal_W']:.5f} W in metal, and {float(spw['Pdielectric_W']):.5f} and {pw['Pdielectric_W']:.5f} W in dielectric, at the common 0.5 W stimulated normalization. The solver records whole-antenna dissipation. It does not isolate T-junction loss. The feed and coupling change input impedance and stored fields. Distinct dissipation and mismatch contributions can therefore move in different directions.

## Handpicked operating point versus extrema

{opttab}

The selection criterion above uses realized gain at genuinely simulated monitors satisfying S11 ≤ −10 dB. The lowest broadband S11 occurs at {s['fmin_GHz']:.2f} GHz (single) and {a['fmin_GHz']:.2f} GHz (array). The two selections and the minima answer different questions. Lines on frequency plots connect discrete farfield monitor solutions.

## Spacing, coupling and excitation

{coupling}

The coarse spacing comparison retains common ground, inset, transformer and vertical feed dimensions. Increasing spacing lengthens each horizontal 50 Ω continuation by half the change in spacing. The measured change in Zin, resonance, current and radiation therefore includes mutual fields and routing changes. A one-port antenna has no independent external element-to-element S21. The exported local Ez values originate at four matched reference-plane pairs 0.020 mm above the ground. The maximum absolute final right/left amplitude difference is **{ab:.4f} dB**, and phase difference **{ph:.3f}°**. These are loaded local field ratios. They support balanced excitation without assigning independently calibrated forward powers to the branches. The current table averages |K|² over equal central patch rectangles, using the native facet areas at the top metal surface.

Among the final forward cut samples, the strongest additional local maximum relative to the H-cut peak is {a['H_other_forward_peak_relative_dB'] if a['H_other_forward_peak_relative_dB'] is not None else 'absent'} (dB if present). The E-cut value is {a['E_other_forward_peak_relative_dB'] if a['E_other_forward_peak_relative_dB'] is not None else 'absent'}. These checks apply to the sampled principal cuts. The global maximum and full 3D sphere also establish the main-beam direction."""
    put('Single_vs_Array_Analysis.md',analysis)
    pics='\n\n'.join('!['+label+'](../03_Comparison/'+name+'_Comparison.png)' for label,name in [('Return loss at a common 50 Ω','S11'),('Directivity','Directivity'),('Realized gain','Realized_Gain'),('Radiation and total efficiency','Efficiency'),('E-plane','E_Plane'),('H-plane','H_Plane'),('Matched bandwidth','Bandwidth')])
    report=f"""# TELE9782 · A corporate-fed D-band patch pair at 150 GHz

## Abstract

{evaltext.split('## Engineering conclusion at 150 GHz')[1].strip()}

## Assignment and baseline

The assignment calls for a D-band microstrip antenna with directivity above 6.5 dBi. We compare a validated original single patch, a single on the larger array ground, and a single-port two-patch design at 150 GHz. The original native file and its verification record were preserved. All antenna performance values in this study are full-wave simulations.

{theory}

{feed}

{implementation}

![Final CST geometry](../02_Simulation_Results/Geometry_Top.png)

## Parameter optimization

{historytab}

Candidate selection first required S11 ≤ −10 dB at 150 GHz, then ranked peak realized gain. This selected screening case {case}. Subsequent angular, power and mesh checks test whether this scalar choice is defensible. The solver models complete routes with square bends, nominally quarter-wave transformer arms and the real dielectric and metal losses.

{analysis}

## Comparison figures

{pics}

![Top-surface current at 150 GHz](../02_Simulation_Results/Surface_Current_Map.png)

![Native CST farfield at 150 GHz](../02_Simulation_Results/Farfield_150_CST.png)

{verification}

## Limitations

Gold conductivity and constant substrate permittivity and loss tangent are engineering inputs. Surface roughness, process tolerances, packaging, connector transitions and measured D-band material dispersion were not characterized. An individual arm has a nominal quarter-wave design. Its embedded impedance is influenced by loading. The common-reference calculation does not move the port plane. The matched interval covers part of 130–170 GHz. Sparse farfield monitors support conclusions at their sampled frequencies. Nominal geometric symmetry alone is insufficient to establish balance, hence the complex field comparison.

## Conclusion

For the 150 GHz enhancement study, the narrower H-plane beam and simulated peak realized-gain increase of {delta('realized_gain_dBi'):.2f} dB quantify the return on a larger, more complex board. For a submission whose sole requirement is directivity above 6.5 dBi, the original single element remains sufficient."""
    put('Final_Report_Results.md',report)
    checklist=f"""# Acceptance record

| Check | Evidence |
|---|---|
| One physical input, two connected patches, shared board and finite gold | Geometry_Top.png, Port.png, Tree.json, native CST history |
| Physical transformers, equal arms and modal checks | Feed_Network_Calculations.md, Port_Mode_Check.json |
| Both elements excited | Branch_Balance.csv, Surface_Current_150.txt, Surface_Current_Map.png |
| Solver, reopened parameters, fresh run and re-read trace | Verification.json, state {ver['solver']['state']} |
| D > 6.5 dBi and S11 ≤ −10 dB at 150 GHz | D {a['Dmax_dBi']:.3f} dBi, S11 {a['S11_dB']:.3f} dB |
| Gain and radiation/total efficiencies | Final_Array_Performance.csv, 13 farfield monitors |
| E/H cuts and beamwidth | E_Plane.csv, H_Plane.csv, comparison figures |
| Same-geometry mesh comparison | Mesh_Convergence.csv, ΔD {dD:.4f} dB and Δf {df:.3f}% |
| Power and farfield normalization | Power_Balance.csv, residual {pw['power_balance_residual_percent_accepted']:+.3f}%, sphere mean {a['sphere_mean']:.6f} |
| Original, ground control, final, both operating-point definitions | Single_vs_Array_150GHz.csv, Operating_Point_Comparison.csv |
| Full native model, companion, comparison plots and report | 01_CST_Project, 03_Comparison, Final_Report_Results.md |

Aspirational at 150 GHz: D≥9 dBi {'met' if a['Dmax_dBi']>=9 else 'missed'}, Greal≥6.8 dBi {'met' if a['realized_gain_dBi']>=6.8 else 'missed'}, S11≤−15 dB {'met' if a['S11_dB']<=-15 else 'missed'}, ηrad≥71.55% {'met' if a['rad_eff_pct']>=71.55 else 'missed'}. Physical measurements remain outside this simulation study."""
    put('Final_Acceptance_Checklist.md',checklist)
if __name__=='__main__':main()


