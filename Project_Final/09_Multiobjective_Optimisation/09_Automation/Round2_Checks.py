"""Material, feed continuity and far-field normalization checks for each fresh delivery."""
from Round2_Analysis import *
def geometry_audit(folder):
    c=read(folder/'parameters.json');dy=c.get('shift_y',0);w=c['feed_width'];h=c['substrate_h'];j=c['junction_y'];l=c['patch_length'];spacing=c['array_spacing'];width=c['patch_width'];edge=c['ground_length']/2+c.get('rear_delta',0);rear=dy+l/2
    vals=dict(feed_trunk_to_ground_vertical_clearance_mm=h,gap_between_patches_mm=spacing-width,distance_between_horizontal_branch_and_front_patch_mm=-l/2-j-w/2,inset_contact_length_mm=c['inset_length'],left_right_branch_length_mm=spacing/2-l/2+c['inset_length']-j,divider_to_negative_substrate_edge_mm=j+dy-w/2+c['ground_length']/2,clearance_to_positive_substrate_edge_mm=edge-rear,outer_patch_clearance_x_mm=(c['ground_width']-spacing-width)/2,single_port_y_mm=-c['ground_length']/2-c['launch_length'],passive_gap_mm=c.get('strip_gap',.08) if c.get('strip') else None)
    if c.get('strip'):vals['passive_rear_ground_margin_mm']=edge-rear-c.get('strip_gap',.08)-c['strip']
    requirements=['gap_between_patches_mm','distance_between_horizontal_branch_and_front_patch_mm','feed_trunk_to_ground_vertical_clearance_mm','inset_contact_length_mm','divider_to_negative_substrate_edge_mm','clearance_to_positive_substrate_edge_mm','outer_patch_clearance_x_mm']
    if c.get('strip'):requirements+=['passive_rear_ground_margin_mm','passive_gap_mm']
    vals['geometrically_valid']=all(vals[k]>0 for k in requirements)
    assert vals['geometrically_valid'],vals
    return vals
def historical_and_winner(paths):
    sub=R/'Angular_Cuts';sub.mkdir(exist_ok=True)
    from Round2_Patterns import detail
    old=ROOT.parent/'07_Array_1x2/02_Simulation_Results'
    write(DI/'Historical_Angular_Metrics.csv',detail(BASE,sub)+detail(old,sub))
    for folder in [BASE]+[Path(p) for p in dict.fromkeys(paths)]:
        geom=geometry_audit(folder);name=folder.name
        if folder==BASE:
            out=DI/'Baseline_Geometry_Check.json'
        else:out=folder/'Geometry_Check.json'
        out.write_text(json.dumps(geom,indent=2),encoding='utf-8')

