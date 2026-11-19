"""Extract paired local Ez and CST surface-current displays from saved monitors."""
from Array_Run import b,ci
import json,sys
from pathlib import Path
def export(p,folder,spacing):
    m=p.model3d;tree=m.get_tree_items();(folder/'Tree.json').write_text(json.dumps(tree,indent=2))
    def select(word):
        return next(x for x in tree if x.startswith('2D/3D Results') and word.lower() in x.lower() and '(f=150)' in x.lower())
    e=select('e-field');assert m.SelectTreeItem(e)
    points=folder/'Field_Points_mm.txt'
    points.write_text(''.join(f'{side*spacing/2} {y} 0.020\n' for y in [-.43,-.39,-.35,-.31] for side in [-1,1]))
    a=m.ASCIIExport;a.Reset();a.FileName(str(folder/'Branch_Ez_150.txt'));a.SetPointFile(str(points));a.Execute()
    current=select('surface current');assert m.SelectTreeItem(current)
    m.Plot.DrawWorkplane('False');m.Plot.RestoreView('Front');m.Plot.ZoomToStructure()
    m.Plot.ExportImage(str(folder/'Surface_Current_150.png'),1400,1000)
    a.Reset();a.FileName(str(folder/'Surface_Current_150.txt'));a.Mode('FixedNumber');a.StepX(95);a.StepY(75);a.StepZ(2);a.Execute()
def main():
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        for name in sys.argv[1:]:
            folder=b.ROOT/'06_Working'/name
            p=de.open_project(str(folder/(name+'.cst')))
            try:export(p,folder,json.loads((folder/'parameters.json').read_text())['array_spacing'])
            finally:p.close()
    finally:de.close()
if __name__=='__main__':main()


