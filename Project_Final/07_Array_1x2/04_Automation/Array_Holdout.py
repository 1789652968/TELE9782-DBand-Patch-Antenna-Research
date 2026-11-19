"""Independent holdout mesh check and final postprocessing after the production rerun."""
from Array_Final_Selection import ref
from Array_Results_Extraction import *
import time
def main():
    while not (R/'Port_Mode_Check.json').is_file():time.sleep(10)
    v=ref('Refined','MeshHoldout',mesh_near=38,mesh_box=57)
    print('INDEPENDENT_MESH',v,flush=True)
    from Array_Postprocess import main as post
    post()
if __name__=='__main__':main()
