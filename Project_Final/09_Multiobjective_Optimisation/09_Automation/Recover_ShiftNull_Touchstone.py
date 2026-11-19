"""Recover the interrupted Touchstone export without recomputing electromagnetic fields."""
from Round2_Core import *
import cst.results as cr
import shutil, os
def main():
    folder=V/'ShiftNull75/ShiftNull75_Delivery'; dest=folder/(folder.name+'.cst')
    if (folder/'round2.json').exists():return
    assert json.loads((folder/'summary.json').read_text())['solver']['state']=='SUCCESS'
    verification=json.loads((folder/'Reopen_Verification.json').read_text());assert verification['first']==verification['last']==0
    reader=cr.ProjectFile(str(dest),allow_interactive=False).get_3d()
    key=r'1D Results\S-Parameters\S1,1';item=reader.get_result_item(key);xx=list(item.get_xdata());yy=list(item.get_ydata())
    raw=list(csv.DictReader((folder/'1D Results_S-Parameters_S1,1.csv').open()))
    assert len(xx)==len(yy)==len(raw)==1001 and max(abs(v-complex(float(t['real']),float(t['imag']))) for v,t in zip(yy,raw))<1e-12
    ref=float(reader.get_result_item(r'1D Results\Reference Impedance\ZRef 1(1)').get_ydata()[0].real)
    out=folder/'CST_50ohm.s1p';partial=folder/'CST_50ohm.interrupted.partial'
    if out.exists() and not partial.exists():shutil.copy2(out,partial)
    new=folder/'Recovered_50ohm.s1p'
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        p=de.open_project(str(dest))
        try:
            t=p.model3d.TOUCHSTONE;t.Reset();t.FileName(str(new.with_suffix('')));t.Impedance(50);t.ExportType('S');t.Format('RI');t.FrequencyRange('Full');t.Renormalize(True);t.UseARResults(False);t.SetNSamples(0);t.Write()
        finally:p.close()
    finally:de.close()
    tab=[list(map(float,line.split())) for line in new.read_text().splitlines() if line.strip() and not line.lstrip().startswith(('!','#'))]
    assert len(tab)==1001 and all(len(row)==3 for row in tab)
    err=0
    for row,x,g in zip(tab,xx,yy):
        z=ref*(1+g)/(1-g);g50=(z-50)/(z+50);assert abs(row[0]-x)<.00005
        err=max(err,abs(complex(row[1],row[2])-g50))
    assert err<1e-5
    os.replace(new,out)
    v=metrics(folder);v.update(mode='fresh',source=str(folder.parent/'ShiftNull75_Production'),seconds=None)
    dump(folder/'Touchstone_Recovery.json',dict(samples=len(tab),max_complex_error=err,database_matched=True,reran_solver=False))
    dump(folder/'round2.json',v);print('RECOVERED',v['eta'],v['theta'],v['G0'],err,flush=True)
if __name__=='__main__':main()

