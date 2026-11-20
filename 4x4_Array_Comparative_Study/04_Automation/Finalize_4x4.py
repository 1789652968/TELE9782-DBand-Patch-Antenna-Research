"""Refresh reports, create a GitHub-ready evidence directory and hash the native handover ZIP."""
from pathlib import Path
import os, sys, shutil, time, subprocess, hashlib, csv, json, zipfile
from Extract_Results import ROOT, BASE, COMP, RESULTS, read, write_json, write, volts
from Write_Reports import main as reports
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def main():
    auto=ROOT/'04_Automation';log=auto/'Study_Complete.log'
    while 'COMPLETE STUDY' not in log.read_text(encoding='utf-8',errors='replace'):
        time.sleep(20)
    reports()
    final=ROOT/'01_CST_Project/Final_4x4'
    initial=ROOT/'01_CST_Project/Initial_4x4'
    report_dir=COMP/'Comparison_Figures'
    shutil.copy2(final/'Geometry.png',report_dir/'4x4_Geometry_CST.png')
    orig_probes,orig_stats=volts(initial)
    assert orig_stats['connected_patch_probes']==16 and orig_stats['minimum_Ez_Vm']>0
    write(RESULTS/'Verification/Initial_16_Patch_Probes.csv',orig_probes)
    write_json(RESULTS/'Verification/Initial_16_Patch_Probe_Check.json',orig_stats)
    primary=next(BASE.glob('*.cst'))
    baseline_sha=sha(primary);assert baseline_sha=='2030cb97b1ef2eb6c17ed60dcfb91eaf0d6838e38425c55beeb807cefc2f14fd'
    write_json(RESULTS/'Verification/Baseline_Project_SHA256.json',dict(path=str(primary),sha256=baseline_sha))
    repo=ROOT/'4x4_Array_Comparative_Study';repo.mkdir(exist_ok=True)
    for d in ('02_Simulation_Results','03_Comparison','05_Documentation'):
        shutil.copytree(ROOT/d,repo/d,dirs_exist_ok=True,ignore=shutil.ignore_patterns('Initial_Field_Readback'))
    ad=repo/'04_Automation';ad.mkdir(exist_ok=True)
    for name in ('Build_4x4.py','Run_4x4.py','Extract_Results.py','Verify_Native.py','Study_Sequence.py','Write_Reports.py'):
        shutil.copy2(auto/name,ad/name)
    shutil.copytree(auto/'CST_Utilities',ad/'CST_Utilities',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
    src=repo/'Native_Exports';src.mkdir(exist_ok=True)
    for p in final.iterdir():
        if p.is_file() and p.suffix.lower() in {'.csv','.json','.txt','.s1p','.png'}:shutil.copy2(p,src/p.name)
    path=ROOT/'Final_4x4_Native_CST.zip'
    manifest=ROOT/'Final_4x4_Native_CST.manifest.json'
    if not manifest.is_file():
        chosen=[final/'Final_4x4.cst']+[p for p in (final/'Final_4x4').rglob('*') if p.is_file() and p.suffix.lower() not in {'.lck','.lock','.tmp'}]
        partial=path.with_suffix('.zip.partial')
        with zipfile.ZipFile(partial,'w',zipfile.ZIP_DEFLATED,compresslevel=3,allowZip64=True) as z:
            for p in chosen:z.write(p,p.relative_to(ROOT).as_posix())
        with zipfile.ZipFile(partial) as z:
            for p in chosen:
                with z.open(p.relative_to(ROOT).as_posix()) as x:
                    assert hashlib.file_digest(x,'sha256').hexdigest()==sha(p),p
        os.replace(partial,path)
        write_json(manifest,dict(filename=path.name,bytes=path.stat().st_size,sha256=sha(path),source_files=len(chosen),local_only=True))
    manifest_record=read(manifest);assert sha(path)==manifest_record['sha256'];shutil.copy2(manifest,repo/manifest.name)
    local_remote='https://github.com/1789652968/TELE9782-DBand-Patch-Antenna-Research'
    handover=ROOT.parent/'10_GitHub_Handover/TELE9782-DBand-Patch-Antenna-Research'
    git_url=subprocess.run(['git','-C',str(handover),'remote','get-url','origin'],capture_output=True,text=True,check=False).stdout.strip()
    assert git_url==local_remote+'.git',git_url
    (repo/'README.md').write_text(f"""# TELE9782 4×4 Array Comparative Study

This evidence directory is staged locally for the existing TELE9782 research repository. It contains report documents, numerical comparisons, automation and native text exports. The native result archive remains in the parent study folder under {path.name}. Its SHA256 and byte count are listed in the accompanying manifest. Keep the .cst file with its same-named companion directory when extracting and opening it.

Start with the [comparison summary](03_Comparison/Comparison_Summary.md), the [English report](05_Documentation/Comparative_Study_Report.md) and the [reproduction guide](05_Documentation/Reproduction_Guide.md). The validated 1×2 baseline and its native archive are available in the [existing handover]({local_remote}). This 4×4 addition is a local staging directory and has no remote download link yet.
""",encoding='utf-8')
    result=read(RESULTS/'Verification/Final_Metrics.json')
    required=(final/'Final_4x4.cst',final/'Final_4x4/Result/Model.log',final/'Surface_Current_150.txt',final/'Farfield_150_Sphere.txt',final/'RealizedGain_Native_150_Sphere.txt',
        COMP/'Array_1x2_vs_4x4_Comparison.csv',ROOT/'05_Documentation/Comparative_Study_Report.md',
        COMP/'Comparison_Summary.md',RESULTS/'Verification/Native_Database_Readback.json')
    for p in required:assert p.stat().st_size>50,p
    from PIL import Image
    figures=list((COMP/'Comparison_Figures').glob('*.png'));assert len(figures)>=6
    for p in figures:
        with Image.open(p) as im:im.verify()
    write_json(RESULTS/'Verification/Delivery_Check.json',dict(verified_files=[str(p.relative_to(ROOT)) for p in required],
        figure_count=len(figures),radiation_efficiency_4x4=result['array4x4']['radiation_efficiency_pct'],archive=manifest_record))
    print('DELIVERY COMPLETE',len(figures),manifest_record,flush=True)
if __name__=='__main__':main()

