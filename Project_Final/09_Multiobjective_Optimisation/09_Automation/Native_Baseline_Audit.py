"""Compare baseline exported power, S11 and impedance point for point with CST result database."""
from Round2_Core import *
import cst.results as cr
def main():
    path=next(BASE.glob('*.cst'));reader=cr.ProjectFile(str(path),allow_interactive=False).get_3d()
    keys=[k for k in reader.get_tree_items() if '1D Results' in k and any(s in k for s in ('Power\\Excitation [1]\\','S-Parameters\\S1,1','Reference Impedance\\ZRef','Efficiencies\\'))]
    out=[]
    for key in keys:
        f=BASE/(key.replace('\\','_').replace('/','_').replace(':','_')+'.csv')
        if not f.is_file():continue
        series=reader.get_result_item(key);x=list(series.get_xdata());y=list(series.get_ydata());rows=list(csv.DictReader(f.open()))
        assert len(x)==len(rows)==len(y)
        e=max(abs(complex(v)-complex(float(a['real']),float(a['imag']))) for v,a in zip(y,rows))
        dx=max(abs(float(v)-float(a['x'])) for v,a in zip(x,rows));assert dx<1.e-9 and e<1.e-9
        out.append(dict(tree=key,export=str(f),n=len(x),max_x_delta=dx,max_complex_y_delta=e))
    assert len(out)>=10
    dump(DI/'CST_Database_Export_Audit.json',out);print(len(out),'series verified',flush=True)
if __name__=='__main__':main()

