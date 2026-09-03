# -*- coding: utf-8 -*-
import json
import os
_dir=os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(_dir,'data.json'),encoding='utf-8'))

CH_ORDER = ['中国','亚洲 · 中东','欧洲','美洲','全球品牌']
def sub_of(r): return r['subgroup'] or ''

html_parts = []
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

# 按章/子组组织
def emit_rows(lst):
    for r in lst:
        is_annual = (r['chip'][:2].isdigit() and ('年' in r['chip'] or '年度' in r['chip'])) and not any(k in r['chip'] for k in ['估','测','计','累计','宿','团','场','体','含','期','过','峰'])
        # 简单年度判定：chip 以4位年开头且不含非年度词
        import re as _re
        is_annual = bool(_re.match(r'^(20\d\d|19\d\d)[ 年]', r['chip'])) and not any(k in r['chip'] for k in ['估','预','累计','宿','集团','整体','商场','含','过夜','峰值','高峰','展期','前十月'])
        chip_cls = 'y' if is_annual else 'o'
        vis_html = f'<div class="vis">{esc(r["vis"])}</div><span class="chip {chip_cls}">{esc(r["chip"])}</span>'
        if r['pph']:
            pph_html = f'<div class="pph">{esc(r["pph"])}</div><span class="chip psrc">{esc(r["pph_src"])}</span>'
        else:
            pph_html = '<div class="pph none">—</div><span class="chip no">暂无公开</span>'
        link = f'<a class="cname" href="{r["slug"]}/">{esc(r["name"])}</a>'
        loc = esc(r['location'])
        desc = esc(r['desc'])
        html_parts.append(
            '<tr>'
            f'<td class="col-name"><div class="nwrap">{link}<div class="loc">{loc}</div></div></td>'
            f'<td class="col-vis">{vis_html}</td>'
            f'<td class="col-pph">{pph_html}</td>'
            f'<td class="col-desc">{desc}</td>'
            '</tr>')

for ch in CH_ORDER:
    ch_rows = [r for r in rows if r['chapter']==ch]
    if not ch_rows: continue
    html_parts.append(f'<tr class="chap-row"><td colspan="4">{esc(ch)} <span>{len(ch_rows)} 例</span></td></tr>')
    # 子组
    if ch=='中国':
        seen=[]
        for r in ch_rows:
            s=sub_of(r)
            if s and s not in seen:
                seen.append(s)
                sg=[x for x in ch_rows if sub_of(x)==s]
                html_parts.append(f'<tr class="sub-row"><td colspan="4"><span class="sdot"></span>{esc(s)} <span>{len(sg)} 例</span></td></tr>')
            if not s:
                html_parts.append(f'<tr class="sub-row plain"><td colspan="4">{esc(r["name"])}</td></tr>')
        # 中国里无子组的直接跟卡片 暂不做单独tr
        # 重新按顺序emit，但需跳过于组header本身属同一层：改为分组emit
    else:
        pass

# 上面只放了header，行没放。改为重构：直接组织好顺序再统一 emit。
html_parts.clear()
def organized():
    seq=[]
    for ch in CH_ORDER:
        ch_rows=[r for r in rows if r['chapter']==ch]
        if not ch_rows: continue
        seq.append(('chap',ch,ch_rows))
        subs=[]; groups={}
        for r in ch_rows:
            s=sub_of(r)
            if s: groups.setdefault(s,[]).append(r)
        for s,lst in groups.items():
            seq.append(('sub',s,lst))
        # 无子组的散卡
        loose=[r for r in ch_rows if not sub_of(r) and r['chapter']==ch]
        if loose: seq.append(('loose',None,loose))
    return seq

body=''
for kind,title,lst in organized():
    if kind=='chap':
        body+=f'<tr class="chap-row"><td colspan="4">{esc(title)}<span class="cnum">{len(lst)} 例</span></td></tr>'
    elif kind=='sub':
        body+=f'<tr class="sub-row"><td colspan="4"><span class="sdot"></span>{esc(title)}<span class="cnum">{len(lst)} 例</span></td></tr>'
    else:
        pass
    # emit rows（仅子组/散卡层；章头行自身不发数据）
    if kind == 'chap':
        continue
    for r in lst:
        import re as _re
        chip=r['chip']
        non_annual=['估','预','累计','商场','合计','四园','整体','含本园','未标','峰值','高峰','展期','前十月','过夜','容量','计划','规划','接待上限','入住率','国庆','暑期','非年度']
        is_annual = chip.startswith('TEA 20') or (bool(_re.match(r'^(20\d\d|19\d\d)[ 年]', chip)) and not any(k in chip for k in non_annual))
        chip_cls = 'tea' if chip.startswith('TEA 20') else ('y' if is_annual else 'o')
        vis_html = f'<div class="vis">{esc(r["vis"])}</div><span class="chip {chip_cls}">{esc(r["chip"])}</span>'
        if r['pph']:
            pph_html = f'<div class="pph">{esc(r["pph"])}</div><span class="chip psrc">{esc(r["pph_src"])}</span>'
        else:
            pph_html = '<div class="pph none">—</div><span class="chip no">暂无公开</span>'
        link=f'<a class="cname" href="{r["slug"]}/index.html">{esc(r["name"])}</a>'
        body+=( '<tr>'
                f'<td class="col-name"><div class="nwrap">{link}<div class="loc">{esc(r["location"])}</div></div></td>'
                f'<td class="col-vis">{vis_html}</td>'
                f'<td class="col-pph">{pph_html}</td>'
                f'<td class="col-desc">{esc(r["desc"])}</td></tr>')

