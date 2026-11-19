"""Resume completed solves from the saved native database if a graphical export was interrupted."""
from pathlib import Path
here=Path(__file__).resolve().parent
p=here/'Array_Build.py'
s=p.read_text(encoding='utf-8-sig')
s=s.replace("    m.Plot.ExportImage(str(folder/f'Farfield_{f:g}_CST.png'),1400,1000)", "    if f==150 and not (folder/f'Farfield_{f:g}_CST.png').exists():\n        m.Plot.ExportImage(str(folder/f'Farfield_{f:g}_CST.png'),1100,780)")
p.write_text(s,encoding='utf-8')
p=here/'Round2_Core.py';s=p.read_text(encoding='utf-8-sig')
start=s.index('        for f in ([145,150,154]');end=s.index('    except Exception as e:',start)
s=s[:start]+'''        return finish_exports(p,folder,cfg,mode,source,start)
'''+s[end:]
insert=s.index('def run(')
s=s[:insert]+r'''def finish_exports(p,folder,cfg,mode,source,start):
    for f in ([145,150,154] if mode in ('production','dense','fresh') else [150]):
        if not (folder/f'Farfield_{f}_Sphere.txt').is_file() or (f==150 and not (folder/'Farfield_150_CST.png').is_file()):
            b.export_pattern(p,f,folder)
    if mode in ('fresh','production'):
        if not all((folder/n).is_file() for n in ['Geometry.png','Aperture_Efield_150.txt','Surface_Current_150.txt','Radiating_Edge_Efield_150.txt']):fields(p,folder,cfg)
        m=p.model3d
        assert m.SelectTreeItem(r'Farfields\farfield (f=150) [1]')
        ff=m.FarfieldPlot;ff.Reset();ff.Plottype('3d');ff.SetPlotMode('realized gain');ff.SelectComponent('Abs');ff.SetScaleLinear(False);ff.SetPlotRangeOnly(False);ff.Step(2);ff.Step2(2);ff.Plot()
        a=m.ASCIIExport;a.Reset();a.FileName(str(folder/'RealizedGain_Native_150_Sphere.txt'));a.Execute()
        t=m.TOUCHSTONE;t.Reset();t.FileName(str(folder/'CST_50ohm'));t.Impedance(50);t.ExportType('S');t.Format('RI');t.FrequencyRange('Full');t.Renormalize(True);t.UseARResults(False);t.SetNSamples(0);t.Write()
    v=metrics(folder);v.update(mode=mode,seconds=round(time.time()-start,1),source=str(source) if source else None)
    p.save();dump(folder/'round2.json',v);print('DONE',folder.name,round(v['eta'],3),v['theta'],round(v['G0'],3),round(v['S11_50'],2),flush=True);return v
''' +s[insert:]
needle='        if source:\n            p=de.open_project'
assert needle in s
s=s.replace(needle,r'''        if dest.exists() and (folder/'summary.json').is_file() and (not source or (folder/'Reopen_Verification.json').is_file()):
            status=json.loads((folder/'summary.json').read_text())['solver']['state']
            assert status=='SUCCESS' and read_params(folder)==cfg
            p=de.open_project(str(dest));stored=b.result_data(p)[r'1D Results\S-Parameters\S1,1']
            rows=list(csv.DictReader((folder/'1D Results_S-Parameters_S1,1.csv').open()))
            assert len(stored['y'])==len(rows)==1001
            assert max(abs(v-complex(float(r['real']),float(r['imag']))) for v,r in zip(stored['y'],rows))<1e-12
            print('RESUME_NATIVE_EXPORT',name,flush=True)
            return finish_exports(p,folder,cfg,mode,source,start)
        if source:
            p=de.open_project''')
p.write_text(s,encoding='utf-8')

