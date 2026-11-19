"""Stage B adapts to solved coarse data; only one CST environment computes at a time."""
from Round2_Core import *
from Round2_Geometry import install
install()
def completed():
    return [json.loads(p.read_text()) for stage in (F,H,Y,A) for p in stage.glob('*/round2.json')]
def good(v):
    return v['solver']=='SUCCESS' and v['D']>=6.5 and v['S11_50']<=-10 and abs(v['residual_pct'])<=2 and abs(v['sphere_mean']-1)<.02
def balanced(v):
    # Attainment gaps saturate once a soft target is met. Weights and scales are fixed for every run.
    axes=[('eta',90,6,3),('eta_total50',88,7,1),('G0',8,.6,2),('G50',8.5,.6,1),('D',9,1,.5),('bandwidth50',13.5,4,1)]
    return sum(w*max(0,(goal-v[key])/s) for key,goal,s,w in axes)+2.5*max(0,(v['theta']-5)/12)+.6*max(0,(v['S11_50']+17)/7)
def roles(rows):
    g=[v for v in rows if good(v)]
    if not g:raise ValueError('No feasible geometry')
    pool=[v for v in g if v['eta']>=81] or g
    return {'Highest_Efficiency':max(g,key=lambda v:(v['eta'],-balanced(v))),
      'Best_Balanced':min(g,key=lambda v:(balanced(v),-v['G0'],-v['eta'])),
      'Best_Broadside':min(pool,key=lambda v:(v['theta'],-v['G0'],-v['eta']))}
def config(v):return read_params(Path(v['path']))
def nearby_dip(v):
    folder=Path(v['path'])
    raw=list(csv.DictReader((folder/'1D Results_S-Parameters_S1,1.csv').open()))
    vals=[]
    for row in raw:
        g=complex(float(row['real']),float(row['imag']))
        z=v['Zref']*(1+g)/(1-g);vals.append((float(row['x']),abs((z-50)/(z+50))))
    dips=[f for i,(f,a) in enumerate(vals) if 0<i<len(vals)-1 and 137<=f<=163 and a<vals[i-1][1] and a<=vals[i+1][1]]
    return min(dips,key=lambda f:abs(f-150)) if dips else v['fmin50']
def focused(de):
    coarse=completed();by={v['name']:v for v in coarse};control=by['Control20']
    heights=[v for v in coarse if v['name'] in ['Control20','H060','H070','H085','H095','H110']]
    eligible=[v for v in heights if v['S11_50']< -7]
    ht=max(eligible,key=lambda v:v['eta']);hc=config(ht)
    # Apply bounded resonant-length correction to best thickness. This remains a screened design hypothesis.
    shift=max(-.025,min(.025,hc['patch_length']*(nearby_dip(ht)/150-1)*.7))
    tune=hc|dict(patch_length=round(hc['patch_length']+shift,4))
    ground=[by[n] for n in ['Control20','RearShort','RearLong','WideGround']]
    go=min(ground,key=lambda v:(v['theta'],-v['G0']));edge={k:config(go)[k] for k in ('ground_width','rear_delta') if k in config(go)}
    bestd=max([by[n] for n in ['Control20','Spacing100','Spacing125']],key=lambda v:v['G0'])
    spacing=config(bestd)['array_spacing']
    jobs=[(H,'ThicknessRetune',tune|{'inset_length':.15}),
          (H,'HighInsetMatch',tune|dict(inset_length=.126,transformer_length=.305,transformer_width=round(.96*hc['transformer_width'],4))),
          (H,'H095Matched',thick(.095)|dict(patch_length=.5195,inset_length=.143,transformer_length=.295)),
          (H,'H125Exploratory',thick(.125)|dict(patch_length=.498,inset_length=.13,transformer_length=.306,junction_y=-.43)),
          (A,'HighWide',tune|dict(patch_width=.78,inset_length=.15,array_spacing=spacing)|edge),
          (Y,'FeedShiftMinus',dict(shift_y=-.19)),(Y,'FeedShiftPlus',dict(shift_y=.24)),
          (Y,'NearRearEdge',dict(rear_delta=-.42)),(Y,'IntermediateRearEdge',dict(rear_delta=-.23)),
          (Y,'WideApertureBroadside',tune|dict(rear_delta=-.30,ground_width=3.05,patch_width=.82,array_spacing=1.22,inset_length=.15)),
          (Y,'MovedWideAperture',tune|dict(shift_y=-.16,rear_delta=-.46,junction_y=-.355,ground_width=3.05,patch_width=.82,array_spacing=1.22,inset_length=.15)),
          (Y,'ShortFeedWide',tune|dict(junction_y=-.35,shift_y=-.16,patch_width=.76,array_spacing=spacing,inset_length=.15)),
          (A,'RearCoupledShort',dict(strip=.36,strip_gap=.055,strip_w=.64,rear_delta=.26)),
          (A,'RearCoupledResonant',dict(strip=.50,strip_gap=.075,strip_w=.66,rear_delta=.26))]
    for st,name,c in jobs:
        if name in ('ShortFeedWide','MovedWideAperture'):
            c['junction_y']=round(min(c['junction_y'],-c['patch_length']/2-c['feed_width']/2-.02),4)
            c['shift_y']=round(max(c['shift_y'],-.747-c['junction_y']+c['feed_width']/2),4)
        run(de,st,name,c)
    r=roles(completed());beam=r['Best_Broadside'];balanced_c=r['Best_Balanced'];efficient=r['Highest_Efficiency']
    boost=config(efficient);bc=config(beam)
    for label in ('strip','strip_gap','strip_w','rear_delta','shift_y','ground_width','array_spacing'):
        if label in bc:boost[label]=bc[label]
    # Ensure translated bends are fully supported over the substrate.
    if boost.get('shift_y',0)+boost['junction_y']-boost['feed_width']/2<-.75:boost['shift_y']=round(-.747-boost['junction_y']+boost['feed_width']/2,4)
    min_rear=boost.get('shift_y',0)+boost['patch_length']/2-boost['ground_length']/2+.015
    if boost.get('rear_delta',0)<min_rear:boost['rear_delta']=round(min_rear,4)
    if boost.get('strip') and boost.get('shift_y',0)+boost['patch_length']/2+boost.get('strip_gap',.08)+boost['strip']>=boost['ground_length']/2+boost.get('rear_delta',0):
        boost.pop('strip',None)
    run(de,A,'CombinedObjectives',boost|dict(inset_length=round(max(.12,min(.19,boost['inset_length']-.012)),4)))
    c=config(balanced_c);delta=.017 if balanced_c['fmin50']>150 else -.017
    run(de,A,'BalanceRematch',c|dict(patch_length=round(c['patch_length']+delta*.55,4),transformer_length=round(c['transformer_length']*.94,4)))
    (A/'focused_finished.json').write_text(json.dumps({k:v['name'] for k,v in roles(completed()).items()},indent=2))
