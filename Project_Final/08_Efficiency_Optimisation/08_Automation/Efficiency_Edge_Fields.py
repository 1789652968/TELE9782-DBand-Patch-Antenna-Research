"""Sample a near-edge field proxy at equal offsets from side edges. No solver invocation."""
from Efficiency_CST import *
def main():
    while not (T/'selection.json').exists():time.sleep(10)
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        for folder in [D/'A_Gold_PI',*(T/n for n in ['H30','H50','H60','H75'] )]:
            if not (folder/'completed.json').is_file():continue
            cfg=json.loads((folder/'parameters.json').read_text());p=de.open_project(str(folder/(folder.name+'.cst')))
            try:
                m=p.model3d;key=next(k for k in m.get_tree_items() if k.startswith('2D/3D Results') and 'e-field' in k.lower() and '(f=150)' in k)
                assert m.SelectTreeItem(key)
                pts=folder/'Edge_Points_mm.txt';pts.write_text(''.join(f"{sg*(cfg['ground_width']/2-u)} {y} {cfg['substrate_h']/2}\n" for sg in [-1,1] for u in [.03,.06,.09] for y in [-.15,0,.15]))
                a=m.ASCIIExport;a.Reset();a.FileName(str(folder/'Edge_Field_150.txt'));a.SetPointFile(str(pts));a.Execute()
            finally:p.close()
    finally:de.close()
    (R/'Edge_Exports_Complete.txt').write_text('150 GHz E-field samples exported from saved CST monitor results.')
if __name__=='__main__':main()