n_annual = len([r for r in rows if (r['chip'].startswith('TEA 20')) or (r['chip'][:4].isdigit() and not any(k in r['chip'] for k in ['估','预','累计','商场','合计','四园','整体','含本园','未标','峰值','高峰','展期','前十月','过夜','容量','计划','规划','接待上限','入住率','国庆','暑期','非年度']))])
n_pph = len([r for r in rows if r['pph']])

CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
html { font-size:17px; scroll-behavior:smooth; }
body { font-family:'DM Sans',-apple-system,BlinkMacSystemFont,sans-serif; background:#F5F0E8; color:#1A1520; line-height:1.6; }
.header { background:linear-gradient(165deg,#1A1520 0%,#2D2035 50%,#1A1520 100%); color:#FFF; padding:3rem 2rem 2.2rem; text-align:center; position:relative; overflow:hidden; }
.header::before { content:''; position:absolute; inset:0; background:radial-gradient(ellipse at 30% 60%, rgba(200,160,100,0.08) 0%, transparent 60%), radial-gradient(ellipse at 70% 30%, rgba(120,90,160,0.07) 0%, transparent 60%); }
.header-inner { position:relative; z-index:1; max-width:900px; margin:0 auto; }
.back { position:absolute; top:1.3rem; left:1.5rem; color:rgba(255,255,255,0.7); text-decoration:none; font-size:0.9rem; z-index:2; }
.back:hover { color:#C8A45C; }
.header h1 { font-family:'Playfair Display',serif; font-size:2.5rem; font-weight:800; letter-spacing:0.02em; margin-bottom:0.4rem; }
.header .sub { color:rgba(255,255,255,0.62); font-size:0.98rem; max-width:640px; margin:0 auto; }
.header .stats { margin-top:1.1rem; display:flex; gap:0.5rem; justify-content:center; flex-wrap:wrap; }
.stat { font-family:'DM Mono',monospace; font-size:0.74rem; color:#C8A45C; border:1px solid rgba(200,160,100,0.45); border-radius:100px; padding:0.26rem 0.8rem; }
.wrap { max-width:1180px; margin:0 auto; padding:2rem 1.6rem 3rem; }
.legend { font-size:0.76rem; color:#8B7355; margin:0 0 0.8rem; display:flex; flex-wrap:wrap; gap:1rem; align-items:center; }
.legend .chip { vertical-align:middle; }
.scroll { overflow-x:auto; border:1px solid #E8E0D5; border-radius:12px; background:#FFF; }
table { width:100%; border-collapse:collapse; min-width:1080px; }
thead th { font-family:'DM Mono',monospace; font-size:0.7rem; letter-spacing:0.08em; text-transform:uppercase; color:#8B7355; text-align:left; padding:0.9rem 1rem; background:#FAF6EE; border-bottom:2px solid #E0D6C6; position:sticky; top:0; }
thead th small { display:block; font-family:'DM Sans',sans-serif; font-size:0.68rem; text-transform:none; letter-spacing:0; color:#B0A28C; font-weight:400; margin-top:2px; }
th.c-vis { width:13%; } th.c-pph { width:12%; } th.c-desc { width:44%; }
tr.chap-row td { padding:1rem 1rem 0.5rem; font-family:'Playfair Display',serif; font-weight:800; font-size:1.18rem; color:#1A1520; }
tr.chap-row { border-top:3px solid #2D2035; background:#F5F0E8; }
tr.chap-row:first-child { border-top:none; }
tr.sub-row td { padding:0.55rem 1rem 0.3rem; font-weight:700; font-size:0.86rem; color:#8B3A4A; background:#FBF7F0; }
tr.sub-row td { border-bottom:none; }
.cnum { font-family:'DM Mono',monospace; font-weight:400; font-size:0.68rem; color:#B0A28C; margin-left:0.6rem; }
.sdot { display:inline-block; width:7px; height:7px; background:#C8A45C; border-radius:2px; margin-right:0.5rem; }
tbody tr.data { border-top:1px solid #EFE7DA; }
tbody tr.data:hover { background:#FBF6EC; }
td { vertical-align:top; padding:0.8rem 1rem; }
.col-name { width:20%; }
.nwrap .cname { font-family:'Playfair Display',serif; font-weight:700; font-size:1.02rem; color:#1A1520; text-decoration:none; }
.nwrap .cname:hover { color:#8B3A4A; }
.loc { font-size:0.72rem; color:#A09080; margin-top:3px; font-family:'DM Mono',monospace; }
.vis { font-family:'DM Mono',monospace; font-weight:500; font-size:1.02rem; color:#1A1520; }
.chip { display:inline-block; font-size:0.64rem; font-family:'DM Mono',monospace; letter-spacing:0.02em; margin-top:5px; padding:0.12rem 0.5rem; border-radius:100px; white-space:nowrap; }
.chip.y { background:#1A1520; color:#FFF; }
.chip.tea { background:#8B3A4A; color:#FFF; }
.chip.o { border:1px solid #D8CCB8; color:#8B7355; background:#FFF; }
.chip.no { border:1px dashed #E0D6C6; color:#C4B7A2; background:transparent; }
.chip.psrc { background:#FFF3EC; color:#8B3A4A; border:1px solid #F0D8CC; }
.pph { font-family:'DM Mono',monospace; font-weight:600; font-size:1.05rem; color:#8B3A4A; }
.pph.none { color:#D5C9B6; font-weight:400; }
.col-desc { font-size:0.8rem; color:#6B5E50; line-height:1.55; }
.foot { margin-top:1rem; font-size:0.75rem; color:#8B7355; line-height:1.8; }
.foot b { color:#6B5E50; }
.footer { text-align:center; padding:2rem; font-size:0.8rem; color:#8B7B60; border-top:1px solid #E8E0D5; max-width:1200px; margin:0 auto; }
@media (max-width:640px){ .header{ padding:3rem 1rem 1.8rem; } .header h1{font-size:1.9rem;} .wrap{padding:1.4rem 0.8rem 2rem;} }
"""

doc = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>总览 · 张走走的文旅案例库</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&family=DM+Mono:wght@400;500;600&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,500&display=swap" rel="stylesheet">
<style>""" + CSS + """</style>
</head>
<body>
<div class="header">
  <a class="back" href="index.html">← 返回首页</a>
  <div class="header-inner">
    <h1>案例总览</h1>
    <p class="sub">71 个已上线案例一表纵览：单园客流（尽量取年度实值，非年度口径一律单独标注）+ 娱乐值 PPH（全园设施理论小时载客总量）。客流值取自各案例页已核实研究，凡该园登上 TEA《2024 全球体验指数》榜单的，一律以 TEA 2024 精确值统一口径。</p>
    <div class="stats">
      <span class="stat">71 案例</span>
      <span class="stat">%d 例有单园年度客流</span>
      <span class="stat">%d 例有 PPH 实值</span>
    </div>
  </div>
</div>
<div class="wrap">
  <div class="legend">
    客流口径：<span class="chip y">实心＝单园某年年度实值</span><span class="chip o">空心＝累计／预计／估算／集团等</span><span class="chip tea">TEA 2024＝全球旅报/TEA 统一口径</span>
    娱乐值 PPH：<span class="chip psrc">标来源＝实值</span><span class="chip no">未收录</span>
  </div>
  <div class="scroll">
  <table>
    <thead><tr>
      <th class="c-name">案例<small>地点（年份）</small></th>
      <th class="c-vis">客流 / 游客量<small>数值按各页口径</small></th>
      <th class="c-pph">娱乐值 PPH<small>人/小时</small></th>
      <th class="c-desc">关键描述</th>
    </tr></thead>
    <tbody>
""" % (n_annual, n_pph) + body + """
    </tbody>
  </table>
  </div>
  <div class="foot">
    <b>口径说明：</b>「客流」列优先放单园年度实值——实心=单园某年实值，其中 TEA 2024 为《2024 全球体验指数》统一口径（全球旅报 2025-12 发布），已覆盖并校准案例页旧年份数（如迪士尼海洋、海洋王国、乐天、海昌由 2023/空白升为 2024，好莱坞影城宿主数按 TEA 修正）；空心含累计、预计/估算、集团或宿主园（云顶为 GENM 集团、银河边缘两案为宿主乐园客流）等非单园年度口径。<br>
    <b>娱乐值 PPH：</b>定义＝园区所有游乐设施理论小时载客容量之和（The Park DB 园页 Capacity 字段，见文献页）。除北京环球为本库 PPH 工具校验值外，均取 The Park DB 公开园页实值；「星球大战：银河边缘」两案为宿主乐园口径（迪士尼乐园 / 好莱坞影城）。多数国内新园及森泊、玛雅系列水乐园 The Park DB 尚未收录，暂无公开可溯源值，留空不估。两列互不换算——客流看热度，PPH 看产能，正好可对比「产能 vs 热度」找选题。
  </div>
</div>
<div class="footer">
  <p>张走走的 案例研究 &amp; 工具集 · <a href="https://github.com/joanna2joanna/casestudy" style="color:#8B3A4A;">GitHub</a> 托管 · 客流年份口径以各案例页原文为准</p>
</div>
</body>
</html>
"""
open(os.path.normpath(os.path.join(_dir,'../../overview.html')),'w',encoding='utf-8').write(doc)
print("已生成 overview.html，字节数:", len(doc))
