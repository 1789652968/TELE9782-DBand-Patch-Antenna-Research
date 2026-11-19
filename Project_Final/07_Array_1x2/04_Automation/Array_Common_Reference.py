"""Grade angular and power checks at the operating point, plus re-reference input power."""
from Array_Results_Extraction import *
def main():
    models=[('Original',ORIG,ORIG),('Enlarged ground',W/'GroundControl',W/'GroundControl'),('Final array',P,R)]
    shared=[];native=[]
    for label,folder,pat in models:
        m=metrics(folder,pat);f,g,z0,z,g50=scattering(folder);k=np.argmin(abs(f-150))
        mis=1-abs(g50[k])**2;et=m['rad_eff_pct']*mis
        ffdb,phase=sphere(pat);ref=m['reference_ohm']
        common=dict(design=label,frequency_GHz=150,reflection_50_dB=20*np.log10(abs(g50[k])),Gamma50_real=g50[k].real,Gamma50_imag=g50[k].imag,Zin_real_ohm=z[k].real,Zin_imag_ohm=z[k].imag,directivity_dBi=m['Dmax_dBi'],gain_accepted_dBi=m['Dmax_dBi']+10*np.log10(m['rad_eff_pct']/100),realized_gain_50_dBi=m['realized_50_dBi'],rad_eff_pct=m['rad_eff_pct'],total_eff_50_pct=et,mismatch_eff_50_pct=100*mis)
        shared.append(common)
        fp=next(v for v in read((ORIG/'numerical_audit.json') if folder==ORIG else ((P/'numerical_audit.json') if folder==P else (folder/'numerical_audit.json')))['farfield_checks'] if v['f_GHz']==150) if folder!=W/'GroundControl' else next(v for v in audit(folder)['farfield_checks'] if v['f_GHz']==150)
        native.append(dict(design=label,reference_ohm=ref,**fp,sphere_mean=m['sphere_mean']))
    write(C/'Common50_150GHz.csv',shared);write(C/'Three_Model_Power_150GHz.csv',native)
    f,g,zref,z,g50=scattering(P)
    with (R/'Final_50ohm.s1p').open('w',encoding='ascii') as out:
        out.write('! Final physical CST array, reference plane at input launch\n# GHz S RI R 50\n')
        for x,gg in zip(f,g50):out.write(f'{x:.9g} {gg.real:.12e} {gg.imag:.12e}\n')
    absdb=np.abs
    stim=native[-1]['Pstim_W'];v=native[-1]
    data=dict(Pincident_minus_Preflected_minus_Paccepted_W=stim-v['Poutgoing_W']-v['Paccepted_W'],radiation_efficiency_from_power_percent=100*v['Prad_W']/v['Paccepted_W'],total_efficiency_from_power_percent=100*v['Prad_W']/stim,normalized_gain_identity_dB=v['gain_identity_residual_dB'])
    (R/'Independent_Power_Check.json').write_text(json.dumps(data,indent=2))
if __name__=='__main__':main()
