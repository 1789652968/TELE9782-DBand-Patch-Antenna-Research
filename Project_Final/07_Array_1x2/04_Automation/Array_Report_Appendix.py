"""Integrate the finished reference, frequency and selection checks into the written report."""
from Array_Report import *
def finalize():
    path=DOC/'Final_Report_Results.md';report=path.read_text(encoding='utf-8')
    common=numtable(C/'Common50_150GHz.csv',['design','reflection_50_dB','directivity_dBi','realized_gain_50_dBi','rad_eff_pct','total_eff_50_pct'],['Design','S11 dB','D dBi','Greal dBi','ηrad %','ηtotal %'])
    freq=numtable(R/'Final_Array_Performance.csv',['f_GHz','S11_dB','Dmax_dBi','realized_gain_dBi','rad_eff_pct','total_eff_pct'],['GHz','S11 dB','D dBi','Greal dBi','ηrad %','ηtotal %'])
    v=read(R/'Reference_Comparison.json');eng=read(W/'engineering_selection.json');ret=metrics(W/'Spacing120_Retuned');old=metrics(W/'Spacing120')
    a=read(C/'Comparison_Metrics.json')['array'];opts=rows(R/'Optimisation_History.csv')
    selected=eng['selected_mesh'];confirm=read(R/'Verification.json')
    summary=f"""### Resonance retuning and the production choice

The 1.20 mm screening case gave {old['Dmax_dBi']:.3f} dBi and {old['S11_dB']:.2f} dB S11 at 150 GHz. Increasing its patch length to 0.513 mm produced {ret['Dmax_dBi']:.3f} dBi, {ret['realized_gain_dBi']:.3f} dBi realized gain and {ret['S11_dB']:.2f} dB S11 on the same coarse grid. The finer-grid comparison selected **{selected}** as the physical production source. The Final50 production source retained its geometry and resolution. The jump from 218,776 to 474,240 cells changed peak directivity by 0.233 dB and the minimum-S11 frequency by 1.56 GHz. An independently solved 38/57 holdout grid checks the stability of the 36/54 production mesh. Mesh_Convergence.csv contains every grid on this geometry, including the earlier nonmonotonic shift. Independently re-referencing the freshly solved broadband trace to 50 Ω recovers the CST-native 50 Ω Touchstone export with maximum complex reflection error {v['broadband_max_complex_difference']:.5g}.

### Common 50 Ω reference, 150 GHz

{common}

### Final array monitor samples

{freq}

These are maxima over angle at each stated monitor frequency. The 150 GHz fixed comparison uses independently calculated angular cuts and broadside data. The broadband S11 trace has {confirm['sample_count']} samples."""
    report=report.replace('## Comparison figures',summary+'\n\n## Comparison figures')
    report=report.replace('![Top-surface current at 150 GHz]', '![Controlled spacing current comparison](../03_Comparison/Spacing_Current_Comparison.png)\n\n![Top-surface current at 150 GHz]')
    start=report.find('# Single versus array\n');end=report.find('## Fixed-frequency comparison',start)
    if start>=0 and end>start:report=report[:start]+report[end:]
    for title in ['Array design theory','Corporate-feed calculations','CST implementation','Numerical validation']:report=report.replace('\n# '+title+'\n','\n## '+title+'\n')
    path.write_text(report,encoding='utf-8')
    analysis=DOC/'Single_vs_Array_Analysis.md';analysis.write_text(analysis.read_text(encoding='utf-8')+'\n'+summary+'\n',encoding='utf-8')
if __name__=='__main__':finalize()


