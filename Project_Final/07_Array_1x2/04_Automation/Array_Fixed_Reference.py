"""Validate exact fixed-50-ohm native S parameters on the selected physical/mesh design."""
from Array_Run import b,ci
import json,sys
def main(source):
    work=b.ROOT/'06_Working';p0=json.loads((work/source/'parameters.json').read_text());name='Final50'
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        p=b.build(de,name,p0,monitors=[130,140,*range(146,155),160,170])
        p.model3d.add_to_history('Fix scattering reference at exactly 50 ohms','Solver.AutoNormImpedance "True"\nSolver.NormingImpedance "50"')
        p.save();s,data=b.run(p);assert s['solver']['state']=='SUCCESS'
        b.export_pattern(p,150,work/name);p.save();p.close()
        (work/'final_source.json').write_text(json.dumps(dict(mesh_source=source,selected='Final50')))
    finally:de.close()
if __name__=='__main__':main(sys.argv[1])
