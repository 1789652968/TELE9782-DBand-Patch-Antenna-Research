from pathlib import Path
p=Path(__file__).with_name('Round2_Report.py')
s=p.read_text(encoding='utf-8-sig');key="    warnings=[s.strip() for s in log.splitlines()"
addition='''    boundary={}
    for axis in ['Xmin','Xmax','Ymin','Ymax','Zmin','Zmax']:
        vals=re.findall(r'\\.'+axis+r'\\s+"([^"]+)"',code)
        assert vals
        boundary[axis]=vals[-1]
    assert boundary=={k:('open' if k=='Ymin' else 'expanded open') for k in boundary}
    for spec in ['.ReferencePlaneDistance "0"','.PortOnBound "True"','.FrequencyForMinimumDistance "130"', '.MinimumDistancePerWavelengthNewMeshEngine "4"']:
        checks[spec]=spec in code
    assert np.max(abs(data[:,0]-f))<.00005
    mask=direction[:,2]>-35
    native_offset=10*np.log10(10**(ff['total_eff_dB']/10))
    angular_delta=float(np.max(abs((native[mask,2]-direction[mask,2])-native_offset)))
    assert angular_delta<.025,angular_delta
'''
if '    boundary={}' not in s:
    s=s.replace(key,addition+key).replace('out=dict(native_gain_theta=', 'out=dict(final_boundary=boundary,reference_plane_distance_mm=0,maximum_native_gain_identity_residual_dB=angular_delta,native_gain_theta=')
p.write_text(s,encoding='utf-8')

