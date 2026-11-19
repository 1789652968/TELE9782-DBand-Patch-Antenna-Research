from pathlib import Path
p=Path(__file__).with_name('Round2_Search.py');s=p.read_text(encoding='utf-8')
s=s.replace("def focused(de):",'''def nearby_dip(v):
    folder=Path(v['path'])
    raw=list(csv.DictReader((folder/'1D Results_S-Parameters_S1,1.csv').open()))
    vals=[]
    for row in raw:
        g=complex(float(row['real']),float(row['imag']))
        z=v['Zref']*(1+g)/(1-g);vals.append((float(row['x']),abs((z-50)/(z+50))))
    dips=[f for i,(f,a) in enumerate(vals) if 0<i<len(vals)-1 and 137<=f<=163 and a<vals[i-1][1] and a<=vals[i+1][1]]
    return min(dips,key=lambda f:abs(f-150)) if dips else v['fmin50']
def focused(de):''')
s=s.replace("ht['fmin50']/150","nearby_dip(ht)/150")
s=s.replace("(A,'HighWide',tune", """(H,'HighInsetMatch',tune|dict(inset_length=.126,transformer_length=.305,transformer_width=round(.96*hc['transformer_width'],4))),
          (H,'H095Matched',thick(.095)|dict(patch_length=.5195,inset_length=.143,transformer_length=.295)),
          (H,'H125Exploratory',thick(.125)|dict(patch_length=.498,inset_length=.13,transformer_length=.306,junction_y=-.43)),
          (A,'HighWide',tune""")
p.write_text(s,encoding='utf-8')

