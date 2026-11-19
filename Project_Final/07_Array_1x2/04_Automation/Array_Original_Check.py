"""Read the archived original native CST results without opening an editable design."""
from Array_Run import b
import cst.results as cr
import json,csv,math
def main():
    orig=b.ROOT.parent;file=orig/'01_CST_Project'/'TELE9782_DBand_Patch_Final.cst';folder=orig/'02_Simulation_Results';native=cr.ProjectFile(str(file)).get_3d()
    q=native.get_result_item(r'1D Results\S-Parameters\S1,1');f=list(q.get_xdata());gamma=list(q.get_ydata());i=min(range(len(f)),key=lambda j:abs(f[j]-150))
    with (folder/'CST_Raw'/'1D Results_S-Parameters_S1,1.csv').open() as fp:r=list(csv.DictReader(fp))
    assert len(r)==len(f) and all(abs(float(t['x'])-freq)<1e-8 for t,freq in zip(r,f))
    err=max(abs(complex(float(v['real']),float(v['imag']))-g) for v,g in zip(r,gamma));assert err<1e-9
    history=json.loads((file.with_suffix('')/'Model/3D/ModelHistory.json').read_text(encoding='utf-8-sig'))
    cmds='\n'.join('\n'.join(v['code']) for v in history['history'])
    ref=native.get_result_item(r'1D Results\Reference Impedance\ZRef 1(1)')
    out=dict(original_native_project=str(file),sweep_sample_count=len(f),S11_150GHz_native_dB=20*math.log10(abs(gamma[i])),reference_ohm=float(complex(ref.get_ydata()[i]).real),maximum_native_vs_archived_trace_difference=err,native_history_captions=[v['caption'] for v in history['history']],material_gold_sigma='4.561e+007' in cmds,near_model_farfield_disabled='MonitorFarFieldsNearToModel "False"' in cmds,saved_verification=json.loads((folder/'Verification.json').read_text()))
    (b.ROOT/'02_Simulation_Results'/'Original_Native_Read_Check.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
