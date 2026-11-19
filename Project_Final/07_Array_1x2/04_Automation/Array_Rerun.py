"""Publish selected mesh, close/reopen, solve freshly, close/reopen and verify raw data."""
from Array_Run import b,ci
from Array_Fields import export as fields
import json,csv,shutil,sys
from pathlib import Path
def main(source='Fine'):
    folder=b.ROOT/'06_Working'/source;dest=b.ROOT/'01_CST_Project'/'TELE9782_DBand_1x2_Array_Final.cst'
    out=b.ROOT/'02_Simulation_Results';key=r'1D Results\S-Parameters\S1,1'
    old=json.loads((folder/'summary.json').read_text())
    pars=json.loads((folder/'parameters.json').read_text())
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        p=de.open_project(str(folder/(source+'.cst')))
        orig=b.result_data(p)[key];p.save(str(dest),include_results=True);p.close()
        p=de.open_project(str(dest));m=p.model3d;tree=m.get_tree_items()
        actual={m.GetParameterName(i):float(m.GetParameterSValue(i)) for i in range(m.GetNumberOfParameters())}
        assert actual==pars
        port=[t for t in tree if t.startswith('Ports\\')];assert len(port)==1
        mon=[t for t in tree if t.startswith('Field Monitors\\farfield')];assert len(mon)==13
        def diff(a,c):
            assert list(a['x'])==list(c['x'])
            return max(abs(complex(x)-complex(y)) for x,y in zip(a['y'],c['y']))
        before=diff(orig,b.result_data(p)[key]);assert before<1e-12
        s,d=b.run(p);assert s['solver']['state']=='SUCCESS'
        fresh=diff(orig,d[key])
        prev={t['f_GHz']:t for t in old['farfields']}
        ffdelta={k:max(abs(t[k]-prev[t['f_GHz']][k]) for t in s['farfields']) for k in ('Dmax_dBi','realized_gain_dBi','rad_eff_dB','total_eff_dB')}
        p.save();p.close();p=de.open_project(str(dest));m=p.model3d;after=diff(d[key],b.result_data(p)[key])
        path=dest.parent/'1D Results_S-Parameters_S1,1.csv'
        with path.open() as fp: rows=list(csv.DictReader(fp))
        saved=diff(dict(x=[float(v['x']) for v in rows],y=[complex(float(v['real']),float(v['imag'])) for v in rows]),d[key])
        b.export_pattern(p,150,out)
        m.SelectTreeItem('Components');m.Plot.DrawWorkplane('False');m.Plot.DrawBox(False);m.Plot.RestoreView('Front');m.Plot.ZoomToStructure();m.Plot.ExportImage(str(out/'Geometry_Top.png'),1400,1000)
        m.SelectTreeItem(port[0]);m.Plot.RestoreView('Perspective');m.Plot.ZoomToStructure();m.Plot.ExportImage(str(out/'Port.png'),1400,1000)
        ver=dict(source=source,delivered=str(dest),before_rerun_complex_delta=before,rerun_complex_delta=fresh,after_reopen_complex_delta=after,exported_csv_complex_delta=saved,farfields_rerun_max_deltas_dB=ffdelta,port=port,monitors=mon,parameters=actual,solver=m.get_solver_run_info(),sample_count=len(rows),final_reopened=True)
        (dest.parent/'parameters.json').write_text(json.dumps(actual,indent=2))
        (out/'Verification.json').write_text(json.dumps(ver,indent=2))
        assert after<1e-12 and saved<1e-12 and s['solver']['state']=='SUCCESS'
        fields(p,out,actual['array_spacing'])
        p.save();p.close()
    finally:de.close()
if __name__=='__main__':main(*sys.argv[1:])



