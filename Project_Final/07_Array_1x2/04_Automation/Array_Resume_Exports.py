"""Finish native exports from an already freshly solved and reopened delivery."""
from Array_Fields import ci,b,export
import json
def main():
    r=b.ROOT/'02_Simulation_Results';v=json.loads((r/'Verification.json').read_text())
    assert v['final_reopened'] and v['solver']['state']=='SUCCESS' and v['after_reopen_complex_delta']==0 and v['exported_csv_complex_delta']==0
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        p=de.open_project(v['delivered']);export(p,r,v['parameters']['array_spacing']);p.close()
    finally:de.close()
if __name__=='__main__':main()
