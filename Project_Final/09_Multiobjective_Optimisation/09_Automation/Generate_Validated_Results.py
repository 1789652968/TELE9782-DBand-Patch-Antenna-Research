"""Publish the completed high-resolution comparisons directly from the saved selected projects."""
from Round2_Delivery import *
def main():
    selected=read(V/'Final_Selection.json');tested=read(V/'Verification_Results.json');rows=all_trials();old=legacy()
    cmp=old+[read(Path(p)/'round2.json')|{'name':role} for role,p in selected.items()]
    fr=[];aud=[]
    for p in dict.fromkeys(selected.values()):
        folder=Path(p);fr+=freq_rows(folder);aud.append(final_audit(folder)|{'name':folder.name})
    write(R/'Multiobjective_Comparison.csv',cmp);write(R/'Final_Frequency_Monitors.csv',fr);write(R/'Radiation_Pattern_Audit.csv',aud)
    figures(rows,cmp,selected,tested);beam_diagnosis(rows,old[-1])
    for q in cmp:print(q['name'],q['eta'],q['D'],q['G50'],q['G0'],q['theta'],q['bandwidth50'])
if __name__=='__main__':main()

