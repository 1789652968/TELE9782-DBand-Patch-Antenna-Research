"""Verify the original and selected native CST databases without modifying their projects."""
from Build_4x4 import ROOT, BASE
import csv,json,sys
import cst.results as cr
def compare(folder):
    path=next(folder.glob('*.cst'));r=cr.ProjectFile(str(path),allow_interactive=False).get_3d()
    terms=('Power Accepted','Power Radiated','Loss in Metals','Loss in Dielectrics','Power Absorbed at all Ports')
    nodes=[r'1D Results\S-Parameters\S1,1',r'1D Results\Reference Impedance\ZRef 1(1)']+[r'1D Results\Power\Excitation [1]'+'\\'+k for k in terms]
    out={}
    for key in nodes:
        item=r.get_result_item(key);x=list(item.get_xdata());y=list(item.get_ydata())
        name=key.replace('\\','_').replace('/','_').replace(':','_')+'.csv'
        with (folder/name).open(newline='') as f:raw=list(csv.DictReader(f))
        assert len(x)==len(y)==len(raw)
        dx=max(abs(a-float(b['x'])) for a,b in zip(x,raw))
        dy=max(abs(a-complex(float(b['real']),float(b['imag']))) for a,b in zip(y,raw))
        assert dx<1e-9 and dy<1e-9,key
        out[key]={'points':len(x),'maximum_x_delta':dx,'maximum_complex_y_delta':dy}
    return {'source':str(path),'reopened_read_only':True,'series':out}
if __name__=='__main__':
    f=ROOT/'02_Simulation_Results/Verification';f.mkdir(parents=True,exist_ok=True)
    folder=ROOT/'01_CST_Project'/sys.argv[1]
    (f/'Native_Database_Readback.json').write_text(json.dumps([compare(BASE),compare(folder)],indent=2),encoding='utf-8')
    print('VERIFIED_NATIVE_READBACK',folder.name,flush=True)

