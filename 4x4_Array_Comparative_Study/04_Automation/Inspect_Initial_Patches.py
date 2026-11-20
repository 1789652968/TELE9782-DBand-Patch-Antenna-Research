"""Read 16 input fields and conductor-current data from the already solved initial case."""
from Run_4x4 import native_curves,ci,ROOT
from pathlib import Path
import shutil,sys,json
def main():
    name='Initial_4x4';f=ROOT/'01_CST_Project'/name
    evidence=ROOT/'06_Local_Readback/Initial_Field_Readback';evidence.mkdir(parents=True,exist_ok=True)
    p0=f/(name+'.cst');dest=evidence/p0.name
    if not dest.exists():
        shutil.copy2(p0,dest)
        shutil.copytree(p0.with_suffix(''),dest.with_suffix(''),dirs_exist_ok=True)
    for n in ('parameters.json','layout.json'):shutil.copy2(f/n,evidence/n)
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        p=de.open_project(str(dest))
        try:native_curves(p,evidence,True)
        finally:p.close()
    finally:de.close()
    for n in ('Patch_Feed_Ez150.txt','Patch_Field_Probes_mm.txt','Surface_Current_150.txt','Geometry.png'):
        shutil.copy2(evidence/n,f/n)
    print('INITIAL_PROBE_EXPORT_COMPLETE',flush=True)
if __name__=='__main__':main()

