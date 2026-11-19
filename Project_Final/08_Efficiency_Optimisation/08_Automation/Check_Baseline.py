"""Read-only provenance and native-CST vs CSV check on the backup."""
from Efficiency_CST import *
import cst.results as cr
import hashlib
def main():
    original=ROOT.parent/'07_Array_1x2/01_CST_Project'
    def sha(p):
        h=hashlib.sha256()
        with p.open('rb') as f:
            for buf in iter(lambda:f.read(1024*1024),b''):h.update(buf)
        return h.hexdigest()
    checked={}
    for f in BASE.rglob('*'):
        if f.is_file():k=str(f.relative_to(BASE));a=sha(f);assert a==sha(original/k),k;checked[k]=a
    r=cr.ProjectFile(str(NATIVE)).get_3d();raw={}
    for k in ['Power Accepted','Power Radiated','Loss in Metals','Loss in Dielectrics','Power Absorbed at all Ports','Power Outgoing all Ports','Power Stimulated']:
        q=r.get_result_item('1D Results\\Power\\Excitation [1]\\'+k);x=q.get_xdata();i=min(range(len(x)),key=lambda i:abs(x[i]-150));assert abs(x[i]-150)<1e-5
        val=complex(q.get_ydata()[i]).real;assert abs(val-row_at(BASE,k))<1e-10;raw[k]=val
    dump(ROOT/'01_Baseline_Copy/Native_Provenance.json',dict(original=str(original),files_verified=len(checked),sha256=checked,power_read_directly_from_CST_results_W=raw))
if __name__=='__main__':main()
