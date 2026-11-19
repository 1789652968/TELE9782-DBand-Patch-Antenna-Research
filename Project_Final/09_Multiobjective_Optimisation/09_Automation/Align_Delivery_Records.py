from pathlib import Path
d=Path(__file__).resolve().parent
p=d/'Round2_Report.py';s=p.read_text(encoding='utf-8-sig')
old="        failed.append(dict(name=path.parent.name,solver='ATTEMPT_ERROR',path=str(path.parent),note=read(path)['error']))"
new="""        known=next((v for v in rows if v['path']==str(path.parent)),None)
        if known is not None:
            known['recovered_error']=read(path)['error'];known['recovered_error_file']=str(path)
        else:
            status=read(path.parent/'summary.json')['solver']['state'] if (path.parent/'summary.json').exists() else 'UNVERIFIED'
            failed.append(dict(name=path.parent.name,solver=status,path=str(path.parent),note=read(path)['error']))"""
if old in s:p.write_text(s.replace(old,new),encoding='utf-8')
p=d/'Round2_Supplement.py';s=p.read_text(encoding='utf-8-sig').replace("recommended=d,fullsphere","recommended=read(V/'Recommended_Project.json'),fullsphere");p.write_text(s,encoding='utf-8')
p=d/'Round2_Delivery.py';s=p.read_text(encoding='utf-8-sig').replace('90% 在三次高分辨率计算中均达到：**{support}**。',"{'生产网格、加密网格和交付复算均达到 90%。' if support else '90% 目标未通过三次高分辨率验证。'}")
p.write_text(s,encoding='utf-8')
g=d.parent/'10_Documentation/Reproduction_Guide.md';s=g.read_text(encoding='utf-8-sig')
if 'Round2_Resume.py' not in s:g.write_text(s+"""
## 本次中断恢复与精细定位

Round2_Resume.py 是本轮交付所用的续跑入口。完成 Round2_Core.py 初筛后，若从空目录重建，先在 CST Python 会话用 Round2_Search.focused(de) 完成联合筛选及 Round2_Search.final_jobs(de) 进行初选验证。已有 H085 的生产和加密结果时，可直接运行 Round2_Resume.py。它先核对成功求解的原生复 S11 与原导出 1001 个采样值，在独立 CST 连接补齐图像中断时未完成的数值导出。之后按实测方向相反的两个位置补做几何夹逼，再选择和复算入围候选。Round2_Local_Bracket.py 记录最后一次位置细化。故障保存在 H085_Delivery/error.json。原生求解成功和图片导出错误在审计表中分别记录。

Resume_Publish.py 是本次交付的后处理入口。在搜索结束后，它先做独立端口模式频率试验，读取历史工程副本和最终候选的实测数值场，再生成最终报告与图表。日志为 Resume.log、Resume.err、Publish.log、Publish.err。本轮完整搜索不需要重复执行已完成的历史脚本 Round2_Targeted.py。
""".replace('实测数值场','原生仿真场'),encoding='utf-8')

