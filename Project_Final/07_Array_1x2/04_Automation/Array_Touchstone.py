"""Export CST's own 50-ohm renormalized Touchstone file from the saved full-wave result."""
from Array_Run import ci,b
import sys,json
from pathlib import Path
def main(test=False):
    w=b.ROOT/'06_Working'/'Final50';dest=w if test else b.ROOT/'02_Simulation_Results'
    file=(w/'Final50.cst') if test else b.ROOT/'01_CST_Project'/'TELE9782_DBand_1x2_Array_Final.cst'
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        p=de.open_project(str(file));m=p.model3d;touch=m.TOUCHSTONE;touch.Reset();touch.FileName(str(dest/'CST_50ohm'));touch.Impedance(50);touch.ExportType('S');touch.Format('RI');touch.FrequencyRange('Full');touch.Renormalize(True);touch.UseARResults(False);touch.SetNSamples(0);touch.Write()
        print(touch.GetFileName(),flush=True);p.close()
    finally:de.close()
if __name__=='__main__':main('test' in sys.argv)
