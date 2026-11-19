"""Complex Ez at opposite radiating-edge probes; no independent-source decomposition is assumed."""
from Round2_Analysis import *
def edge(folder):
    path=folder/'Radiating_Edge_Efield_150.txt';a=np.loadtxt(path,skiprows=2);c=read(folder/'parameters.json');y0=c.get('shift_y',0)
    assert len(a)==20
    out=[]
    for label,sign in [('left',-1),('right',1)]:
        xpos=sign*c['array_spacing']/2;ok=abs(a[:,0]-xpos)<.49*c['patch_width'];ok &= abs(a[:,0]-xpos)>.14*c['patch_width']
        low=a[ok&(a[:,1]<y0)];high=a[ok&(a[:,1]>y0)]
        assert len(low)==len(high)==4
        neg=np.mean(low[:,7]+1j*low[:,8]);pos=np.mean(high[:,7]+1j*high[:,8]);ratio=pos/neg
        out.append(dict(model=folder.name,patch=label,points_per_edge=4,positive_y_abs_Ez=abs(pos),negative_y_abs_Ez=abs(neg),positive_over_negative_dB=20*np.log10(abs(ratio)),raw_positive_minus_negative_deg=np.angle(ratio,deg=True)))
    return out
def append(paths):
    folders=[DI/'PreviousArray',DI/'FirstOptimised']+[Path(p) for p in dict.fromkeys(paths)]
    rows=[]
    for folder in folders:
        if (folder/'Radiating_Edge_Efield_150.txt').exists():rows+=edge(folder)
    write(DI/'Opposite_Slot_Complex_Ez.csv',rows)
    from Round2_Delivery import table
    text=table(rows,['model','patch','positive_over_negative_dB','raw_positive_minus_negative_deg'],['Model','Patch','+Y / −Y |Ez| (dB)','Arg(Ez,+Y / Ez,−Y) (°)'])
    with (DOC/'Beam_Squint_Diagnosis.md').open('a',encoding='utf-8') as out:
        out.write('\n## Near-edge field asymmetry\n\n'+text+'\n\nFour points per edge at x offsets ±0.20W and ±0.33W, 4 μm inside the patch and halfway through the substrate, exclude the central inset. Values are the complex means of the local longitudinal electric field. This diagnostic compares the two radiating edges inside each patch. Its phase is the raw Ez phase, before applying an equivalent-slot normal convention. It does not isolate feed-line radiation, finite-ground radiation or their interference in the far field.\n')

