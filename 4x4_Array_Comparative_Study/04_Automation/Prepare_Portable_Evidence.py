from pathlib import Path
p=Path(__file__).resolve().parent
for n in ('Build_4x4.py','Extract_Results.py'):
 f=p/n;s=f.read_text(encoding='utf-8-sig')
 if n=='Extract_Results.py':s=s.replace('import argparse, csv, json, math, re','import argparse, csv, json, math, re, os')
 needle="BASE=ROOT.parent/'08_Efficiency_Optimisation/06_Final_Candidate/TELE9782_DBand_Efficiency_Final'"
 add="""path_from_project='08_Efficiency_Optimisation/06_Final_Candidate/TELE9782_DBand_Efficiency_Final'
BASE=Path(os.environ['TELE9782_BASELINE_DIR']) if 'TELE9782_BASELINE_DIR' in os.environ else ROOT.parent/path_from_project
if not (BASE/'parameters.json').exists():BASE=ROOT.parent/'Project_Final'/path_from_project"""
 s=s.replace(needle,add);f.write_text(s,encoding='utf-8')
f=p/'Inspect_Initial_Patches.py';s=f.read_text(encoding='utf-8').replace('02_Simulation_Results/Verification/Initial_Field_Readback','06_Local_Readback/Initial_Field_Readback').replace('evidence.mkdir(parents=True,exist_ok=True)','evidence.mkdir(parents=True,exist_ok=True)');f.write_text(s,encoding='utf-8')
f=p/'Finalize_4x4.py';s=f.read_text(encoding='utf-8')
s=s.replace("from Extract_Results import ROOT, COMP, RESULTS, read, write_json", "from Extract_Results import ROOT, BASE, COMP, RESULTS, read, write_json, write, volts")
a="""    initial=ROOT/'01_CST_Project/Initial_4x4'
    report_dir=COMP/'Comparison_Figures'
    shutil.copy2(final/'Geometry.png',report_dir/'4x4_Geometry_CST.png')
    orig_probes,orig_stats=volts(initial)
    assert orig_stats['connected_patch_probes']==16 and orig_stats['minimum_Ez_Vm']>0
    write(RESULTS/'Verification/Initial_16_Patch_Probes.csv',orig_probes)
    write_json(RESULTS/'Verification/Initial_16_Patch_Probe_Check.json',orig_stats)
    primary=next(BASE.glob('*.cst'))
    baseline_sha=sha(primary);assert baseline_sha=='2030cb97b1ef2eb6c17ed60dcfb91eaf0d6838e38425c55beeb807cefc2f14fd'
    write_json(RESULTS/'Verification/Baseline_Project_SHA256.json',dict(path=str(primary),sha256=baseline_sha))
"""
s=s.replace("    repo=ROOT/'4x4_Array_Comparative_Study';repo.mkdir(exist_ok=True)",a+"    repo=ROOT/'4x4_Array_Comparative_Study';repo.mkdir(exist_ok=True)")
s=s.replace("shutil.copytree(ROOT/d,repo/d,dirs_exist_ok=True)","shutil.copytree(ROOT/d,repo/d,dirs_exist_ok=True,ignore=shutil.ignore_patterns('Initial_Field_Readback'))")
f.write_text(s,encoding='utf-8')

