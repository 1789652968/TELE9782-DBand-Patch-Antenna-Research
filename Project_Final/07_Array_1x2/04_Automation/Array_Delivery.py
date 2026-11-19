"""Check the finished deliverable and produce a portable manifest and run instructions."""
from Array_Results_Extraction import *
import hashlib,re
def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def main():
    ver=read(R/'Verification.json');source=ver['source'];mesh=read(W/'final_source.json')['mesh_source'];sweep=read(W/'selection.json')['name']
    results='S11.csv Directivity.csv Realized_Gain.csv Radiation_Efficiency.csv Total_Efficiency.csv E_Plane.csv H_Plane.csv Mesh_Convergence.csv Power_Balance.csv Optimisation_History.csv Final_Array_Performance.csv Branch_Balance.csv Farfield_150_Sphere.txt Surface_Current_Map.png CST_50ohm.s1p Final_50ohm.s1p Independent_Power_Check.json Geometry_Top.png Port.png Farfield_150_CST.png Verification.json Port_Mode_Check.json Saved_Model_Configuration_Check.json Power_Closure_By_Mesh.csv'.split()
    comparisons='Single_vs_Array_150GHz.csv Single_vs_Array_Frequency.csv Directivity_Comparison.png Realized_Gain_Comparison.png S11_Comparison.png Efficiency_Comparison.png E_Plane_Comparison.png H_Plane_Comparison.png Bandwidth_Comparison.png Operating_Point_Comparison.csv Spacing_Field_and_Pattern_Study.csv Spacing_Current_Comparison.png Common50_150GHz.csv Three_Model_Power_150GHz.csv'.split()
    docs='Array_Design_Theory.md Feed_Network_Calculations.md CST_Implementation.md Simulation_Validation.md Single_vs_Array_Analysis.md Final_Report_Results.md Final_Acceptance_Checklist.md'.split()
    model=P/'TELE9782_DBand_1x2_Array_Final.cst'
    assert model.is_file() and (model.with_suffix('')/'Result'/'Model.log').is_file()
    for folder,items in [(R,results),(C,comparisons),(DOC,docs)]:
        assert all((folder/file).stat().st_size>0 for file in items)
    for m in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',(DOC/'Final_Report_Results.md').read_text(encoding='utf-8')):
        assert (DOC/m).is_file(),m
    orig=ROOT.parent/'01_CST_Project'/'TELE9782_DBand_Patch_Final.cst'
    fixed=metrics(P,R);native=metrics(W/mesh);comparison=dict(modal_source=mesh,native_modal_reference_ohm=native['reference_ohm'],pre_rerun_expected_fixed50_from_modal_S11_dB=native['S11_50_dB'],native_delivered_reference_ohm=fixed['reference_ohm'],native_delivered_S11_dB=fixed['S11_dB'],native_gain_dBi=fixed['realized_gain_dBi'],pre_rerun_expected_realized_common50_dBi=native['realized_50_dBi'],delivered_realized_common50_dBi=fixed['realized_50_dBi'])
    f,_,_,_,calc=scattering(W/mesh);x,g,z,_,_=scattering(P);assert np.allclose(f,x)
    comparison['native_vs_math50_max_complex_difference']=float(max(abs(scattering(P)[4]-g)))
    comparison['native_modal_vs_production_max_complex_difference']=float(max(abs(scattering(W/mesh)[1]-g)))
    touch=next(R.glob('CST_50ohm*.s1p'))
    data=np.loadtxt([line for line in touch.read_text(errors='replace').splitlines() if line.strip() and line.lstrip()[0] not in '!#'])
    factor=data[-1,0]/f[-1];assert np.allclose(data[:,0]/factor,f,atol=.0001)
    exported=data[:,1]+1j*data[:,2];comparison['broadband_max_complex_difference']=float(max(abs(scattering(P)[4]-exported)))
    comparison['CST_touchstone_header']=next(line for line in touch.read_text().splitlines() if line.strip().startswith('#'))
    comparison['CST_touchstone_s11_150_dB']=20*np.log10(abs(exported[np.argmin(abs(f-150))]))
    comparison['explanation']='Native S1,1 retained the solved modal reference. The CST Touchstone exporter explicitly renormalized the saved result to 50 ohms.'
    (R/'Reference_Comparison.json').write_text(json.dumps(comparison,indent=2))
    assert '50' in comparison['CST_touchstone_header'] and comparison['broadband_max_complex_difference']<.0001,comparison
    if '### Common 50 Ω reference, 150 GHz' not in (DOC/'Final_Report_Results.md').read_text(encoding='utf-8'):
        from Array_Report_Appendix import finalize
        finalize()
    tree=read(R/'Tree.json')
    assert all(item in tree for item in [r'Components\antenna\trunk',r'Components\antenna\ground',r'Components\antenna\substrate',r'Materials\Gold',r'Materials\Polyimide (lossy)'])
    checks=[]
    for folder,names in [(P,[model.name]),(R,results),(C,comparisons),(DOC,docs)]:
        for name in names:
            path=folder/name;checks.append(dict(path=str(path.relative_to(ROOT)),bytes=path.stat().st_size,sha256=digest(path)))
    write(R/'Delivery_Manifest.csv',checks)
    (R/'Baseline_Provenance.json').write_text(json.dumps({str(f.relative_to(ROOT.parent)):digest(f) for f in [orig,ORIG/'Validation_Summary.csv',ORIG/'Verification.json',ORIG/'Farfield_150_Sphere.txt']},indent=2))
    readme=f"""# TELE9782 · 150 GHz corporate-fed 1×2 array

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
- [06_Working](06_Working) · solver projects, intermediate numerical exports and run logs. The selected initial screening geometry was {sweep}, final validated mesh source {mesh}, and exact-reference production source {source}.

The comparison reads the original validated single from the sibling directory ../02_Simulation_Results. Keep the array directory under Project_Final when regenerating the plots."""
    (ROOT/'README.md').write_text(readme,encoding='utf-8')
    auto=f"""# Automation and reproduction

Commands below use the current directory 04_Automation. Execute the CST steps serially on a licensed workstation. A scratch copy of the array folder preserves the delivered files. To rebuild the study from scratch, use a fresh study directory with the same 01–06 directory names and these automation files, adjacent to the original validated results. Completed screening cases are reused if their angular exports are present.

In PowerShell define the two interpreters.

~~~powershell
$cst = 'D:\\TELE9782\\CST Studio Suite 2024\\Opera\\code\\bin\\python.exe'
$analysisDir = 'C:\\Users\\Admin\\AppData\\Local\\spyder-6\\envs\\spyder-runtime'
$analysis = Join-Path $analysisDir 'python.exe'
$env:PATH = "$analysisDir;$analysisDir\\Library\\bin;$env:PATH"
~~~

Rebuild and extract the electromagnetic results.

~~~powershell
& $cst Array_Optimisation.py
& $cst Array_Sweep_Fields.py
~~~

For the complete second-stage resonance comparison, run & $analysis Array_Final_Selection.py after the first two commands. It runs the retuned 1.20 mm coarse case, checks whether a fine candidate is warranted, tests mesh stability, performs native fixed-reference production, and calls the rerun and mode scripts. If it has completed, proceed directly to the numerical postprocessing steps below. The independent holdout is obtained with & $cst Array_Refine.py Refined MeshHoldout mesh_near=38 mesh_box=57 after native verification. Array_Holdout.py also performs this check and then regenerates all outputs. The first script performs the feed sweep, controlled spacing comparison, Fine run and ground control. Where a third grid was required use the geometry and mesh settings recorded in Mesh_Convergence.csv with Array_Refine.py. To repeat an individual geometry, supply source name, new case name and key=value parameters.

~~~powershell
& $cst Array_Fixed_Reference.py {mesh}
& $cst Array_Rerun.py Final50
& $cst Array_Line_Mode.py
& $cst Array_Touchstone.py
& $analysis Array_Results_Extraction.py
& $analysis Array_Comparison.py
& $analysis Array_Coupling.py
& $analysis Array_Current_Maps.py
& $analysis Array_Common_Reference.py
& $analysis Array_Report.py
& $analysis Array_Config_Check.py
& $analysis Array_Power_Closure.py
& $analysis Array_Delivery.py
~~~

The hosted scripts use the CST 2024 Python interface installed with the software. Numerical post-processing uses NumPy 2 and Matplotlib. Array_Build.py and Single_Control.py share Reference_ModelHistory.json. Array_Fields.py exports native complex fields at explicit point coordinates. The postprocessor reads exported values and native CST farfields, with no ideal array synthesis. To inspect the original modal setup use the {mesh} working project. Open the final project for the production model. Use the CST Touchstone export for the exact 50 Ω curve."""
    (ROOT/'04_Automation'/'README.md').write_text(auto,encoding='utf-8')
    (DOC/'Execution_Log.md').write_text(f"""# Execution log

1. Original single geometry, fine-mesh numerical baseline and saved verification read. Provenance hashes recorded.
2. Initial connected array solved. Feed development and five nominal spacings tested on a fixed board. Candidate values, warnings and intermediate native file locations are recorded in Optimisation_History.csv.
3. Screening selection was {sweep}. More than one grid on the same geometry was solved. Accepted mesh source: {mesh}. GroundControl is a separate enlarged-board single.
4. Final50 was solved with the explicit 50 Ω history setting. The saved modal trace was independently renormalized by CST Touchstone export. The delivered file was reopened and freshly solved. Complex S11 and all farfield monitor metrics were compared.
5. Native EM field, current, power and angular exports were reduced to tables and plots. Source and file-existence checks completed. The report lists numerical uncertainty and the limits of a simulation-only design.
""",encoding='utf-8')
if __name__=='__main__':main()






