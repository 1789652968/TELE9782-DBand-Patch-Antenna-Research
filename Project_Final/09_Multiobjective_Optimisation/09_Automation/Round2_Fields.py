"""Sample complex near fields from real solved result sets; isolated historical copies only."""
from Round2_Core import *
import shutil
from Round2_Angular_Resolution import complete_angular
def export_xy(p,folder,c):
    m=p.model3d;tree=m.get_tree_items();key=next(k for k in tree if k.startswith('2D/3D Results') and 'e-field' in k.lower() and '(f=150)' in k.lower());assert m.SelectTreeItem(key)
    points=folder/'XY_Points_mm.txt'
    ymin=-c['ground_length']/2; ymax=c['ground_length']/2+c.get('rear_delta',0);w=c['ground_width']; z=c['substrate_h']/2
    points.write_text(''.join(f'{-.495*w+.99*w*i/64:.7f} {ymin+.005+(ymax-ymin-.01)*j/48:.7f} {z:.7f}\n' for j in range(49) for i in range(65)))
    a=m.ASCIIExport;a.Reset();a.FileName(str(folder/'Efield_XY_150.txt'));a.SetPointFile(str(points));a.Execute()
def main():
    old=ROOT.parent/'07_Array_1x2/01_CST_Project';selected={} if '--history' in sys.argv else json.loads((V/'Final_Selection.json').read_text())
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        for label,src in [('PreviousArray',old),('FirstOptimised',BASE)]:
            folder=DI/label;folder.mkdir(exist_ok=True)
            if (folder/'Efield_XY_150.txt').exists():continue
            orig=next(src.glob('*.cst'));dest=folder/(label+'.cst')
            if not dest.exists():shutil.copy2(orig,dest);shutil.copytree(orig.with_suffix(''),dest.with_suffix(''),dirs_exist_ok=True)
            cfg=read_params(src);dump(folder/'parameters.json',cfg);p=de.open_project(str(dest))
            try:export_xy(p,folder,cfg)
            finally:p.close()
        for path in dict.fromkeys(selected.values()):
            folder=Path(path)
            if (folder/'Efield_XY_150.txt').exists() and complete_angular(folder/'Farfield_150_1deg_Directivity.txt'):continue
            # An isolated result-bearing copy avoids changing the delivery validation or its hash.
            label=folder.name+'_FieldView';view=DI/label;view.mkdir(exist_ok=True)
            orig=folder/(folder.name+'.cst');dest=view/(label+'.cst')
            if not dest.exists():shutil.copy2(orig,dest);shutil.copytree(orig.with_suffix(''),dest.with_suffix(''),dirs_exist_ok=True)
            p=de.open_project(str(dest))
            try:
                from Round2_Angular_Resolution import export
                export(p,folder);export_xy(p,folder,read_params(folder))
            finally:p.close()
    finally:de.close()
if __name__=='__main__':main()

