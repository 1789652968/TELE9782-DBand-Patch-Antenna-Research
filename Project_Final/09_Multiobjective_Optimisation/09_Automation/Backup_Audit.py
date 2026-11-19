"""A byte-level backup audit and reproducible workflow notes."""
from pathlib import Path
import csv,hashlib,json
ROOT=Path(__file__).resolve().parents[1];DI=ROOT/'02_Diagnostics';DOC=ROOT/'10_Documentation'
def sha(p):
    with p.open('rb') as f:
        h=hashlib.sha256()
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def main():
    name='TELE9782_DBand_Efficiency_Final';src=ROOT.parent/'08_Efficiency_Optimisation/06_Final_Candidate'/name;dst=ROOT/'01_Baseline_Backup'/name
    left={p.relative_to(src):p for p in src.rglob('*') if p.is_file()};right={p.relative_to(dst):p for p in dst.rglob('*') if p.is_file()}
    assert left.keys()==right.keys(),(left.keys()-right.keys(),right.keys()-left.keys())
    with (DI/'Baseline_Backup_Check.csv').open('w',newline='',encoding='utf-8-sig') as fp:
        w=csv.writer(fp);w.writerow(['relative_path','bytes','source_SHA256','backup_SHA256'])
        for k,p in sorted(left.items()):
            a=sha(p);b=sha(right[k]);w.writerow([str(k),p.stat().st_size,a,b]);assert a==b,k
    (DI/'Backup_Verified.json').write_text(json.dumps(dict(files=len(left),bytes=sum(p.stat().st_size for p in left.values()),original=str(src),backup=str(dst),sha256=sha(next(dst.glob('*.cst')))),indent=2))
    (DOC/'Reproduction_Guide.md').write_text(r"""# 复现 TELE9782 150 GHz 第二轮多目标优化

## 查看与复核

1. 在 07_Final_Candidates/Final_Selection.json 查看角色到实际目录的映射。打开交付目录内与目录同名的 .cst，同时保留同名原生结果文件夹。基线完整备份在 01_Baseline_Backup。Baseline_Backup_Check.csv 给出源文件与备份的逐文件 SHA256。
2. 使用 CST Studio Suite 2024，Time Domain、130–170 GHz、单一 y-min 波导端口和开放边界。读取实际模型历史中的 Gold 和 Polyimide (lossy) 定义以及完整参数。各候选 parameters.json 给出参数，扩展几何（后缘、平移或无源片）的尺寸还写入独立模型历史。长度单位 mm，频率 GHz，功率 W，增益 dBi。
3. 在交付工程的副本上运行求解，避免改写已核查数据。查看 Model.log 的稳态终止、网格数和端口模消息。读取 1D Results 下的 S-Parameters、Reference Impedance 和 Power/Excitation [1]，以及 Farfields 下的 145、150、154 GHz 三维结果。各 1D 表每行保留原始实部及虚部。E/H 场、表面电流及点场使用 150 GHz 的原生监视器。
4. 使用原生复 Γ 与实参考阻抗计算 Zin=Zref(1+Γ)/(1−Γ)，再用 Γ50=(Zin−50)/(Zin+50) 核对 CST_50ohm.s1p。检查峰值及 +Z 实现增益，并比较归一化前后结果。核对 Prad/Pacc 与远场 ηrad、全空间方向性积分、接受功率闭合和原生实现增益的角度。Independent_Audit.json 记录审计值。
5. 完整方向图为 2° 步进的 CST ASCII 球面采样。+Z 对应 θ=0°。E 面取 φ=90°/270°，H 面取 φ=0°/180°。Radiation_Pattern_Audit.csv 给出 HPBW；Full_Sphere_Audit.csv 中的次峰采用前半空间内偏离主峰超过 10° 的局部最大值，空白表示该定义下未检出。法线交叉极化采用 Y 为共极化的 Ludwig-3 分解。近场相位图参照每个模型 |Ez| 最大的采样点，低于最大幅度 3% 的点掩蔽。

## 从工作目录复现

CST 运行时为 D:\TELE9782\CST Studio Suite 2024\Opera\code\bin\python.exe。数值绘图使用 C:\Users\Admin\AppData\Local\spyder-6\envs\spyder-runtime\python.exe（numpy、matplotlib），将后者目录及 Library\bin 放在 PATH 前面。第三方工具无需网络。每次只运行一个求解任务。

- 以本目录结构为模板，新建单独的实验工作目录，复制 01_Baseline_Backup、09_Automation 和空的其余阶段目录。脚本以自身上级目录为根。保留原始 07 与 08 路径以便生成历史对照。
- 在 09_Automation 中使用 CST Python 执行 Round2_Core.py 重放初筛。Round2_Search.py 读取已完成的初筛记录，进行自适应联合优化、三种角色选择、两种网格、保存重开复算及公差研究。独立的密网格采用 38/57，交付文件采用 36/54。脚本验证参数完全相同后才复用 completed 结果；从空候选目录运行可触发真正的新求解。
- 对现有数据仅重新生成比较表和工程报告，可用数值绘图 Python 运行 Round2_Delivery.py。需要重新导出高密度复电场样本时，在完成求解后运行 CST Python 的 Round2_Fields.py。该步骤在独立的历史/场视图副本中读取原生三维结果。Round2_Report.py 作为完整后处理入口先导出场，再调用交付生成程序。
- PowerShell 入口 Continue_Study.ps1 可在初筛已启动后接续后续任务，原始日志位于 09_Automation。若脚本中断，先读取相应 *.err 和候选的 error.json。setup_ready 标记记录已完整建立的几何，round2.json 仅在真实求解和所需导出均结束时写入。保留失败目录作为审计记录。

## 证据位置

08_Results_and_Figures 汇总优化试验、选型、收敛、频率、公差、近场和远场数据。各个求解目录内，.cst 同名目录的 Result/Model.log 是求解器日志，Model/3D/ModelHistory.json 记录物理模型。summary.json 保存原生远场监视器统计及消息，1D Results_*.csv 为原生一维导出。Farfield_*_Sphere.txt 为 CST 原生全空间输出。round2.json 和汇总表为可复算的后处理。图中频率点取实际求解监视器，不在缺失频点构造方向图。
""",encoding='utf-8')
if __name__=='__main__':main()

