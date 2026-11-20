"""Single-layer 150 GHz side-fed corporate array. All coordinates are in mm."""
from pathlib import Path
import json, math, os, sys
ROOT=Path(__file__).resolve().parents[1]
path_from_project='08_Efficiency_Optimisation/06_Final_Candidate/TELE9782_DBand_Efficiency_Final'
BASE=Path(os.environ['TELE9782_BASELINE_DIR']) if 'TELE9782_BASELINE_DIR' in os.environ else ROOT.parent/path_from_project
if not (BASE/'parameters.json').exists():BASE=ROOT.parent/'Project_Final'/path_from_project
REUSE=Path(__file__).resolve().parent/'CST_Utilities'
if not REUSE.exists():REUSE=ROOT.parent/'09_Multiobjective_Optimisation/09_Automation'
sys.path.insert(0,str(REUSE))
from Array_Run import b,ci

def parameters(changes):
    orig=json.loads((BASE/'parameters.json').read_text())
    keys=('patch_width','patch_length','substrate_h','metal_thickness','eps_r','loss_tangent','feed_width',
          'transformer_width','transformer_length','inset_length','inset_gap','port_halfwidth','launch_length')
    return {key:orig[key] for key in keys}|dict(pitch_x=1.12,pitch_y=1.25,stage3_separation=.235,
        inlet_rail_separation=.225,stage4_offset=.405,row_split_x=-2.24,first_split_x=-2.90,
        board_x_min=-3.12,board_x_max=2.40,mesh_near=20,mesh_box=30)|changes

