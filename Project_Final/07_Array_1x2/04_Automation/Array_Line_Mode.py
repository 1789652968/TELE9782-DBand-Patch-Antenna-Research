"""Calculate straight-section port modes and the exact native trunk eigenmode."""
from Array_Run import b,ci
import Single_Control as single
import json,sys
def mode(p):
    import cst.results as cr
    r=cr.ProjectFile(p.filename(),allow_interactive=True).get_3d();out={}
    for k in ['Gamma','Line Impedance','Effective Dielectric Constant']:
        q=r.get_result_item('1D Results\\Port Information\\'+k+'\\1(1)');x=list(q.get_xdata());y=list(q.get_ydata());i=min(range(len(x)),key=lambda j:abs(x[j]-150))
        out[k]=dict(x=x[i],real=complex(y[i]).real,imag=complex(y[i]).imag,xlabel=q.xlabel,ylabel=q.ylabel)
    return out
def calculate(de,width,near,box):
    name=f'LineMode_{round(width*1000)}um_{round(near)}';w=b.ROOT/'06_Working'/name;cache=w/'mode.json'
    if cache.exists():return json.loads(cache.read_text())
    p=single.build(de,name,dict(feed_width=width,mesh_near=near,mesh_box=box,ground_width=2.5,ground_length=1.5))
    p.model3d.add_to_history('Only solve input cross-section eigenmode','Solver.CalculateModesOnly "True"');p.save()
    p.model3d.run_solver();p.save();val=mode(p);cache.write_text(json.dumps(val,indent=2));p.close();return val
def main(preview=False):
    if preview:pars=dict(mesh_near=30,mesh_box=45,transformer_width=.055)
    else:pars=json.loads((b.ROOT/'01_CST_Project'/'parameters.json').read_text())
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        out={}
        if not preview:
            p=de.open_project(str(b.ROOT/'01_CST_Project'/'TELE9782_DBand_1x2_Array_Final.cst'))
            out['Trunk']=mode(p);p.close()
        for label,width in [('NominalTransformer',.049),('SelectedTransformer',pars['transformer_width'])]:
            out[label]=calculate(de,width,pars['mesh_near'],pars['mesh_box'])
        if not preview:(b.ROOT/'02_Simulation_Results'/'Port_Mode_Check.json').write_text(json.dumps(out,indent=2))
    finally:de.close()
if __name__=='__main__':main('preview' in sys.argv)