def final_jobs(de):
    coarse=completed();pre=roles(coarse);chosen={v['name']:v for v in pre.values()}
    dump(V/'Screen_Selection.json',{k:v['name'] for k,v in pre.items()})
    def validate(n,v):
        c=config(v);stage=V/n;stage.mkdir(exist_ok=True)
        prod=run(de,stage,n+'_Production',c|dict(mesh_near=36,mesh_box=54),'production')
        den=run(de,stage,n+'_Dense',c|dict(mesh_near=38,mesh_box=57),'dense')
        fresh=run(de,stage,n+'_Delivery',config(prod),'fresh',Path(prod['path']))
        return dict(trial=n,screen=v,production=prod,dense=den,fresh=fresh,
          accepted=all(good(k) for k in (prod,den,fresh)),
          eta_range=max(k['eta'] for k in (prod,den,fresh))-min(k['eta'] for k in (prod,den,fresh)),
          beam_range=max(k['theta'] for k in (prod,den,fresh))-min(k['theta'] for k in (prod,den,fresh)))
    tested={}
    for n,v in chosen.items():
        tested[n]=validate(n,v);dump(V/'Verification_Results.json',tested)
    def stable(t):return t['accepted'] and t['eta_range']<=1.2 and t['beam_range']<=4
    viable=[t['fresh'] for t in tested.values() if stable(t)]
    # Replace failed nominations individually, so a missing high-efficiency role is not masked by a passing broadside model.
    for role,initial in pre.items():
        if stable(tested[initial['name']]) or len(tested)>=len(chosen)+2:continue
        remaining=[v for v in coarse if good(v) and v['name'] not in tested and v['name']!='Control20']
        if not remaining:continue
        alt=roles(remaining)[role];tested[alt['name']]=validate(alt['name'],alt);dump(V/'Verification_Results.json',tested)
    viable=[t['fresh'] for t in tested.values() if stable(t)]
    if not viable:
        others=[v for v in coarse if good(v) and v['name'] not in chosen and v['name']!='Control20']
        if others:
            v=min(others,key=balanced);tested[v['name']]=validate(v['name'],v);dump(V/'Verification_Results.json',tested)
        viable=[t['fresh'] for t in tested.values() if stable(t)]
    if not viable:
        dump(V/'Final_Selection.json',{'fallback':str(BASE),'reason':'No independently stable new finalist'});return None
    selected=roles(viable);dump(V/'Final_Selection.json',{k:v['path'] for k,v in selected.items()});return selected['Best_Balanced']
def tolerance(de,winner):
    if winner is None:return
    stage=A/'Manufacturing_Sensitivity';stage.mkdir(exist_ok=True);base=config(winner)|dict(mesh_near=20,mesh_box=30)
    plan=[('Nominal',{})]
    for k,step in [('substrate_h',.003),('patch_length',.005),('patch_width',.005),('feed_width',.005),('metal_thickness',.0003),('eps_r',.07),('loss_tangent',.0004)]:
        for sign,suffix in [(-1,'Low'),(1,'High')]:plan.append((k+'_'+suffix,{k:round(base[k]+step*sign,6)}))
    for n,c in plan:run(de,stage,n,base|c,'sensitivity')
def main():
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        if not (A/'focused_finished.json').exists():focused(de)
        winner=final_jobs(de)
        tolerance(de,winner)
    finally:de.close()
    dump(R/'Search_Complete.json',{'verified':(V/'Final_Selection.json').exists(),'finished':time.time()})
if __name__=='__main__':main()

