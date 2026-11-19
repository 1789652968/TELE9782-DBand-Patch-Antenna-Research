"""Loss-guided serial screening; print and retain every solved case including failed matching."""
from Efficiency_CST import *
def pattern(folder):
    a=[list(map(float,line.split())) for line in (folder/'Farfield_150_Sphere.txt').read_text().splitlines()[2:] if line.strip()]
    top=max(a,key=lambda x:x[2]);return top[0],top[1]
def valid(v,folder):
    return v['S11_50']<=-10 and v['D']>=6.5 and abs(v['residual_pct'])<=2 and pattern(folder)[0]<=20
def chosen(items):
    feasible=[i for i in items if valid(i[1],i[0])]
    if not feasible:return None
    return max(feasible,key=lambda i:(round(i[1]['eta'],1),i[1]['G50']))
def getp(d):return json.loads((d/'parameters.json').read_text())
def optimise():
    while not (D/'D_PEC_NoTanD/completed.json').exists():time.sleep(10)
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True);items=[]
    def run(stage,name,params):
        v=solve(de,stage,name,params);i=(stage/name,v);items.append(i);return i
    def tune(stage,i,hlabel):
        folder,v=i
        if valid(v,folder) and v['S11_50']<-13:return i
        p=getp(folder);shift=max(-.025,min(.025,p['patch_length']*(v['fmin50']/150-1)*1.12))
        if abs(shift)<.001:shift=.001
        c=p|dict(patch_length=round(p['patch_length']+shift,4))
        j=run(stage,hlabel+'_Length',c)
        if valid(j[1],j[0]):return j
        c['inset_length']=round(c['inset_length']*(.88 if j[1]['Rin']<50 else 1.10),4)
        return run(stage,hlabel+'_Inset',c)
    try:
        a=D/'A_Gold_PI';items.append((a,result(a)))
        run(F,'F1_ShortArms',{'junction_y':-.405,'array_spacing':1.12})
        run(F,'F2_WideTransformer',{'junction_y':-.405,'array_spacing':1.12,'transformer_width':.066,'transformer_length':.24})
        run(F,'F3_Miter',{'junction_y':-.405,'array_spacing':1.12,'transformer_width':.066,'transformer_length':.24,'miter':1})
        run(F,'F4_Tee',{'junction_y':-.405,'array_spacing':1.12,'transformer_width':.066,'transformer_length':.24,'miter':1,'fillet':1})
        feed=max(items[1:],key=lambda i:i[1]['eta']);tune(F,feed,'F5_Rematch')
        # Include the unchanged geometry when the reduced routing does not improve efficiency.
        best=chosen(items);assert best;feedp=getp(best[0]);dump(F/'selection.json',dict(case=best[0].name,metrics=best[1]))
        for h in [.03,.05,.06]:
            scale=h/.04
            c=feedp|dict(substrate_h=h,feed_width=round(feedp['feed_width']*scale,4),transformer_width=round(feedp['transformer_width']*scale,4),patch_length=round(feedp['patch_length']-.65*(h-.04),4))
            tag='H'+str(round(h*1000));i=run(T,tag,c);tune(T,i,tag)
        # Explore one extra thickness only when the prior feasible thick design improved.
        best=chosen(items);p=getp(best[0])
        if p['substrate_h']>=.05 and best[1]['eta']>=items[0][1]['eta']+2:
            h=.075;c=p|dict(substrate_h=h,feed_width=round(p['feed_width']*h/p['substrate_h'],4),transformer_width=round(p['transformer_width']*h/p['substrate_h'],4),patch_length=round(p['patch_length']-.65*(h-p['substrate_h']),4));i=run(T,'H75',c);tune(T,i,'H75')
        best=chosen(items);p=getp(best[0])
        for t in [.003,.005]:run(T,f'Au{round(t*1000)}um',p|dict(metal_thickness=t))
        best=chosen(items);name=best[0].name;p=getp(best[0])
        dump(T/'selection.json',dict(case=name,params=p,metrics=best[1]))
        i=run(V,'Fine',p|dict(mesh_near=36,mesh_box=54))
        if not valid(i[1],i[0]):i=tune(V,i,'FineRematched')
        if not valid(i[1],i[0]):raise RuntimeError('Final high-resolution case requires further physical retuning')
        src=i[0];p=getp(src)
        hold=run(V,'IndependentMesh',p|dict(mesh_near=38,mesh_box=57))
        dump(V/'selection.json',dict(screen=name,source=src.name,holdout=hold[0].name,source_results=i[1],holdout_results=hold[1]))
        run(T,'PortFrequency140',getp(best[0])|dict(mode_factor=.25))
    finally:de.close()
if __name__=='__main__':optimise()
