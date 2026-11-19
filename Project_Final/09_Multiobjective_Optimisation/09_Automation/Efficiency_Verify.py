"""Publish native project from the selected fine grid; reopen, rerun, reopen and verify."""
from Efficiency_CST import *
def fields(p,folder,cfg):
    m=p.model3d;tree=m.get_tree_items();dump(folder/'Tree.json',tree)
    def select(word):
        key=next(k for k in tree if k.startswith('2D/3D Results') and word in k.lower() and '(f=150)' in k.lower())
        assert m.SelectTreeItem(key)
    select('e-field');pts=folder/'Field_Points_mm.txt';a=m.ASCIIExport;edge=-cfg['patch_length']/2
    ys=[cfg['junction_y']+(edge-cfg['junction_y'])*t for t in [.25,.4,.55,.7]]
    pts.write_text(''.join(f"{sg*cfg['array_spacing']/2} {y} {cfg['substrate_h']/2}\n" for y in ys for sg in [-1,1]))
    a.Reset();a.FileName(str(folder/'Branch_Ez_150.txt'));a.SetPointFile(str(pts));a.Execute()
    select('surface current');a.Reset();a.FileName(str(folder/'Surface_Current_150.txt'));a.Mode('FixedNumber');a.StepX(95);a.StepY(75);a.StepZ(2);a.Execute()
    assert m.SelectTreeItem('Components');m.Plot.DrawWorkplane('False');m.Plot.DrawBox(False);m.Plot.RestoreView('Front');m.Plot.ZoomToStructure();m.Plot.ExportImage(str(folder/'Geometry.png'),1200,840)
def main():
    while not (V/'selection.json').exists():time.sleep(10)
    # Source run has closed. Only one large solver is active at any point.
    while not (T/'PortFrequency140/completed.json').exists():time.sleep(10)
    if (V/'verification.json').exists():return
    sel=json.loads((V/'selection.json').read_text());source=V/sel['source'];par=json.loads((source/'parameters.json').read_text())
    name='TELE9782_DBand_Efficiency_Final';folder=V/name;folder.mkdir(exist_ok=True);dest=folder/(name+'.cst')
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        p=de.open_project(str(source/(source.name+'.cst')));orig=b.result_data(p);key=r'1D Results\S-Parameters\S1,1';p.save(str(dest),include_results=True);p.close()
        p=de.open_project(str(dest));m=p.model3d
        def delta(a,c):
            assert list(a[key]['x'])==list(c[key]['x']);return max(abs(x-y) for x,y in zip(a[key]['y'],c[key]['y']))
        before=delta(orig,b.result_data(p));assert before<1e-12
        parameters={m.GetParameterName(i):float(m.GetParameterSValue(i)) for i in range(m.GetNumberOfParameters())}
        assert all(parameters[k]==par[k] for k in GEOM)
        dump(folder/'parameters.json',par);s,fresh=b.run(p);assert s['solver']['state']=='SUCCESS'
        freshdiff=delta(orig,fresh);p.save();p.close();p=de.open_project(str(dest));after=delta(fresh,b.result_data(p));assert after<1e-12
        b.export_pattern(p,150,folder);fields(p,folder,par);m=p.model3d
        touch=m.TOUCHSTONE;touch.Reset();touch.FileName(str(folder/'CST_50ohm'));touch.Impedance(50);touch.ExportType('S');touch.Format('RI');touch.FrequencyRange('Full');touch.Renormalize(True);touch.UseARResults(False);touch.SetNSamples(0);touch.Write()
        v=result(folder);src=result(source)
        tree=m.get_tree_items();ports=[x for x in tree if x.startswith('Ports\\')];mon=[x for x in tree if x.startswith('Field Monitors\\farfield')]
        assert len(ports)==1 and len(mon)==13
        dump(folder/'completed.json',v);p.save();p.close()
        dump(V/'verification.json',dict(path=str(dest),previous=src,fresh=v,reopened_before_and_after=True,max_S11_complex_delta_on_first_open=before,max_S11_complex_delta_on_fresh_solve=freshdiff,max_S11_complex_delta_on_last_open=after,ports=ports,farfield_monitors=mon,parameters_read=parameters,solver=s['solver']))
    finally:de.close()
if __name__=='__main__':main()
