"""Round 2 deterministic CST runner. Store and compare the complete geometry at every run."""
from Efficiency_CST import ROOT, BASE, GEOM, ci, b, clone, corner, dump, result
from Efficiency_Verify import fields
from pathlib import Path
import sys, json, math, csv, time, traceback, hashlib, re
F=ROOT/'03_Feed_Optimisation'
H=ROOT/'04_Substrate_Patch_Optimisation'
Y=ROOT/'05_Beam_Optimisation'
A=ROOT/'06_Advanced_Candidates'
V=ROOT/'07_Final_Candidates'
R=ROOT/'08_Results_and_Figures'
DI=ROOT/'02_Diagnostics'
def sphere(path):
    rows=[list(map(float,line.split())) for line in path.read_text().splitlines()[2:] if line.strip()]
    top=max(rows,key=lambda row:row[2]); axis=next(row for row in rows if row[:2]==[0,0])
    back=next(row for row in rows if row[:2]==[180,0])
    # Uniform theta/phi mesh, discard phi=360 periodic endpoint if present.
    integral=sum(10**(r[2]/10)*math.sin(math.radians(r[0])) for r in rows if r[1]<360)*math.radians(2)**2/(4*math.pi)
    return dict(theta=top[0],phi=top[1],D0=axis[2],Dgrid=top[2],FBaxial=axis[2]-back[2],cross0_dBc=axis[3]-axis[5],sphere_mean=integral)
def metrics(folder):
    v=result(folder);v.update(sphere(folder/'Farfield_150_Sphere.txt'))
    v['G0']=v['D0']+10*math.log10(v['eta_total50']/100)
    v['path']=str(folder)
    return v
def decorate(m,c):
    d=c.get('rear_delta',0)
    if d:
        for name,mat,zrange in [('ground','Gold',('-metal_thickness','0')),('substrate','Polyimide (lossy)',('0','substrate_h'))]:
            aux='rear_'+name; y0='ground_length/2'; y1=f'ground_length/2+({d})'
            piece=b.brick(aux,mat,('-ground_width/2','ground_width/2'),(y0,y1) if d>0 else (y1,y0),zrange)
            op='Add' if d>0 else 'Subtract'
            m.add_to_history('Finite +Y edge '+name,piece+f'Solid.{op} "antenna:{name}","antenna:{aux}"')
    if c.get('strip'):
        for side in [-1,1]:
            x=side*c['array_spacing']/2; w=c.get('strip_w',c['patch_width']*.95)
            y=c['patch_length']/2+c.get('strip_gap',.08)
            m.add_to_history('Passive gold loading '+str(side),b.brick('par'+('L' if side<0 else 'R'),'Gold',(x-w/2,x+w/2),(y,y+c['strip']),('substrate_h','substrate_h+metal_thickness')))
    if c.get('miter') or c.get('fillet'):corner(m,c)
def read_params(folder):return json.loads((folder/'parameters.json').read_text(encoding='utf-8-sig'))
def finish_exports(p,folder,cfg,mode,source,start):
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
    dump(folder/'round2.json',v);print('DONE',folder.name,round(v['eta'],3),v['theta'],round(v['G0'],3),round(v['S11_50'],2),flush=True);return v