def layout(c):
    w=c['feed_width']; q=c['transformer_width']; tq=c['transformer_length']
    l=c['patch_length']; pw=c['patch_width']; i=c['inset_length']; ig=c['inset_gap']
    dx=c['pitch_x']; dy=c['pitch_y']; x1=c['first_split_x'];x2=c['row_split_x']
    s4=c['stage4_offset'];s3=s4+c['stage3_separation'];s0=s3+c['inlet_rail_separation']
    xmin=c['board_x_min']; xmax=c['board_x_max']; oldport=xmin-c['launch_length']
    extra=c.get('extension_l50_mm',0)+c.get('extension_lq_mm',0)+(.5 if 'extension_match_width_mm' in c else 0)
    port=oldport-extra
    ymin=-1.5*dy-s0-.30; ymax=1.5*dy+l/2+.36
    assert dy-l/2-s0-w/2>.02,'Rail near preceding patch'
    assert x2+w/2 < -1.5*dx-pw/2-.045,'Side splitter clear of patch'
    assert s4-l/2-w/2>.02,'Terminal bar clear of patch edge'
    assert min(dy/2,dx/2)>tq and pw>w+2*ig
    assert min(c['stage3_separation'],c['inlet_rail_separation'])>w+.03
    metal=[];patches=[];legs=[];segments={}
    def rect(label,xr,yr,kind):
        assert xr[1]>xr[0] and yr[1]>yr[0],label
        metal.append(dict(name=label,x=xr,y=yr,kind=kind))
    def line(label,a,bb,width=w,prolong=0):
        # Continue the broad strip beyond the turn by half its width.
        ax,ay=a;bx,by=bb
        assert (ay==by)!=(ax==bx),(label,a,bb)
        if ay==by:
            start,end=sorted((ax,bx));start-=prolong if bx<ax else 0;end+=prolong if bx>ax else 0
            rect(label,(start,end),(ay-width/2,ay+width/2),'feed')
        else:
            start,end=sorted((ay,by));start-=prolong if by<ay else 0;end+=prolong if by>ay else 0
            rect(label,(ax-width/2,ax+width/2),(start,end),'feed')
        legs.append(math.hypot(bx-ax,by-ay));segments[label]=(a,bb)
    def split(label,a,axis,reach,sign):
        ix,iy=(sign,0) if axis=='x' else (0,sign)
        end=(a[0]+ix*reach,a[1]+iy*reach)
        z=(a[0]+ix*tq,a[1]+iy*tq)
        line(label+'_transformer',a,z,q)
        line(label+'_arm',z,end,w,w/2)
        return end
    annex=None
    if 'extension_match_width_mm' in c:
        xq=port+.5;x50=xq+c['extension_lq_mm'];ww=c['extension_match_width_mm']
        line('trunk',(port,-s0),(xq,-s0),w)
        line('wideQuarterWave',(xq,-s0),(x50,-s0),ww)
        line('return_to_original_plane',(x50,-s0),(oldport,-s0),w)
        line('core_input',(oldport,-s0),(x1,-s0),w,w/2)
        annex=dict(x=[xq-.14,x50+.14],y=[-s0-ww/2-.19,-s0+ww/2+.19])
        assert annex['x'][0]>port and annex['x'][1]<oldport
    elif 'stub_start' in c:
        x=port+c['stub_start'];sw=c['stub_width'];sl=c['stub_length']
        assert xmin+sw/2+.015<=x and x+sw/2+.04<=x1-q/2
        line('trunk',(port,-s0),(x,-s0),w)
        line('open_matching_stub',(x,-s0),(x,-s0+sl),sw)
        line('input_to_divider',(x,-s0),(x1,-s0),w,w/2)
    elif 'match_width' in c:
        a=port+c['match_start'];b=a+c['match_length']
        assert port+.16<=a and b<=x1-.08
        assert .045<=c['match_width']<=.25
        line('trunk',(port,-s0),(a,-s0),w)
        line('input_transformer',(a,-s0),(b,-s0),c['match_width'])
        line('input_to_divider',(b,-s0),(x1,-s0),w,w/2)
    else:
        line('trunk',(port,-s0),(x1,-s0),w,w/2)
    for t,sg in enumerate((-1,1)):
        first=split('level1_'+str(t),(x1,-s0),'y',dy,sg)
        node=(x2,first[1]);line('group_run_'+str(t),first,node,w,w/2)
        for j,direction in enumerate((-1,1)):
            row=2*t+j; origin=split('level2_'+str(row),node,'y',dy/2,direction)
            yc=(-1.5+row)*dy;rail=yc-s0
            assert abs(origin[1]-rail)<1e-9
            root=(0, yc-s3);line('row_rail_'+str(row),origin,(0,origin[1]),w,w/2)
            line('row_entry_'+str(row),(0,origin[1]),root,w,w/2)
            for k,sgx in enumerate((-1,1)):
                left_or_right=split(f'level3_{row}_{k}',root,'x',dx,sgx)
                final=(left_or_right[0],yc-s4)
                line(f'row_rise_{row}_{k}',left_or_right,final,w,w/2)
                for n,side in enumerate((-1,1)):
                    xc=final[0]+side*dx/2; lab=f'r{row+1}c{2*k+n+1}'
                    branch=split('level4_'+lab,final,'x',dx/2,side)
                    front=yc-l/2
                    line('inset_'+lab,branch,(xc,front+i))
                    patches.append(dict(name=lab,x=xc,y=yc,front_y=front,probe_y=(front+branch[1])/2))
                    rect('patch_'+lab,(xc-pw/2,xc+pw/2),(front,front+l),'patch')
    assert len(patches)==16 and len({(u['x'],u['y']) for u in patches})==16
    assert sum(x['name'].startswith('level') and x['name'].endswith('_transformer') for x in metal)==30
    # Check planar graph connectivity independently of CST. Feed overlap at intended T and elbow contacts.
    def touches(a,bb):
        return all(min(a[k][1],bb[k][1])>=max(a[k][0],bb[k][0])-1e-9 for k in ('x','y'))
    lines=[a for a in metal if a['kind']=='feed']
    for index,a in enumerate(lines):
        for b in lines[index+1:]:
            if touches(a,b):
                assert any(math.dist(j,k)<1.e-8 for j in segments[a['name']] for k in segments[b['name']]),(a['name'],b['name'])
    visited={0}; frontier=[0]
    while frontier:
        n=frontier.pop()
        for j,u in enumerate(metal):
            if j not in visited and touches(metal[n],u):
                visited.add(j);frontier.append(j)
    assert len(visited)==len(metal)
    for j,a in enumerate(metal):
        if a['kind']!='patch':continue
        contacts=[b['name'] for b in metal if b is not a and touches(a,b)]
        assert contacts==['inset_'+a['name'][6:]],(a['name'],contacts)
    single_path=(x1-port)+dy+(x2-x1)+dy/2-x2+(s0-s3)+dx+(s3-s4)+dx/2+(s4-l/2+i)
    return dict(parts=metal,patches=patches,board_x=[xmin,xmax],board_y=[ymin,ymax],port_x=port,port_y=-s0,
                board_width_mm=xmax-xmin,board_length_mm=ymax-ymin,network_total_centerline_mm=sum(legs),matching_annex=annex,
                equal_path_to_inset_mm=single_path,junctions=15+int("stub_start" in c),corporate_splitters=15,electrically_connected=True)

