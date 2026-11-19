"""Geometry extensions and local field sampling for focused and final runs."""
import Round2_Core as core
from Round2_Core import b
original=core.decorate
original_fields=core.fields
def decorate(m,c):
    dy=c.get('shift_y',0)
    if not dy:
        original(m,c);return
    # Finish the bend operation in the original reference frame, then move the connected gold.
    original(m,c|{'strip':0})
    ymin=-c['ground_length']/2-c['launch_length']
    assert c['junction_y']+dy-c['feed_width']/2>=-c['ground_length']/2-.000001
    assert c['patch_length']/2+dy < c['ground_length']/2+c.get('rear_delta',0)
    move=f'''With Transform
.Reset
.Name "antenna:trunk"
.Vector "0", "{dy}", "0"
.UsePickedPoints "False"
.InvertPickedPoints "False"
.MultipleObjects "False"
.GroupObjects "False"
.Repetitions "1"
.MultipleSelection "False"
.Destination ""
.Material ""
.Transform "Shape", "Translate"
End With
'''
    if dy<0:
        change=b.brick('trim_trunk','Vacuum',('-feed_width','feed_width'),(ymin+dy-.02,ymin),('substrate_h','substrate_h+metal_thickness'))
        move+=change+'Solid.Subtract "antenna:trunk","antenna:trim_trunk"'
    else:
        change=b.brick('extend_trunk','Gold',('-feed_width/2','feed_width/2'),(ymin,ymin+dy),('substrate_h','substrate_h+metal_thickness'))
        move+=change+'Solid.Add "antenna:trunk","antenna:extend_trunk"'
    m.add_to_history('Move divider and radiators along Y; retain the original single port plane',move)
    if c.get('strip'):
        for side in [-1,1]:
            x=side*c['array_spacing']/2; w=c.get('strip_w',c['patch_width']*.95)
            y=dy+c['patch_length']/2+c.get('strip_gap',.08)
            assert y+c['strip']<c['ground_length']/2+c.get('rear_delta',0)
            m.add_to_history('Passive gold loading '+str(side),b.brick('par'+('L' if side<0 else 'R'),'Gold',(x-w/2,x+w/2),(y,y+c['strip']),('substrate_h','substrate_h+metal_thickness')))
def fields(p,folder,c):
    original_fields(p,folder,c);m=p.model3d;tree=m.get_tree_items()
    key=next(k for k in tree if k.startswith('2D/3D Results') and 'e-field' in k.lower() and '(f=150)' in k.lower());assert m.SelectTreeItem(key)
    dy=c.get('shift_y',0);d=c['array_spacing']/2;l=c['patch_length'];h=c['substrate_h'];j=c['junction_y']
    def sample(points,filename):
        pts=folder/(filename+'_Points.txt');pts.write_text(''.join(f'{x} {y} {z}\n' for x,y,z in points))
        a=m.ASCIIExport;a.Reset();a.FileName(str(folder/(filename+'.txt')));a.SetPointFile(str(pts));a.Execute()
    sample([(sg*d,dy+j+(-l/2-j)*t,h/2) for t in [.25,.4,.55,.7] for sg in [-1,1]],'Branch_Ez_150')
    sample([(sg*d+dx*c['patch_width'],dy+sy*(l/2-.004),h/2) for sg in [-1,1] for sy in [-1,1] for dx in [-.33,-.20,0,.20,.33]],'Radiating_Edge_Efield_150')
    sample([(x,dy+y,h/2) for y in [j+(-l/2-j)*.4,-l/2+.01,0,l/2-.01] for x in [-d,0,d]],'Aperture_Efield_150')
def install():
    core.decorate=decorate;core.fields=fields

