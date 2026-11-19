"""Run one named mesh or retuned geometry using a saved screening candidate."""
from Array_Optimisation import solve,ci,b
import sys,json
if __name__=='__main__':
    src,dst,*args=sys.argv[1:];pars=json.loads((b.ROOT/'06_Working'/src/'parameters.json').read_text())
    pars.update({k:float(v) for k,v in (item.split('=') for item in args)})
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:print(solve(de,dst,pars))
    finally:de.close()
