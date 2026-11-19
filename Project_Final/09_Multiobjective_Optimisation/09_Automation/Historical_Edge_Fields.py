"""Use identical, dimension-normalized near-edge probes on the two historical solved models."""
from Round2_Core import *
def main():
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        for label in ['PreviousArray','FirstOptimised']:
            folder=DI/label;dest=folder/(label+'.cst');cfg=read_params(folder);c=cfg
            if (folder/'Radiating_Edge_Efield_150.txt').exists():continue
            p=de.open_project(str(dest))
            try:
                m=p.model3d;key=next(k for k in m.get_tree_items() if k.startswith('2D/3D Results') and 'e-field' in k.lower() and '(f=150)' in k.lower());assert m.SelectTreeItem(key)
                d=c['array_spacing']/2;l=c['patch_length'];h=c['substrate_h'];w=c['patch_width']
                pts=folder/'Radiating_Edge_Efield_150_Points.txt';pts.write_text(''.join(f'{sg*d+dx*w} {sy*(l/2-.004)} {h/2}\n' for sg in [-1,1] for sy in [-1,1] for dx in [-.33,-.20,0,.20,.33]))
                a=m.ASCIIExport;a.Reset();a.FileName(str(folder/'Radiating_Edge_Efield_150.txt'));a.SetPointFile(str(pts));a.Execute()
            finally:p.close()
    finally:de.close()
if __name__=='__main__':main()

