"""Native CAD top and perspective views, plus a current plot at 150 GHz."""
from Array_Run import ci,b
import sys
from pathlib import Path
def capture(p,folder):
    m=p.model3d
    for label,item in [('Geometry','Components'),('Current','2D/3D Results\\Surface Current\\surface current (f=150) [1]')]:
        assert m.SelectTreeItem(item);m.Plot.DrawBox(False);m.Plot.DrawWorkplane('False')
        for view in ['Front','Back','Perspective']:
            m.Plot.RestoreView(view);m.Plot.ZoomToStructure()
            m.Plot.ExportImage(str(folder/(label+'_'+view+'.png')),1100,800)
if __name__=='__main__':
    folder=b.ROOT/'06_Working'/sys.argv[1];de=ci.DesignEnvironment.new();de.set_quiet_mode(True);p=de.open_project(str(folder/(folder.name+'.cst')))
    try:capture(p,folder)
    finally:p.close();de.close()
