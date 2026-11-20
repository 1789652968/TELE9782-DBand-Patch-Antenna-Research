from pathlib import Path
p=Path(__file__).resolve().parent
f=p/'Build_4x4.py';s=f.read_text()
s=s.replace("xmin=c['board_x_min']; xmax=c['board_x_max']; port=xmin-c['launch_length']", """xmin=c['board_x_min']; xmax=c['board_x_max']; oldport=xmin-c['launch_length']
    extra=c.get('extension_l50_mm',0)+c.get('extension_lq_mm',0)+(.5 if 'extension_match_width_mm' in c else 0)
    port=oldport-extra""")
s=s.replace("    if 'stub_start' in c:", """    annex=None
    if 'extension_match_width_mm' in c:
        xq=port+.5;x50=xq+c['extension_lq_mm'];ww=c['extension_match_width_mm']
        line('trunk',(port,-s0),(xq,-s0),w)
        line('wideQuarterWave',(xq,-s0),(x50,-s0),ww)
        line('return_to_original_plane',(x50,-s0),(oldport,-s0),w)
        line('core_input',(oldport,-s0),(x1,-s0),w,w/2)
        annex=dict(x=[xq-.14,x50+.14],y=[-s0-ww/2-.19,-s0+ww/2+.19])
        assert annex['x'][0]>port and annex['x'][1]<oldport
    elif 'stub_start' in c:""")
s=s.replace("board_width_mm=xmax-xmin,board_length_mm=ymax-ymin,network_total_centerline_mm=sum(legs),",
"""board_width_mm=xmax-xmin,board_length_mm=ymax-ymin,network_total_centerline_mm=sum(legs),matching_annex=annex,""")
s=s.replace("        cst+=f'Solid.Add \"antenna:{name}\",\"antenna:launch_{name}\"\\n'", """        cst+=f'Solid.Add "antenna:{name}","antenna:launch_{name}"\\n'
        if g['matching_annex']:
            a=g['matching_annex'];cst+=b.brick('annex_'+name,material,a['x'],a['y'],z)
            cst+=f'Solid.Add "antenna:{name}","antenna:annex_{name}"\\n'""")
f.write_text(s,encoding='utf-8')
f=p/'Extract_Results.py';s=f.read_text(encoding='utf-8')
s=s.replace("res['maximum_port_extension_mm']=c['launch_length']","res['maximum_port_extension_mm']=geometry['board_x'][0]-geometry['port_x'] if geometry else c['launch_length']")
s=s.replace("+(c['launch_length'] if geometry else 0)","+(res['maximum_port_extension_mm'] if geometry else 0)")
f.write_text(s,encoding='utf-8')
f=p/'Study_Sequence.py';s=f.read_text(encoding='utf-8')
at=s.index('def stable(')
addition=r'''def estimate_quarter_wave(c,initial):
    """Match near the measured low-resistance point, with a separate straight-line landing."""
    z0=initial['modal_reference_ohm'];h=c['substrate_h'];eps=c['eps_r']
    def modal(w):
        u=w/h;eff=(eps+1)/2+(eps-1)/2*(1+12/u)**-.5
        z=120*math.pi/(eff**.5*(u+1.393+.667*math.log(u+1.444)))
        return eff,z
    e0,z_est=modal(c['feed_width']);scale=z0/z_est
    f,g=raw(P/'Initial_4x4','1D Results_S-Parameters_S1,1');sel=abs(f-150)<=1.1
    f=f[sel];z_in=z0*(1+g[sel])/(1-g[sel]);m=len(f)//2
    def line(z,r,l,e):
        t=np.tan(2*np.pi*f*l*np.sqrt(e)/299.792458);return r*(z+1j*r*t)/(r+1j*z*t)
    best=(math.inf,None,None)
    for l in np.arange(.47,.651,.006):
        z= line(z_in,z0,l,e0)
        if abs(z[m].imag)>10:continue
        for w in np.arange(.37,.86,.02):
            eff,r=modal(w)
            for lq in np.arange(.23,.334,.008):
                zprod=line(line(z,r*scale,lq,eff),z0,.5,e0);g50=abs((zprod-50)/(zprod+50))
                score=.66*float(g50[m])+.27*float(g50.mean())+.07*float(max(g50))
                if score<best[0]:
                    best=(score,dict(extension_l50_mm=round(float(l),5),extension_lq_mm=round(float(lq),5),extension_match_width_mm=round(float(w),5)),
                        dict(load_r=float(z[m].real),load_x=float(z[m].imag),transmission_line_Z_ohm=r*scale,predicted_s11_50ohm_dB=20*math.log10(g50[m])))
    assert best[1] is not None
    write_json(V/'Quarterwave_Transformer_Proposal.json',dict(settings=best[1],approximation=best[2],source='Native initial input impedance; uniform-line model calibrated to native port ref'))
    return best[1]
'''
s=s[:at]+addition+s[at:]
s=s.replace("    if '--wait-existing' in sys.argv:","    if '--wait-refined' in sys.argv:\n        existing=P/'Refined_4x4'\n        while not (existing/'Export_Complete.json').is_file():\n            if (existing/'Run_Failure.txt').is_file():break\n            time.sleep(15)\n    if '--wait-existing' in sys.argv:")
needle="    print('SELECTED',best['design'],change,flush=True)"
addition="""    if best['s11_50ohm_dB']>-10:
        q0=run('Refined_4x4',change|dict(mesh_near=26,mesh_box=39),True)
        if q0['s11_50ohm_dB']>-10:
            ch=estimate_quarter_wave(nominal,first)
            q=run('Matched_Quarterwave_4x4',ch);tests.append(q)
            if q['s11_50ohm_dB']<best['s11_50ohm_dB']:
                best=q;change=ch
"""
s=s.replace(needle,addition+needle)
s=s.replace("fine_case='Refined_4x4';fine=", "fine_case='Quarterwave_Refined_4x4' if 'extension_match_width_mm' in change else 'Refined_4x4';fine=")
f.write_text(s,encoding='utf-8')
f=p/'Finalize_4x4.py';s=f.read_text(encoding='utf-8').replace("auto/'Study_Revised.log'","auto/'Study_Complete.log'").replace("auto/'Study_Revised.err'","auto/'Study_Complete.err'");f.write_text(s,encoding='utf-8')

