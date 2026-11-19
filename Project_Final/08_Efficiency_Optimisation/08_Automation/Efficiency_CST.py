"""Sequential CST jobs derived from the actual archived model, all writes inside study root."""
from Array_Run import b,ci
from pathlib import Path
import sys,shutil,json,csv,math,re,time
ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/'01_Baseline_Copy/01_CST_Project'
NATIVE=next(BASE.glob('*.cst')); GEOM=json.loads((BASE/'parameters.json').read_text())
D=ROOT/'02_Loss_Diagnostics';F=ROOT/'03_Feed_Optimisation';T=ROOT/'04_Substrate_Metal_Study';V=ROOT/'06_Final_Candidate';R=ROOT/'07_Results_and_Figures'
def dump(path,value):path.write_text(json.dumps(value,indent=2),encoding='utf-8')
def row_at(folder,term,optional=False):
    f=folder/('1D Results_Power_Excitation [1]_'+term+'.csv')
    if not f.exists() and optional:return 0.
    return float(next(r for r in csv.DictReader(f.open()) if abs(float(r['x'])-150)<.00002)['real'])
def result(folder):
    s=json.loads((folder/'summary.json').read_text());q=next(v for v in s['farfields'] if v['f_GHz']==150)
    p=json.loads((folder/'parameters.json').read_text());file=lambda name: list(csv.DictReader((folder/name).open()))
    raw=file('1D Results_S-Parameters_S1,1.csv');zref=float(file('1D Results_Reference Impedance_ZRef 1(1).csv')[0]['real']);curve=[]
    for pt in raw:
        g=complex(float(pt['real']),float(pt['imag']));z=zref*(1+g)/(1-g);g50=(z-50)/(z+50);curve.append((float(pt['x']),g50,z))
    k=min(range(len(curve)),key=lambda i:abs(curve[i][0]-150));_,g,z=curve[k]
    pa=row_at(folder,'Power Accepted');pr=row_at(folder,'Power Radiated');pm=row_at(folder,'Loss in Metals',bool(p.get('pec')));pd=row_at(folder,'Loss in Dielectrics',p['loss_tangent']==0);pp=row_at(folder,'Power Absorbed at all Ports');pi=row_at(folder,'Power Stimulated');po=row_at(folder,'Power Outgoing all Ports')
    eta=pr/pa; assert abs(eta-10**(q['rad_eff_dB']/10))<.002
    db=[20*math.log10(abs(i[1])) for i in curve];edges=[]
    for j in range(1,len(db)):
        if (db[j]<=-10)!=(db[j-1]<=-10):
            edges.append(curve[j-1][0]+(-10-db[j-1])*(curve[j][0]-curve[j-1][0])/(db[j]-db[j-1]))
    lo=max([x for x in edges if x<150] or [130]);hi=min([x for x in edges if x>150] or [170]);bw=hi-lo if db[k]<=-10 else 0
    return dict(name=folder.name,solver=s['solver']['state'],eta=100*eta,eta_farfield=100*10**(q['rad_eff_dB']/10),eta_total50=100*eta*(1-abs(g)**2),S11_50=db[k],D=q['Dmax_dBi'],G50=q['Dmax_dBi']+10*math.log10(eta*(1-abs(g)**2)),Rin=z.real,Xin=z.imag,Zref=zref,Pin=pi,Pout=po,Pacc=pa,Prad=pr,Pmetal=pm,Pdiel=pd,Pport=pp,residual_pct=100*(pa-pr-pm-pd-pp)/pa,bandwidth50=bw,low50=lo if bw else None,high50=hi if bw else None,fmin50=curve[min(range(len(db)),key=db.__getitem__)][0])
def clone(folder,p):
    dst=folder/(folder.name+'.cst')
    if not dst.exists():
        shutil.copyfile(NATIVE,dst)
        shutil.copytree(NATIVE.with_suffix('')/'Model',dst.with_suffix('')/'Model',dirs_exist_ok=True)
    return dst
def corner(m,p):
    # Remove the outer triangle of each right-angle bend. Fill two inner T corners.
    def triangular(name,points,subtract):
        code='With Extrude\n.Reset\n.Name "'+name+'"\n.Component "antenna"\n.Material "'+('Vacuum' if subtract else 'Gold')+'"\n.Mode "Pointlist"\n.Height "metal_thickness"\n.Origin "0","0","substrate_h"\n.Uvector "1","0","0"\n.Vvector "0","1","0"\n'
        for j,(x,y) in enumerate(points):code+=('.Point ' if j==0 else '.LineTo ')+f'"{x}","{y}"\n'
        code+='.Create\nEnd With\nSolid.'+('Subtract' if subtract else 'Add')+' "antenna:trunk","antenna:'+name+'"'
        m.add_to_history('Symmetric corner '+name,code)
    w=p['feed_width'];y=p['junction_y'];d=p['array_spacing']/2;t=p['transformer_width'];a=.58*w
    for i,sg in enumerate([-1,1]):
        def pts(arr):
            seq=[(sg*x,yy) for x,yy in arr]
            return seq if sg==1 else list(reversed(seq))
        if p.get('miter'):triangular('miter'+str(i),pts([(d+w/2-a,y-w/2),(d+w/2,y-w/2),(d+w/2,y-w/2+a)]),True)
        if p.get('fillet'):triangular('tee'+str(i),pts([(w/2,y-t/2-.30*w),(w/2+.30*w,y-t/2),(w/2,y-t/2)]),False)
def solve(de,stage,name,changes=None,details=False):
    folder=stage/name;folder.mkdir(exist_ok=True);cfg=GEOM|dict(mesh_near=20.,mesh_box=30.)|(changes or {})
    if (folder/'completed.json').exists():
        assert json.loads((folder/'parameters.json').read_text())==cfg
        return json.loads((folder/'completed.json').read_text())
    path=clone(folder,cfg);p=de.open_project(str(path))
    try:
        m=p.model3d
        for k,v in cfg.items():
            if k in GEOM:m.StoreParameter(k,str(v))
        m.full_history_rebuild()
        if 'mode_factor' in cfg:m.add_to_history('Port mode frequency sensitivity','Solver.SetModeFreqFactor '+chr(34)+str(cfg['mode_factor'])+chr(34))
        if cfg.get('pec'):m.add_to_history('Diagnostic only: all gold surfaces to PEC','Solid.ChangeMaterial "antenna:ground","PEC"\nSolid.ChangeMaterial "antenna:trunk","PEC"')
        if cfg.get('miter') or cfg.get('fillet'):corner(m,cfg)
        dump(folder/'parameters.json',cfg);p.save();print('START',name,flush=True)
        s,_=b.run(p);assert s['solver']['state']=='SUCCESS';v=result(folder)
        b.export_pattern(p,150,folder)
        p.save();dump(folder/'completed.json',v);print('DONE',name,round(v['eta'],3),round(v['S11_50'],2),round(v['G50'],2),flush=True)
        return v
    finally:p.close()
def main():
    print('NATIVE_BASELINE',result(BASE),flush=True);dump(R/'Baseline_Power_Recomputed.json',result(BASE))
    de=ci.DesignEnvironment.new();de.set_quiet_mode(True)
    try:
        for name,change in [('A_Gold_PI',{}),('B_PEC_PI',{'pec':1}),('C_Gold_NoTanD',{'loss_tangent':0}),('D_PEC_NoTanD',{'pec':1,'loss_tangent':0})]:
            solve(de,D,name,change)
    finally:de.close()
if __name__=='__main__':main()

