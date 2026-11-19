from pathlib import Path
d=Path(__file__).resolve().parent
def adjust(name,pairs):
    f=d/name;s=f.read_text(encoding='utf-8-sig')
    for a,b in pairs:
        if a not in s:raise ValueError(a)
        s=s.replace(a,b)
    f.write_text(s,encoding='utf-8')
adjust('Array_Delivery.py',[
("comparison['broadband_max_complex_difference']=float(max(abs(calc-g)))", """comparison['native_vs_math50_max_complex_difference']=float(max(abs(calc-g)))
    comparison['native_modal_vs_production_max_complex_difference']=float(max(abs(scattering(W/mesh)[1]-g)))
    touch=next(R.glob('CST_50ohm*.s1p'))
    data=np.loadtxt([line for line in touch.read_text(errors='replace').splitlines() if line.strip() and line.lstrip()[0] not in '!#'])
    factor=data[-1,0]/f[-1];assert np.allclose(data[:,0]/factor,f,atol=.0001)
    exported=data[:,1]+1j*data[:,2];comparison['broadband_max_complex_difference']=float(max(abs(calc-exported)))
    comparison['CST_touchstone_header']=next(line for line in touch.read_text().splitlines() if line.strip().startswith('#'))
    comparison['CST_touchstone_s11_150_dB']=20*np.log10(abs(exported[np.argmin(abs(f-150))]))
    comparison['explanation']='Native S1,1 retained the solved modal reference. The CST Touchstone exporter explicitly renormalized the saved result to 50 ohms.'"""),
("abs(fixed['reference_ohm']-50)<1e-8 and comparison['broadband_max_complex_difference']<.005","'50' in comparison['CST_touchstone_header'] and comparison['broadband_max_complex_difference']<.0001"),
("The delivered project has an explicit 50 Ω scattering reference.","The model history requests 50 Ω. The saved S1,1 trace uses the solved port reference. For the exact 50 Ω trace use CST_50ohm.s1p exported by CST with Renormalize enabled."),
("Final50 was solved with explicit 50 Ω normalization.","Final50 was solved with the explicit 50 Ω history setting. The saved modal trace was independently renormalized by CST Touchstone export."),
("To use the exact 50 Ω production setup open the final project.","Open the final project for the production model. Use the CST Touchstone export for the exact 50 Ω curve."),
("Final_50ohm.s1p Independent_Power_Check.json","Final_50ohm.s1p Independent_Power_Check.json"),
("& $cst Array_Line_Mode.py","& $cst Array_Line_Mode.py\n& $cst Array_Touchstone.py")
])
adjust('Array_Report.py',[
("The final solver explicitly uses {a['reference_ohm']:.4f} Ω for its S-parameter reference.","The delivered native S1,1 trace has a solved reference of {a['reference_ohm']:.4f} Ω."),
("Production uses AutoNormImpedance=True and NormingImpedance=50.","The production history explicitly requests AutoNormImpedance=True and NormingImpedance=50. Reading the saved project nevertheless shows an unchanged modal-reference S1,1. The independently verified CST Touchstone export is the authoritative fixed-50-Ω trace."),
])
adjust('Array_Report_Appendix.py',[
("The exact-50-Ω source Final50 retained its geometry and resolution.","The Final50 production source retained its geometry and resolution."),
("recovers the explicit-reference run with maximum complex reflection error","recovers the CST-native 50 Ω Touchstone export with maximum complex reflection error")])

