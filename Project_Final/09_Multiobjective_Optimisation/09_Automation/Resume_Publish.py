"""Generate the final reviewed deliverables as soon as sequential solver validation closes."""
from pathlib import Path
import os, subprocess, sys, time
here=Path(__file__).resolve().parent;root=here.parent;results=root/'08_Results_and_Figures'
native=root.parents[1]/'CST Studio Suite 2024/Opera/code/bin/python.exe'
numerical=Path(r'C:\Users\Admin\AppData\Local\spyder-6\envs\spyder-runtime')
def main():
    while not (results/'Search_Complete.json').is_file():time.sleep(12)
    for name in ['Round2_Port.py','Round2_Fields.py']:
        if name=='Round2_Port.py' and (results/'Port_Mode_Sensitivity.json').is_file():continue
        print('START',name,flush=True)
        for trial in range(2):
            rc=subprocess.run([str(native),'-u',str(here/name)],cwd=here).returncode
            if rc==0:break
        else:raise RuntimeError(name)
    env=os.environ.copy();env['PATH']=str(numerical)+';'+str(numerical/'Library/bin')+';'+env['PATH']
    subprocess.run([str(numerical/'python.exe'),'-u',str(here/'Round2_Delivery.py')],env=env,check=True,cwd=here)
    assert (root/'10_Documentation/Final_Optimisation_Report.md').is_file()
    assert (results/'Deliverable_Audit.json').is_file()
    print('DONE Final engineering report, CST evidence and figures',flush=True)
if __name__=='__main__':main()

