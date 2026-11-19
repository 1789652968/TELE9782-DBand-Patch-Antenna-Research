"""Final delivery audit on persisted data; emits only verified file and evidence counts."""
from pathlib import Path
import json,csv,hashlib,sys
from PIL import Image
root=Path(__file__).resolve().parents[1];v=root/'07_Final_Candidates';r=root/'08_Results_and_Figures';doc=root/'10_Documentation'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def table(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def main():
    chosen=read(v/'Final_Selection.json');verified=read(v/'Verification_Results.json')
    assert set(chosen)=={'Best_Balanced','Best_Broadside','Highest_Efficiency'}
    projects={}
    for path in set(chosen.values()):
        p=Path(path);project=p/(p.name+'.cst')
        assert project.is_file() and (project.with_suffix('')/'Result/Model.log').stat().st_size>0
        rec=read(p/'Reopen_Verification.json');assert rec['first']==0 and rec['last']==0
        ai=read(p/'Independent_Audit.json');assert ai['touchstone_max_gamma_difference']<1e-4
        chain=next(t for t in verified.values() if t['fresh']['path']==path)
        assert chain['accepted'] and chain['eta_range']<=1.2 and chain['beam_range']<=4
        for phase in ['production','dense','fresh']:
            s=chain[phase]
            assert s['solver']=='SUCCESS' and s['S11_50']<=-10 and s['D']>=6.5
        for name in ['Farfield_145_Sphere.txt','Farfield_150_Sphere.txt','Farfield_154_Sphere.txt','RealizedGain_Native_150_Sphere.txt','Farfield_150_1deg_Directivity.txt','Surface_Current_150.txt','Branch_Ez_150.txt','Efield_XY_150.txt','Geometry_Check.json','CST_50ohm.s1p']:
            assert (p/name).stat().st_size>0,(p,name)
        projects[p.name]=dict(cst=str(project),sha256=hashlib.sha256(project.read_bytes()).hexdigest(),cells=ai['cells'])
    assert len(table(r/'Multiobjective_Comparison.csv'))==6
    tol=table(r/'Manufacturing_Sensitivity.csv');assert len(tol)==15 and all(q['solver']=='SUCCESS' for q in tol)
    trials=table(r/'All_Optimisation_Trials.csv')
    assert sum(q.get('solver')=='SUCCESS' and bool(q.get('mode')) for q in trials)==len(list(root.glob('0[3-7]_*/**/round2.json')))
    angular=table(r/'Angular_Resolution_Check.csv');assert len(angular)==len(projects)
    for label in ['Final_Optimisation_Report','Reproduction_Guide','Beam_Squint_Diagnosis']:
        assert (doc/(label+'.md')).stat().st_size>700
    imgs=list(r.glob('*.png'));assert len(imgs)>=12
    for f in imgs:
        with Image.open(f) as img:img.verify()
    b=read(root/'02_Diagnostics/Backup_Verified.json');orig=next(Path(b['original']).glob('*.cst'));backup=next(Path(b['backup']).glob('*.cst'))
    assert hashlib.sha256(orig.read_bytes()).hexdigest()==hashlib.sha256(backup.read_bytes()).hexdigest()==b['sha256']
    reco=read(v/'Recommended_Project.json');assert hashlib.sha256(Path(reco['project']).read_bytes()).hexdigest()==reco['sha256']
    check=dict(selected_projects=projects,course_recommendation=reco['project'],verified_chart_files=len(imgs),trials=len(trials),sensitivity_rows=len(tol),source_and_backup_cst_sha256=b['sha256'])
    (r/'Delivery_File_Check.json').write_text(json.dumps(check,indent=2),encoding='utf-8');print(json.dumps(check,indent=2))
if __name__=='__main__':main()

