import os,sys,json
from pathlib import Path
base=Path(os.getenv('CST_INSTALLPATH_2024',r'D:\TELE9782\CST Studio Suite 2024'))/'AMD64'
dll=os.add_dll_directory(str(base));sys.path.insert(0,str(base/'python_cst_libraries'))
import cst.interface as ci
import Array_Build as b
root=b.ROOT
def main():
    name=sys.argv[1]
    changes=dict(array_spacing=1.0,transformer_length=.308,transformer_width=.049,junction_y=-.53,ground_width=2.5,ground_length=1.5,patch_length=.513,inset_length=.19)
    changes.update({k:float(v) for k,v in (a.split('=') for a in sys.argv[2:])})
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    p=b.build(de,name,changes,monitors=[130,140,*range(146,155),160,170])
    print('BUILT',p.filename(),flush=True)
    s,data=b.run(p)
    assert s['solver']['state']=='SUCCESS' and len(s['farfields'])==13
    b.export_pattern(p,150,Path(p.filename()).parent)
    p.save();p.close();de.close()
if __name__=='__main__':main()

