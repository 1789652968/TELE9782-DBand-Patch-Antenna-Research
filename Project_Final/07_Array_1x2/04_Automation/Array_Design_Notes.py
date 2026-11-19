"""Write engineering notes from the actual delivered parameters and reference-plane diagnostics."""
from Array_Results_Extraction import *
def micro(w,h=.040,er=3.5):
    u=w/h;eps=(er+1)/2+(er-1)/2*((1+12/u)**-.5+(0.04*(1-u)**2 if u<1 else 0))
    z=60/np.sqrt(eps)*np.log(8/u+u/4) if u<1 else 120*np.pi/(np.sqrt(eps)*(u+1.393+.667*np.log(u+1.444)))
    return eps,z,299.792458/150/np.sqrt(eps)/4
def width(zo):
    lo=.002;hi=.4
    for _ in range(55):
        x=(lo+hi)/2
        if micro(x)[1]>zo:lo=x
        else:hi=x
    return (lo+hi)/2
def put(name,lines):
    (DOC/name).write_text(lines.strip()+'\n',encoding='utf-8')
def write_theory():
    p=read(P/'parameters.json');v=metrics(P,R)
    d=p['array_spacing'];L=p['patch_length'];w=p['patch_width'];lam=299.792458/150;er=p['eps_r'];h=p['substrate_h'];tw=p['transformer_width'];tl=p['transformer_length']
    eps=(er+1)/2+(er-1)/2*(1+12*h/w)**-.5
    fringe=.412*h*(eps+.3)*(w/h+.264)/((eps-.258)*(w/h+.8))
    estimate=299.792458/(2*(L+2*fringe)*np.sqrt(eps))
    theory=f"""# Array design theory

The assignment requires directivity above 6.5 dBi in 130–170 GHz. The validated single inset-fed patch supplies the starting element. Its width is 0.667 mm, its length is 0.513 mm, and its inset is 0.190 mm. We keep its metals, substrate and polarization to make a meaningful comparison at 150 GHz.

## Resonant length

The transmission-line estimate uses W = c/(2f) sqrt(2/(εr+1)), effective permittivity εeff = (εr+1)/2 + (εr−1)/(2 sqrt(1+12h/W)), and open-edge extension ΔL/h = 0.412 (εeff+0.3)(W/h+0.264) / ((εeff−0.258)(W/h+0.8)). At 150 GHz this gives W = 0.6662 mm and L ≈ 0.5204 mm. For the selected array element W = {w:.3f} mm, L = {L:.3f} mm, εeff = {eps:.4f} and ΔL = {fringe:.5f} mm. The half-wave estimate c/[2(L+2ΔL)√εeff] gives **{estimate:.2f} GHz**. The full assembled antenna has minimum S11 at **{v['fmin_GHz']:.2f} GHz**, a difference of {abs(estimate-v['fmin_GHz']):.2f} GHz ({abs(estimate-v['fmin_GHz'])/estimate*100:.2f}% of estimate). The S11 minimum characterises impedance matching of the driven assembly. Coupled elements, bends, transformers and finite ground affect this frequency.

## Aperture and beam

Elements occupy x = ±{d/2:g} mm with the same y coordinate and orientation. At 150 GHz λ0 = {lam:.4f} mm. The initial spacing of 1.00 mm corresponds to {1/lam:.3f}λ0. The selected {d:.2f} mm spacing is {d/lam:.3f}λ0, leaving an edge gap of {d-w:.3f} mm and a side clearance of {(p['ground_width']-d-w)/2:.3f} mm on each side. For in-phase excitations the ideal two-source array factor is 2 cos(πd sinθ cosφ/λ0). In XZ it varies with angle. In YZ it is constant. This predicts the plane most likely to narrow. All reported pattern values instead come from the full CST model with finite ground and feed scattering. Broadside y polarisation is checked using Eφ and Eθ at θ=0°, φ=0° in the angular export.

A doubled number of radiators alone does not determine the change in realized gain. Directivity normalizes angular radiation by radiated power. Multiplication by radiation efficiency and accepted-power fraction converts it to realized gain. The three-model comparison separates ground-size and excitation effects to the extent supported by one enlarged-ground control."""
    put('Array_Design_Theory.md',theory)
    table=['| Impedance (Ω) | Width (mm) | εeff | λg/4 (mm) |','|---:|---:|---:|---:|']
    for z in [50,math.sqrt(5000),100,math.sqrt(1250)]:
        wi=width(z);ee,_,lq=micro(wi);table.append(f'| {z:.2f} | {wi:.5f} | {ee:.4f} | {lq:.5f} |')
    ee,zt,lq=micro(tw)
    mode=read(R/'Port_Mode_Check.json')
    mode_table=['| CST section at 150 GHz | Modal line Z (Ω) | CST effective permittivity | Propagation constant, raw Re + j Im | λg/4 from εeff (mm) |','|---|---:|---:|---|---:|']
    for label,values in mode.items():
        eff=values['Effective Dielectric Constant']['real'];gam=values['Gamma'];mode_table.append(f"| {label} | {values['Line Impedance']['real']:.3f} | {eff:.5f} | {gam['real']:.6g} + j {gam['imag']:.6g} ({gam['ylabel']}) | {lam/4/math.sqrt(eff):.5f} |")
    path=d/2+(-L/2+p['inset_length']-p['junction_y'])
    feed=f"""# Corporate-feed calculations

Two inset patch loads of nominal 50 Ω connected directly in parallel present 25 Ω. In Option A each approximately quarter-wave branch has nominal impedance √(50×100) = 70.71 Ω. Its input at the T is approximately 70.71²/50 = 100 Ω. Two transformed branches in parallel give 50 Ω. Option B would instead place a common √(25×50) = 35.36 Ω quarter-wave section before the T and run 50 Ω branches. The wider common section changes the available routing and needs independent full-wave validation. Option A met the operating-point objectives and was taken through full-wave development. Option B was evaluated analytically.

## Physical dimensions

For u = w/h, εeff uses (εr+1)/2 + (εr−1)/2 [(1+12/u)^−½ + δ], where δ = 0.04(1−u)² for u<1, else zero. For u<1, Z0 = (60/√εeff) ln(8/u+u/4). For u≥1, Z0 = 120π / [√εeff (u+1.393+0.667 ln(u+1.444))]. Solving these zero-thickness equations on the 0.040 mm polyimide gives the following starting values.

{chr(10).join(table)}

The built trunk and 50 Ω outlet sections are 0.090 mm wide. The initial branches were 0.049 mm × 0.308 mm. Selected physical width × length is **{tw:.3f} × {tl:.3f} mm**, giving {zt:.2f} Ω and {90*tl/lq:.1f}° on the quasi-static isolated-line approximation. At the junction y={p['junction_y']} mm, the straight transformer extends along ±x and meets the 0.090 mm section. The nominal horizontal distance from T center to bend center is {d/2:.3f} mm. Both routed paths from T center to the inset endpoint are {path:.3f} mm on the centerline. The straight 50 Ω continuation, right-angle unmitered bends, finite metallization, and T overlap load the transformers. Narrow-line length includes the fraction overlapping the T. Electrical tuning used the complete connected antenna.

## Native modal check

{chr(10).join(mode_table)}

The mode-only diagnostics reuse the launch dielectric, ground, signal thickness, port aperture and final mesh settings. Only the strip width changes at the diagnostic cross-section. These uniform-line modal data describe the local line. The actual transformer is embedded between a T junction, a bend and a coupled patch load. Paired complex Ez exports compare the two loaded arms at equal physical reference planes."""
    put('Feed_Network_Calculations.md',feed)
    return theory,feed
if __name__=='__main__':write_theory()
