from pathlib import Path
p=Path(__file__).with_name('Round2_Delivery.py');s=p.read_text(encoding='utf-8')
needle="    report=f"
ins="""    metal_path=ROOT.parent/'08_Efficiency_Optimisation/07_Results_and_Figures/All_Candidates.csv'
    with metal_path.open(encoding='utf-8-sig',newline='') as fp:
        metal_rows={row['name']:row for row in csv.DictReader(fp) if row['name'] in ['H75_Length','Au3um','Au5um']}
    skin_um=1.e6/np.sqrt(np.pi*150.e9*(4*np.pi*1.e-7)*4.561e7)
"""
assert needle in s
if '    metal_path=' not in s:
    s=s.replace(needle,ins+needle)
    needle='## 辐射损耗与波束偏转'
    assert needle in s
    s=s.replace(needle,"""150 GHz、σ=4.561×10⁷ S/m、μr=1 的良导体趋肤深度为 {skin_um:.3f} μm。标称金厚 2 μm 约为 {2/skin_um:.1f} 倍趋肤深度。第一轮真实材料的同设置网格试验中，2、3、5 μm 金厚对应的辐射效率分别为 {float(metal_rows['H75_Length']['eta']):.3f}%、{float(metal_rows['Au3um']['eta']):.3f}% 和 {float(metal_rows['Au5um']['eta']):.3f}%。2 和 3 μm 的模型均为 100,920 单元，5 μm 的模型为 161,472 单元。加厚没有显示稳定效率收益，因此本轮工程保留 2 μm，另用实际求解检查制造厚度偏差。来源为 08_Efficiency_Optimisation/07_Results_and_Figures/All_Candidates.csv 中的 H75_Length、Au3um 和 Au5um；这三个历史值未参加第二轮候选排名。

"""+needle)
    p.write_text(s,encoding='utf-8')

