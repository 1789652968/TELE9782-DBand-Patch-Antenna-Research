"""Finite study: one initial run, up to two basic matching attempts, mesh check, export."""
from Extract_Results import ROOT,RESULTS,observations,raw,read,write,write_json,publish
import math,sys,json,subprocess,time,os,shutil
from pathlib import Path
import numpy as np
CST=Path(os.getenv('CST_INSTALLPATH_2024', r'D:\TELE9782\CST Studio Suite 2024'))
PY=CST/'Opera/code/bin/python.exe'
A=ROOT/'04_Automation';P=ROOT/'01_CST_Project';V=RESULTS/'Verification'

def run(case,change,detail=False):
    f=P/case
    if not (f/'Export_Complete.json').is_file():
        extra=['--detail'] if detail else []
        if (f/'summary.json').is_file() and read(f/'summary.json')['solver']['state']=='SUCCESS':extra+=['--extract']
        args=[str(PY),'-u',str(A/'Run_4x4.py'),case,json.dumps(change)]+extra
        try:subprocess.run(args,cwd=A,check=True)
        except subprocess.CalledProcessError:
            if '--extract' not in extra and (f/'summary.json').is_file() and read(f/'summary.json')['solver']['state']=='SUCCESS':
                subprocess.run(args+['--extract'],cwd=A,check=True)
            else:raise
    q=observations(f)[0]
    print('GATE',case,q['s11_50ohm_dB'],q['radiation_efficiency_pct'],q['directivity_dBi'],q['mesh_cells'],flush=True)
    return q

