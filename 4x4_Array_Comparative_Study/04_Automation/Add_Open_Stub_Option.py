from pathlib import Path
p=Path(__file__).with_name('Build_4x4.py');s=p.read_text(encoding='utf-8-sig')
s=s.replace("    if 'match_width' in c:",'''    if 'stub_start' in c:
        x=port+c['stub_start'];sw=c['stub_width'];sl=c['stub_length']
        assert xmin+sw/2+.015<=x and x+sw/2+.04<=x1-q/2
        line('trunk',(port,-s0),(x,-s0),w)
        line('open_matching_stub',(x,-s0),(x,-s0+sl),sw)
        line('input_to_divider',(x,-s0),(x1,-s0),w,w/2)
    elif 'match_width' in c:''')
s=s.replace('junctions=15,electrically_connected=True','junctions=15+int("stub_start" in c),corporate_splitters=15,electrically_connected=True')
p.write_text(s,encoding='utf-8')
p=Path(__file__).with_name('Study_Sequence.py');s=p.read_text(encoding='utf-8-sig')
pos=s.index('def stable(')
extra=r'''def estimate_open_stub(c,initial):
    """Use the full-wave input Z to design a conventional single shunt-stub match."""
    z0=initial['modal_reference_ohm'];h=c['substrate_h'];eps=c['eps_r'];w0=c['feed_width']
    def modal(w):
        u=w/h;eff=(eps+1)/2+(eps-1)/2*(1+12/u)**-.5
        z=60/eff**.5*math.log(8/u+.25*u) if u<1 else 120*math.pi/(eff**.5*(u+1.393+.667*math.log(u+1.444)))
        return eff,z
    e0,z_est=modal(w0);scale=z0/z_est
    f,g=raw(P/'Initial_4x4','1D Results_S-Parameters_S1,1');sel=abs(f-150)<=1.0
    f=f[sel];z_in=z0*(1+g[sel])/(1-g[sel]);m=len(f)//2
    def transform(z,z0,t):return z0*(z+1j*z0*t)/(z0+1j*z*t)
    best=(math.inf,None)
    for w in [.065,.07,.075,.08,.085]:
        eff,zstub=modal(w);zstub*=scale
        fringe=.412*h*((eff+.3)*(w/h+.264))/((eff-.258)*(w/h+.8))
        for offset in np.arange(.56,.605,.002):
            x=c['board_x_min']-c['launch_length']+offset
            if x < c['board_x_min']+w/2+.015 or x+w/2+.04>c['first_split_x']-c['transformer_width']/2:continue
            t=np.tan(2*np.pi*f*np.sqrt(e0)*offset/299.792458)
            l=transform(z_in,z0,-t)
            for length in np.arange(.13,.285,.003):
                stub=1j*np.tan(2*np.pi*f*np.sqrt(eff)*(length+fringe)/299.792458)/zstub
                result=transform(1/(1/l+stub),z0,t)
                gamma=abs((result-50)/(result+50))
                score=.7*gamma[m]+.3*gamma.mean()
                if score<best[0]:best=(score,dict(stub_start=round(float(offset),4),stub_length=round(float(length),4),stub_width=w))
    assert best[1] is not None
    write_json(V/'Open_Stub_Matching_Proposal.json',dict(approximate_reflection_score=float(best[0]),
      proposal=best[1],source='150 GHz native input impedance and approximate uniform-line transfer, including microstrip open-end correction'))
    return best[1]
'''
s=s[:pos]+extra+s[pos:]
a=s.index("        if best['s11_50ohm_dB']>-10:\n");z=s.index("    print('SELECTED'",a)
s=s[:a]+"""        if best['s11_50ohm_dB']>-10:
            ch=estimate_open_stub(nominal,first)
            q=run('Matched_Stub_4x4',ch);tests.append(q)
            if q['s11_50ohm_dB']<best['s11_50ohm_dB']:best=q;change=ch
"""+s[z:]
p.write_text(s,encoding='utf-8')
p=Path(__file__).with_name('Finalize_4x4.py');s=p.read_text(encoding='utf-8')
s=s.replace("log=auto/'Study.log'","log=auto/'Study_Revised.log'").replace("auto/'Study.err'","auto/'Study_Revised.err'")
p.write_text(s,encoding='utf-8')

