"""One bounded follow-up after the original search: bracket the observed Y-plane reversal and reverse the inset matching trend."""
from Round2_Search import *
import shutil
def safe_copy(p,q):
    if p.exists() and not q.exists():shutil.copy2(p,q)
def main():
    marker=R/'Targeted_Complete.json'
    if marker.exists():return
    for n in ['Final_Selection','Verification_Results','Screen_Selection']:
        safe_copy(V/(n+'.json'),V/(n+'_Initial.json'))
    oldverified=json.loads((V/'Verification_Results_Initial.json').read_text())
    oldsel=json.loads((V/'Final_Selection_Initial.json').read_text())
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        rows=completed();by={q['name']:q for q in rows}
        control=by['Control20'];positive=by['FeedShiftPlus']
        assert control['phi']==90 and positive['phi']==270
        mid=round(.24*control['theta']/(control['theta']+positive['theta']),3)
        jobs=[(Y,'ShiftBracket75',dict(shift_y=mid)),(Y,'ShiftBracket85',thick(.085)|dict(shift_y=mid+.015)),
              (Y,'ShiftBracketWideGround',thick(.085)|dict(shift_y=mid-.015,ground_width=2.85,rear_delta=-.045)),
              (H,'H095DeepInset',thick(.095)|dict(inset_length=.194)),
              (H,'H110DeepInset',thick(.110)|dict(inset_length=.202,transformer_length=.26)),
              (Y,'ShiftBracket95',thick(.095)|dict(shift_y=mid+.005,inset_length=.191,ground_width=2.85))]
        for stage,name,c in jobs:run(de,stage,name,c)
        final_jobs(de)
        tested=oldverified|json.loads((V/'Verification_Results.json').read_text())
        dump(V/'Verification_Results.json',tested)
        viable=[t['fresh'] for t in tested.values() if t['accepted'] and t['eta_range']<=1.2 and t['beam_range']<=4]
        if viable:
            selected=roles(viable);sel={role:v['path'] for role,v in selected.items()}
            dump(V/'Final_Selection.json',sel);win=selected['Best_Balanced']
            if win['path']!=oldsel.get('Best_Balanced'):
                import Round2_Search as search
                # New directory preserves all earlier tolerance runs and their native projects.
                branch=A/('Robustness_'+Path(win['path']).parent.name);branch.mkdir(exist_ok=True)
                original_root=search.A;search.A=branch
                try:search.tolerance(de,win)
                finally:search.A=original_root
                study=branch/'Manufacturing_Sensitivity'
            else:study=A/'Manufacturing_Sensitivity'
            dump(R/'Selected_Sensitivity_Study.json',{'path':str(study),'winner':win['path']})
        else:dump(V/'Final_Selection.json',{'fallback':str(BASE),'reason':'No independently stable new finalist'})
        dump(marker,dict(complete=True,shift_proposal_mm=mid,reason='Two measured opposite Y-plane beam directions; phase-centre hypothesis checked with fresh solves.',jobs=[n for _,n,_ in jobs]))
    finally:de.close()
if __name__=='__main__':main()

