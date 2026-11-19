"""Second-stage resonance tuning and mesh selection. Serial jobs with explicit checkpoints."""
from Array_Results_Extraction import *
import subprocess,os,time,sys
CST=Path(os.getenv('CST_INSTALLPATH_2024',r'D:\TELE9782\CST Studio Suite 2024'))/'Opera/code/bin/python.exe'
AUTO=ROOT/'04_Automation'
def call(script,*args):
    log=W/(Path(script).stem+'_'+('_'.join(args[:2]) or 'job')+'.log')
    with log.open('w',encoding='utf-8') as f:
        subprocess.run([str(CST),'-u',str(AUTO/script),*args],stdout=f,stderr=subprocess.STDOUT,check=True)
def ref(src,dst,**params):
    if not (W/dst/'Farfield_150_Sphere.txt').exists():call('Array_Refine.py',src,dst,*[f'{k}={v}' for k,v in params.items()])
    return metrics(W/dst)
def score(v):return (v['S11_dB']<=-10 and abs(v['sphere_mean']-1)<.02 and v['theta_deg']<=16,v['realized_gain_dBi'])
def main():
    while not (W/'GroundControl'/'Farfield_150_Sphere.txt').is_file():time.sleep(10)
    initial=read(W/'selection.json')['name'];fine=metrics(W/'Fine');coarse=metrics(W/initial)
    choice='Fine';previous=initial
    ret=ref('Spacing120','Spacing120_Retuned',patch_length=.513)
    if score(ret)[0] and (score(ret)[1]>score(coarse)[1]-.15 or not score(fine)[0]):
        fr=ref('Spacing120_Retuned','RetunedFine',mesh_near=30,mesh_box=45)
        if score(fr)>score(fine):
            choice='RetunedFine';previous='Spacing120_Retuned';fine=fr;coarse=ret
    if not score(fine)[0] or abs(fine['Dmax_dBi']-coarse['Dmax_dBi'])>.19 or abs(fine['realized_gain_dBi']-coarse['realized_gain_dBi'])>.35 or abs(fine['fmin_GHz']/coarse['fmin_GHz']-1)>.009 or abs(audit(W/choice)['farfield_checks'][6].get('power_balance_residual_percent_accepted',0))>2:
        finer=ref(choice,'Refined',mesh_near=36,mesh_box=54)
        previous=choice;choice='Refined';fine=finer
    log=dict(initial_screen=initial,selected_mesh=choice,previous_mesh=previous,physical_metrics=fine)
    (W/'engineering_selection.json').write_text(json.dumps(log,indent=2))
    print('ENGINEERING_SELECTION',choice,flush=True)
    if not (W/'final_source.json').is_file():call('Array_Fixed_Reference.py',choice)
    if not (R/'Verification.json').is_file():call('Array_Rerun.py','Final50')
    if not (R/'Port_Mode_Check.json').is_file():call('Array_Line_Mode.py')
if __name__=='__main__':main()