def run(de,stage,name,change,mode='screen',source=None):
    folder=stage/name;folder.mkdir(parents=True,exist_ok=True)
    cfg=GEOM|dict(mesh_near=20,mesh_box=30)|change
    out=folder/'round2.json'
    if out.exists():
        assert read_params(folder)==cfg
        return json.loads(out.read_text())
    if (folder/'parameters.json').exists():assert read_params(folder)==cfg
    dest=folder/(name+'.cst'); start=time.time();p=None
    try:
        if dest.exists() and (folder/'summary.json').is_file() and (not source or (folder/'Reopen_Verification.json').is_file()):
            status=json.loads((folder/'summary.json').read_text())['solver']['state']
            assert status=='SUCCESS' and read_params(folder)==cfg
            p=de.open_project(str(dest));stored=b.result_data(p)[r'1D Results\S-Parameters\S1,1']
            rows=list(csv.DictReader((folder/'1D Results_S-Parameters_S1,1.csv').open()))
            assert len(stored['y'])==len(rows)==1001
            assert max(abs(v-complex(float(r['real']),float(r['imag']))) for v,r in zip(stored['y'],rows))<1e-12
            print('RESUME_NATIVE_EXPORT',name,flush=True)
            return finish_exports(p,folder,cfg,mode,source,start)
        if source:
            p=de.open_project(str(source/(source.name+'.cst')))
            old=b.result_data(p);p.save(str(dest),include_results=True);p.close();p=None
            p=de.open_project(str(dest));again=b.result_data(p)
            key=r'1D Results\S-Parameters\S1,1'
            def diff(a,c):
                assert list(a[key]['x'])==list(c[key]['x']);return max(abs(x-y) for x,y in zip(a[key]['y'],c[key]['y']))
            first=diff(old,again);assert first<1e-12
        elif dest.exists() and (folder/'setup_ready.json').exists():p=de.open_project(str(dest))
        else:
            if dest.exists():raise RuntimeError('Incomplete geometry setup: preserve and inspect before retry')
            path=clone(folder,cfg);p=de.open_project(str(path));m=p.model3d
            for k in GEOM:m.StoreParameter(k,str(cfg[k]))
            m.full_history_rebuild();decorate(m,cfg)
            if mode in ('production','dense'):b.add_monitors(p,[145])
            p.save();dump(folder/'setup_ready.json',True)
        dump(folder/'parameters.json',cfg);print('START',name,mode,flush=True)
        s,data=b.run(p,export_frequencies={150} if mode=='sensitivity' else None);assert s['solver']['state']=='SUCCESS'
        if source:
            freshdiff=diff(old,data);p.save();p.close();p=None;p=de.open_project(str(dest))
            finaldiff=diff(data,b.result_data(p));assert finaldiff<1e-12
            m=p.model3d
            pars={m.GetParameterName(i):float(m.GetParameterSValue(i)) for i in range(m.GetNumberOfParameters())}
            assert all(abs(pars[k]-cfg[k])<1e-9 for k in GEOM)
            ports=[k for k in m.get_tree_items() if k.startswith('Ports\\')];assert len(ports)==1
            dump(folder/'Reopen_Verification.json',dict(first=first,fresh=freshdiff,last=finaldiff,ports=ports,parameters=pars))
        return finish_exports(p,folder,cfg,mode,source,start)
    except Exception as e:
        print('FAILED',name,traceback.format_exc(),flush=True)
        dump(folder/'error.json',dict(error=repr(e),traceback=traceback.format_exc(),time=time.time()))
        raise
    finally:
        if p:p.close()
def thick(h):
    return dict(substrate_h=h,feed_width=round(.1688*h/.075,4),transformer_width=round(.1031*h/.075,4),patch_length=round(.5148-.46*(h-.075),4))
def main():
    print('BASE',metrics(BASE),flush=True);dump(DI/'Baseline_Raw_Recalculation.json',metrics(BASE))
    jobs=[(F,'Control20',{}),(Y,'RearShort',dict(rear_delta=-.32)),(Y,'RearLong',dict(rear_delta=.45)),(F,'Compact',dict(junction_y=-.345,miter=True,fillet=True)),(H,'H095',thick(.095)),(H,'H110',thick(.110)),(H,'H085',thick(.085)),(H,'H070',thick(.070)),(H,'H060',thick(.060)),(H,'Spacing100',dict(array_spacing=1.00)),(H,'Spacing125',dict(array_spacing=1.25)),(H,'WidePatch',dict(patch_width=.78)),(Y,'WideGround',dict(ground_width=3.15)),(Y,'PassiveRear',dict(strip=.16,strip_gap=.09)),(F,'WideTransformer',dict(transformer_width=.123,transformer_length=.245))]
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        for stage,name,c in jobs:run(de,stage,name,c)
    finally:de.close()
if __name__=='__main__':main()