def estimate_width(c,initial):
    w0=c['feed_width'];h=c['substrate_h'];eps=c['eps_r']
    def modal(w):
        u=w/h
        e=(eps+1)/2+(eps-1)/2*(1+12/u)**-.5
        z=60/e**.5*math.log(8/u+.25*u) if u<1 else 120*math.pi/(e**.5*(u+1.393+.667*math.log(u+1.444)))
        return e,z
    e0,z0=modal(w0);scale=initial['modal_reference_ohm']/z0;z0*=scale
    f,g=raw(P/'Initial_4x4','1D Results_S-Parameters_S1,1')
    band=abs(f-150)<=1.3;f=f[band];g=g[band];zin=initial['modal_reference_ohm']*(1+g)/(1-g)
    def line(z,r,l,e):
        t=np.tan(2*np.pi*f*e**.5*l/299.792458)
        return r*(z+1j*r*t)/(r+1j*z*t)
    best=(math.inf,None)
    for start in np.arange(.17,.43,.02):
        for length in np.arange(.14,.465,.02):
            if start+length>.635:continue
            zl=line(zin,z0,-start-length,e0)
            for w in np.arange(.045,.25,.005):
                em,zm=modal(w);pred=line(line(zl,zm*scale,length,em),z0,start,e0)
                reflection=abs((pred-50)/(pred+50))
                score=.65*float(reflection[len(f)//2])+.23*float(np.mean(reflection))+.12*float(max(reflection))
                if score<best[0]:
                    best=(score,dict(match_start=round(float(start),4),match_length=round(float(length),4),match_width=round(float(w),4)))
    write_json(V/'Single_Section_Matching_Proposal.json',dict(source='Measured Initial_4x4 input impedance, lossless uniform-line surrogate for the local stepped section',mean_reflection_score=best[0],trial=best[1]))
    return best[1]

def estimate_open_stub(c,initial):
    """Use the full-wave input Z to design a conventional single shunt-stub match."""
    z0=initial['modal_reference_ohm'];h=c['substrate_h'];eps=c['eps_r'];w0=c['feed_width']
    def modal(w):
        u=w/h;eff=(eps+1)/2+(eps-1)/2*(1+12/u)**-.5
        z=60/eff**.5*math.log(8/u+.25*u) if u<1 else 120*math.pi/(eff**.5*(u+1.393+.667*math.log(u+1.444)))
        return eff,z
    e0,z_est=modal(w0);scale=z0/z_est
    f,g=raw(P/'Initial_4x4','1D Results_S-Parameters_S1,1');sel=abs(f-150)<=1.0
    f=f[sel];z_in=z0*(1+g[sel])/(1-g[sel]);m=len(f)//2
    def transform(z,z0,t):return z0*(z+1j*z0*t)/(z0+1j*z*t)
    best=(math.inf,None)
    for w in [.065,.07,.075,.08,.085]:
        eff,zstub=modal(w);zstub*=scale
        fringe=.412*h*((eff+.3)*(w/h+.264))/((eff-.258)*(w/h+.8))
        for offset in np.arange(.56,.605,.002):
            x=c['board_x_min']-c['launch_length']+offset
            if x < c['board_x_min']+w/2+.015 or x+w/2+.04>c['first_split_x']-c['transformer_width']/2:continue
            t=np.tan(2*np.pi*f*np.sqrt(e0)*offset/299.792458)
            l=transform(z_in,z0,-t)
            for length in np.arange(.13,.285,.003):
                stub=1j*np.tan(2*np.pi*f*np.sqrt(eff)*(length+fringe)/299.792458)/zstub
                result=transform(1/(1/l+stub),z0,t)
                gamma=abs((result-50)/(result+50))
                score=.7*gamma[m]+.3*gamma.mean()
                if score<best[0]:best=(score,dict(stub_start=round(float(offset),4),stub_length=round(float(length),4),stub_width=w))
    assert best[1] is not None
    write_json(V/'Open_Stub_Matching_Proposal.json',dict(approximate_reflection_score=float(best[0]),
      proposal=best[1],source='150 GHz native input impedance and approximate uniform-line transfer, including microstrip open-end correction'))
    return best[1]
def estimate_quarter_wave(c,initial):
    """Match near the measured low-resistance point, with a separate straight-line landing."""
    z0=initial['modal_reference_ohm'];h=c['substrate_h'];eps=c['eps_r']
    def modal(w):
        u=w/h;eff=(eps+1)/2+(eps-1)/2*(1+12/u)**-.5
        z=120*math.pi/(eff**.5*(u+1.393+.667*math.log(u+1.444)))
        return eff,z
    e0,z_est=modal(c['feed_width']);scale=z0/z_est
    f,g=raw(P/'Initial_4x4','1D Results_S-Parameters_S1,1');sel=abs(f-150)<=1.1
    f=f[sel];z_in=z0*(1+g[sel])/(1-g[sel]);m=len(f)//2
    def line(z,r,l,e):
        t=np.tan(2*np.pi*f*l*np.sqrt(e)/299.792458);return r*(z+1j*r*t)/(r+1j*z*t)
    best=(math.inf,None,None)
    for l in np.arange(.47,.651,.006):
        z= line(z_in,z0,l,e0)
        if abs(z[m].imag)>10:continue
        for w in np.arange(.37,.86,.02):
            eff,r=modal(w)
            for lq in np.arange(.23,.334,.008):
                zprod=line(line(z,r*scale,lq,eff),z0,.5,e0);g50=abs((zprod-50)/(zprod+50))
                score=.66*float(g50[m])+.27*float(g50.mean())+.07*float(max(g50))
                if score<best[0]:
                    best=(score,dict(extension_l50_mm=round(float(l),5),extension_lq_mm=round(float(lq),5),extension_match_width_mm=round(float(w),5)),
                        dict(load_r=float(z[m].real),load_x=float(z[m].imag),transmission_line_Z_ohm=r*scale,predicted_s11_50ohm_dB=20*math.log10(g50[m])))
    assert best[1] is not None
    write_json(V/'Quarterwave_Transformer_Proposal.json',dict(settings=best[1],approximation=best[2],source='Native initial input impedance; uniform-line model calibrated to native port ref'))
    return best[1]
def stable(a,b):
    return (abs(a['radiation_efficiency_pct']-b['radiation_efficiency_pct'])<=1.5
            and abs(a['directivity_dBi']-b['directivity_dBi'])<=.30
            and abs(a['plus_z_realized_gain_50ohm_dBi']-b['plus_z_realized_gain_50ohm_dBi'])<=.50
            and abs(a['bandwidth_10dB_GHz']-b['bandwidth_10dB_GHz'])<=2
            and abs(a['beam_theta_deg']-b['beam_theta_deg'])<=4
            and ((a['s11_50ohm_dB']<=-10)==(b['s11_50ohm_dB']<=-10)))

def main():
    initial=P/'Initial_4x4'
    while not (initial/'Export_Complete.json').is_file():
        if (initial/'Run_Failure.txt').is_file():
            if (initial/'summary.json').is_file() and read(initial/'summary.json')['solver']['state']=='SUCCESS':
                run('Initial_4x4',{})
                break
            raise RuntimeError('Initial CST solve failed. See Initial_4x4/Run_Failure.txt')
        time.sleep(15)
    if '--wait-refined' in sys.argv:
        existing=P/'Refined_4x4'
        while not (existing/'Export_Complete.json').is_file():
            if (existing/'Run_Failure.txt').is_file():break
            time.sleep(15)
    if '--wait-existing' in sys.argv:
        existing=P/'Matched_Input_4x4'
        while not (existing/'Export_Complete.json').is_file():
            if (existing/'Run_Failure.txt').is_file():break
            time.sleep(15)
    first=run('Initial_4x4',{})
    tests=[first];nominal=read(initial/'parameters.json')
    best=first;change={}
    if first['s11_50ohm_dB']>-10:
        ch=estimate_width(nominal,first)
        q=run('Matched_Input_4x4',ch);tests.append(q)
        if q['s11_50ohm_dB']<best['s11_50ohm_dB']:best=q;change=ch
        if best['s11_50ohm_dB']>-10:
            ch=estimate_open_stub(nominal,first)
            q=run('Matched_Stub_4x4',ch);tests.append(q)
            if q['s11_50ohm_dB']<best['s11_50ohm_dB']:best=q;change=ch
    if best['s11_50ohm_dB']>-10:
        ch=estimate_quarter_wave(nominal,first)
        q=run('Matched_Quarterwave_4x4',ch);tests.append(q)
        if q['s11_50ohm_dB']<best['s11_50ohm_dB']:
            best=q;change=ch
    print('SELECTED',best['design'],change,flush=True)
    write_json(V/'Selection.json',dict(selected_coarse=best['design'],matching_changes=change,screen_trials=tests))
    # Finite licensed grids after the native 26/39 job was rejected at the 1M-cell limit.
    failures=[]
    def capped(options):
        for near,box in options:
            case=f'Licensed_{near}_{box}_4x4'
            try: return case,run(case,change|dict(mesh_near=near,mesh_box=box),True)
            except subprocess.CalledProcessError:
                evidence=P/case/'failure_messages.json'
                if not evidence.exists() or '1000000 mesh cells' not in evidence.read_text(encoding='utf-8',errors='replace'):
                    raise
                failures.append(case)
        raise RuntimeError('No finer mesh could run within the CST license limit')
    detailed,fine=capped([(22,32),(21,31)])
    meshes=[best,fine]
    if not stable(best,fine) and fine['steps_per_wave_near']<23:
        try:
            d2,dense=capped([(23,33),(23,31)])
            if dense['mesh_cells']>fine['mesh_cells']:
                detailed=d2;meshes.append(dense)
        except RuntimeError as exc:
            if 'No finer mesh' not in str(exc):raise
    write_json(V/'License_Constraint.json',dict(maximum_mesh_cells=1000000,rejected_setup='26 steps per wave, 39 per box, original Refined_4x4',
      original_native_error='This software is licensed for up to 1000000 mesh cells only.',subsequent_rejected_jobs=failures,
      final_steps_per_wave=meshes[-1]['steps_per_wave_near'],final_steps_per_box=meshes[-1]['steps_per_box_near']))
    folder=P/detailed
    assert meshes[-1]['solver_state']=='SUCCESS' and abs(meshes[-1]['directivity_sphere_mean']-1)<.04 and abs(meshes[-1]['balance_residual_pct_accepted'])<3
    write(V/'Mesh_Sensitivity.csv',meshes)
    write(V/'Matching_Trials.csv',tests)
    write_json(V/'Mesh_Selection.json',dict(meshes=meshes,comparable_mesh_pair=stable(meshes[-2],meshes[-1]),detailed_source=detailed))
    # Rename on a copy, retaining the native same-named companion and all numeric exports.
    final=P/'Final_4x4'
    if not final.exists():
        staging=P/'Final_Stage'
        if staging.exists():raise RuntimeError('Inspect incomplete Final_Stage before retry')
        shutil.copytree(folder,staging)
        (staging/(detailed+'.cst')).rename(staging/'Final_4x4.cst')
        (staging/detailed).rename(staging/'Final_4x4');staging.rename(final)
    subprocess.run([str(PY),'-u',str(A/'Verify_Native.py'),'Final_4x4'],cwd=A,check=True)
    publish(final)
    print('COMPLETE STUDY',flush=True)
if __name__=='__main__':main()

