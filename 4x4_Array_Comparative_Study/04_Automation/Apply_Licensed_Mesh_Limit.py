from pathlib import Path
p=Path(__file__).with_name('Study_Sequence.py');s=p.read_text(encoding='utf-8')
a=s.index("    if best['s11_50ohm_dB']>-10:\n        q0=");z=s.index("    print('SELECTED'",a)
s=s[:a]+"""    if best['s11_50ohm_dB']>-10:
        ch=estimate_quarter_wave(nominal,first)
        q=run('Matched_Quarterwave_4x4',ch);tests.append(q)
        if q['s11_50ohm_dB']<best['s11_50ohm_dB']:
            best=q;change=ch
"""+s[z:]
a=s.index('    # Keep successful');z=s.index('    folder=P/detailed',a)
s=s[:a]+"""    # Finite licensed grids after the native 26/39 job was rejected at the 1M-cell limit.
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
"""+s[z:]
p.write_text(s,encoding='utf-8')

