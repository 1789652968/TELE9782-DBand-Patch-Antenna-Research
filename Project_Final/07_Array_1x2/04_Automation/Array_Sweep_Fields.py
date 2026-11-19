"""Read completed spacing projects once the serial solver has advanced to its next case."""
from Array_Fields import b,ci,export
import json,time
def main():
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True);w=b.ROOT/'06_Working'
    try:
        for name,next_name in [('Inset','Transformer'),('Transformer','Spacing90'),('Spacing90','Spacing110'),('Spacing110','Spacing120'),('Spacing120','Spacing130'),('Spacing130','Fine')]:
            path=w/name
            while not (w/next_name/(next_name+'.cst')).is_file():time.sleep(10)
            if (path/'Surface_Current_150.txt').exists():continue
            p=de.open_project(str(path/(name+'.cst')))
            try:export(p,path,json.loads((path/'parameters.json').read_text())['array_spacing'])
            finally:p.close()
            print('FIELDS',name,flush=True)
    finally:de.close()
if __name__=='__main__':main()
