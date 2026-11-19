"""Serial CST worker with a fresh application connection per job and post-export recovery."""
from Round2_Search import *
import Round2_Search as search
import subprocess,shutil
cp=Path(__file__).resolve()
def single():
    task=json.loads(sys.argv[2]);st=Path(task['stage']);source=Path(task['source']) if task['source'] else None
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        run(de,st,task['name'],task['change'],task['mode'],source)
        if task['name']=='ShiftBracket95':
            from Round2_Local_Bracket import local
            local(de)
    finally:de.close()
def isolated(unused,stage,name,change,mode='screen',source=None):
    folder=stage/name;out=folder/'round2.json'
    if out.exists():
        assert read_params(folder)==GEOM|dict(mesh_near=20,mesh_box=30)|change
        return json.loads(out.read_text())
    task=dict(stage=str(stage),name=name,change=change,mode=mode,source=str(source) if source else None)
    for attempt in range(3):
        print('JOB',name,mode,'attempt',attempt+1,flush=True)
        rc=subprocess.run([sys.executable,'-u',str(cp),'single',json.dumps(task)]).returncode
        if out.exists():return json.loads(out.read_text())
        if rc==0:raise RuntimeError('Child returned without result '+name)
    raise RuntimeError('CST did not complete '+name)
def main():
    search.run=isolated
    before=V/'Screen_Selection_Initial.json'
    if not before.exists():shutil.copy2(V/'Screen_Selection.json',before)
    prior=(V/'H085/H085_Production');cfg=read_params(prior)
    h085=isolated(None,prior.parent,'H085_Delivery',cfg,'fresh',prior)
    rows=completed();by={q['name']:q for q in rows}
    control=by['Control20'];positive=by['FeedShiftPlus']
    assert control['phi']==90 and positive['phi']==270
    mid=round(.24*control['theta']/(control['theta']+positive['theta']),3)
    jobs=[(Y,'ShiftBracket75',dict(shift_y=mid)),(Y,'ShiftBracket85',thick(.085)|dict(shift_y=mid+.015)),
          (Y,'ShiftBracketWideGround',thick(.085)|dict(shift_y=mid-.015,ground_width=2.85,rear_delta=-.045)),
          (H,'H095DeepInset',thick(.095)|dict(inset_length=.194)),(H,'H110DeepInset',thick(.110)|dict(inset_length=.202,transformer_length=.26)),
          (Y,'ShiftBracket95',thick(.095)|dict(shift_y=mid+.005,inset_length=.191,ground_width=2.85))]
    for st,n,c in jobs:isolated(None,st,n,c)
    final_jobs(None)
    tested=json.loads((V/'Verification_Results.json').read_text())
    if 'H085' not in tested:
        prod=json.loads((prior/'round2.json').read_text());den=json.loads((prior.parent/'H085_Dense/round2.json').read_text())
        three=[prod,den,h085]
        tested['H085']=dict(trial='H085',screen=by['H085'],production=prod,dense=den,fresh=h085,accepted=all(good(q) for q in three),eta_range=max(q['eta'] for q in three)-min(q['eta'] for q in three),beam_range=max(q['theta'] for q in three)-min(q['theta'] for q in three))
        dump(V/'Verification_Results.json',tested)
    viable=[t['fresh'] for t in tested.values() if t['accepted'] and t['eta_range']<=1.2 and t['beam_range']<=4]
    if not viable:raise RuntimeError('No stable shortlisted candidate')
    sel=roles(viable);dump(V/'Final_Selection.json',{k:v['path'] for k,v in sel.items()});win=sel['Best_Balanced']
    dump(R/'Targeted_Complete.json',{'jobs':[n for _,n,_ in jobs],'shift_proposal_mm':mid,'chosen':win['path']})
    tolerance(None,win)
    dump(R/'Selected_Sensitivity_Study.json',{'path':str(A/'Manufacturing_Sensitivity'),'winner':win['path']})
    dump(R/'Search_Complete.json',{'verified':True,'finished':time.time()})
if __name__=='__main__':
    if len(sys.argv)>1:single()
    else:main()

