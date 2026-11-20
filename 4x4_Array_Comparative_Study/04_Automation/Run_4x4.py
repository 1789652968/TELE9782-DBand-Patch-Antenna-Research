"""Run one native CST solve. Resume extraction from the saved native result if needed."""
from Build_4x4 import ROOT,ci,b,build
import json,sys,time,traceback
from pathlib import Path
def dump(path,obj):path.write_text(json.dumps(obj,indent=2),encoding='utf-8')

def native_curves(p,folder,detail):
    m=p.model3d;tree=m.get_tree_items();dump(folder/'Tree.json',tree)
    assert len([x for x in tree if x.startswith('Ports\\')])==1
    m.SelectTreeItem(r'Farfields\farfield (f=150) [1]')
    ff=m.FarfieldPlot;ff.Reset();ff.Plottype('3d');ff.SelectComponent('Abs');ff.SetScaleLinear(False);ff.SetPlotRangeOnly(False);ff.Step(2);ff.Step2(2)
    for name,mode in [('Farfield_150_Sphere','directivity'),('RealizedGain_Native_150_Sphere','realized gain')]:
        ff.SetPlotMode(mode);ff.Plot()
        a=m.ASCIIExport;a.Reset();a.FileName(str(folder/(name+'.txt')));a.Execute()
    t=m.TOUCHSTONE;t.Reset();t.FileName(str(folder/'CST_50ohm'));t.Impedance(50);t.ExportType('S');t.Format('RI');t.FrequencyRange('Full');t.Renormalize(True);t.UseARResults(False);t.SetNSamples(0);t.Write()
    if not detail:return
    assert m.SelectTreeItem(next(k for k in tree if k.startswith('2D/3D Results') and 'e-field' in k.lower() and '(f=150)' in k.lower()))
    c=json.loads((folder/'parameters.json').read_text());g=json.loads((folder/'layout.json').read_text())
    pts=folder/'Patch_Field_Probes_mm.txt'
    pts.write_text(''.join(f"{u['x']} {u['probe_y']} {c['substrate_h']/2}\n" for u in g['patches']))
    a=m.ASCIIExport;a.Reset();a.FileName(str(folder/'Patch_Feed_Ez150.txt'));a.SetPointFile(str(pts));a.Execute()
    assert m.SelectTreeItem(next(k for k in tree if k.startswith('2D/3D Results') and 'surface current' in k.lower() and '(f=150)' in k.lower()))
    a.Reset();a.FileName(str(folder/'Surface_Current_150.txt'));a.Mode('FixedNumber');a.StepX(125);a.StepY(125);a.StepZ(3);a.Execute()
    assert m.SelectTreeItem('Components')
    m.Plot.DrawWorkplane('False');m.Plot.DrawBox(False);m.Plot.RestoreView('Front');m.Plot.ZoomToStructure();m.Plot.ExportImage(str(folder/'Geometry.png'),1250,1000)

def main():
    name=sys.argv[1];changes=json.loads(sys.argv[2]) if len(sys.argv)>2 else {}
    detail='--detail' in sys.argv;extract='--extract' in sys.argv
    folder=ROOT/'01_CST_Project'/name;dest=folder/(name+'.cst')
    if (folder/'Export_Complete.json').exists():
        print('COMPLETE',name);return
    start=time.time();p=None
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        p=de.open_project(str(dest)) if dest.is_file() else build(de,folder,changes)
        print('READY',name,flush=True)
        if extract:
            s,_=b.extract(p,export_frequencies={145,150,154})
        else:
            s,_=b.run(p,export_frequencies={145,150,154})
        assert s['solver']['state']=='SUCCESS',s['solver']
        p.close();p=None
        p=de.open_project(str(dest))
        native_curves(p,folder,detail)
        dump(folder/'Export_Complete.json',dict(state='SUCCESS',reopened=True,detailed=detail,wall_seconds=round(time.time()-start,1),wall_scope='export_only' if extract else 'solve_and_export',native_solver_run_reused=extract))
        print('COMPLETE',name,flush=True)
    except Exception:
        if folder.exists():(folder/'Run_Failure.txt').write_text(traceback.format_exc(),encoding='utf-8')
        raise
    finally:
        if p:
            try:p.close()
            except RuntimeError:pass
        try:de.close()
        except RuntimeError:pass
if __name__=='__main__':main()