def build(de,folder,changes):
    c=parameters(changes);g=layout(c)
    p=de.new_mws();m=p.model3d
    for key,val in c.items():m.StoreParameter(key,str(val))
    for key in ('port_x','port_y'):m.StoreParameter(key,str(g[key]))
    history=json.loads(b.HISTORY.read_text(encoding='utf-8'))['history']
    m.add_to_history('D-band radiating template','\n'.join(history[0]['code']))
    for part in history:
        if part['caption'].startswith('define material:'):
            code='\n'.join(part['code'])
            if 'Polyimide' in part['caption']:
                code=code.replace('.Epsilon "3.5"','.Epsilon "eps_r"').replace('.TanD "0.0027"','.TanD "loss_tangent"')
                code=code.replace('.SetMaterialUnit "MHz", "mm"','.SetMaterialUnit "GHz", "mm"').replace('.TanDFreq "1.0"','.TanDFreq "150"')
            m.add_to_history(part['caption'],code)
    cst='Component.New "antenna"\n'
    for name,material,z in [('ground','Gold',('-metal_thickness','0')),('substrate','Polyimide (lossy)',('0','substrate_h'))]:
        cst+=b.brick(name,material,g['board_x'],g['board_y'],z)
        cst+=b.brick('launch_'+name,material,(g['port_x'],g['board_x'][0]),('port_y-port_halfwidth','port_y+port_halfwidth'),z)
        cst+=f'Solid.Add "antenna:{name}","antenna:launch_{name}"\n'
        if g['matching_annex']:
            a=g['matching_annex'];cst+=b.brick('annex_'+name,material,a['x'],a['y'],z)
            cst+=f'Solid.Add "antenna:{name}","antenna:annex_{name}"\n'
    m.add_to_history('Solid board and uniform port launch',cst)
    top=('substrate_h','substrate_h+metal_thickness')
    pieces={a['name']:a for a in g['parts']}
    for part in g['parts']:
        n=part['name'];code=b.brick(n,'Gold',part['x'],part['y'],top)
        if part['kind']=='patch':
            u=next(k for k in g['patches'] if k['name']==n[6:]);x=u['x'];y=u['front_y'];w=c['feed_width'];ig=c['inset_gap']
            for h,xr in enumerate(((x-w/2-ig,x-w/2),(x+w/2,x+w/2+ig))):
                cut=n+'_cut'+str(h);code+=b.brick(cut,'Vacuum',xr,(y,y+c['inset_length']),top)
                code+=f'Solid.Subtract "antenna:{n}","antenna:{cut}"\n'
        m.add_to_history('Signal '+n,code)
    merged={'trunk'};pending=[x for x in g['parts'] if x['name']!='trunk']
    # Union in graph order, so only touching objects reach the CAD boolean.
    series=[]
    while pending:
        add=[x for x in pending if any(all(min(x[k][1],pieces[n][k][1])>=max(x[k][0],pieces[n][k][0])-1e-9 for k in ('x','y')) for n in merged)]
        assert add
        for part in add:
            name=part['name'];series.append(f'Solid.Add "antenna:trunk","antenna:{name}"')
            merged.add(name);pending.remove(part)
    m.add_to_history('Union all 16 inset-fed patches and 15 splitter junctions','\n'.join(series))
    # Reuse the audited TD settings; rotate the waveguide-port normal to the side inlet.
    raw=Path(b.__file__).read_text(encoding='utf-8-sig')
    start=raw.index("code='''With Boundary")
    cfg=raw[start:].split("'''",2)[1]
    cfg=cfg.replace('.Ymin "open"','.Xmin "open"').replace('.Orientation "ymin"','.Orientation "xmin"')
    cfg=cfg.replace('.Xrange "-port_halfwidth", "port_halfwidth"','.Xrange "port_x", "port_x"')
    cfg=cfg.replace('.Yrange "-ground_length/2-launch_length", "-ground_length/2-launch_length"','.Yrange "port_y-port_halfwidth", "port_y+port_halfwidth"')
    m.add_to_history('One xmin port, open boundaries and inherited TD settings',cfg)
    folder.mkdir(parents=True,exist_ok=True);dest=folder/(folder.name+'.cst')
    p.save(str(dest))
    b.add_monitors(p,[145,154])
    (folder/'parameters.json').write_text(json.dumps(c,indent=2))
    (folder/'layout.json').write_text(json.dumps(g,indent=2))
    return p

