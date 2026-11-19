"""Sequential full-wave screen. Restart skips completed, exported cases."""
from Array_Run import b,ci
from pathlib import Path
import json
base=dict(array_spacing=1.0,transformer_length=.308,transformer_width=.049,junction_y=-.53,ground_width=2.5,ground_length=1.5,patch_length=.513,inset_length=.19)
def solve(de,name,p,lib=b):
    folder=b.ROOT/'06_Working'/name
    if not (folder/'Farfield_150_Sphere.txt').exists():
        case=lib.build(de,name,p,monitors=[130,140,*range(146,155),160,170])
        s,_=lib.run(case)
        assert s['solver']['state']=='SUCCESS' and len(s['farfields'])==13
        lib.export_pattern(case,150,folder)
        case.save();case.close()
    s=json.loads((folder/'summary.json').read_text())
    return next(v for v in s['farfields'] if v['f_GHz']==150)
def rank(v):
    return (v['s11_dB']<=-10,v['realized_gain_dBi'] if v['s11_dB']<=-10 else -v['s11_dB'])
def main():
    import Single_Control as single
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    trials=[]
    try:
        for name,delta in [('Initial',{}),('Length',dict(patch_length=.507)),('Inset',dict(patch_length=.507,inset_length=.165)),('Transformer',dict(patch_length=.507,inset_length=.165,transformer_width=.055,transformer_length=.28))]:
            p=dict(base,**{})|delta
            trials.append((rank(solve(de,name,p)),name,p))
        _,_,feed=max(trials,key=lambda t:t[0])
        for spacing in [.90,1.10,1.20,1.30]:
            name='Spacing'+str(round(spacing*100))
            p=feed|dict(array_spacing=spacing)
            trials.append((rank(solve(de,name,p)),name,p))
        _,name,coarse=max(trials,key=lambda t:t[0])
        (b.ROOT/'06_Working'/'selection.json').write_text(json.dumps(dict(name=name,parameters=coarse,trials=trials),indent=2))
        solve(de,'Fine',coarse|dict(mesh_near=30,mesh_box=45))
        solve(de,'GroundControl',dict(patch_length=.513,inset_length=.19,ground_width=2.5,ground_length=1.5,mesh_near=30,mesh_box=45),single)
    finally:de.close()
if __name__=='__main__':main()
