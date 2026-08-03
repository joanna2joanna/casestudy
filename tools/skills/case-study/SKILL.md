---
name: case-study
description: 文旅项目案例研究。输入项目名称+地理位置，输出单文件HTML报告（12模块）。
---

项目根目录 `/Users/joanna/Projects/casestudy`。

## 架构

`shared.css` 是唯一样式源。案例 `<style>` 只写 `:root` 变量 + Hero 渐变 + 独特组件。不重复 shared.css 已有样式。

## 流程

### 0. 模板
- 中国：`tools/template-china.html` → `[slug]/index.html`，高德瓦片
- 海外：`tools/template-overseas.html` → `[slug]/index.html`，ESRI ArcGIS

### 1. 搜索
**模型知识截止 2025 年 5 月，生成前必须 WebSearch 确认最新信息。** 面积、投资额、客流、设计方、特色分区、最新动态。中文用中文关键词，海外中英双语。

**外链优先级**：引用资料时优先选持久性高的源：
- ✅ Wikipedia / Wikimedia（永久 ID 不变，分类极少删除）
- ✅ 项目官网首页及 `/en/`、`/about` 等稳定入口（避免深层路径如 `/r/sanya/y`）
- ✅ 主流新闻媒体存档（BBC、Guardian、澎湃、新华社）
- ✅ 政府/旅游局官网
- ⚠️ 百度百科 — 词条可能被删，优先用 Wikipedia 替代
- ⚠️ 行业博客（blooloop、inpark、trip.com）— 文章可能下线
- ❌ 社交媒体贴（微信、抖音、小红书、YouTube 列表页）— 不做外链；只作为搜索来源

### 2. 坐标

**国内** — `amap_search.py` 返回 GCJ-02（与高德瓦片坐标系一致），**直接用，禁止任何转换**：
```bash
python3 tools/amap_search.py <公园名> <城市> <分区1> <分区2> ...
```
⚠️ 模板 JS 已删除 `wgs84ToGcj02`。如坐标来自 amap_search.py，标注直接定位可正确显示。如有人把转换函数加回来，标注会再次向东南偏移。

**海外** — `nominatim_search.py` 返回 WGS-84：
```bash
python3 tools/nominatim_search.py "Europa-Park Rust"
```
海外模板保留 WGS-84→GCJ-02 转换（仅海外用 ESRI 瓦片时需要）或直接用 WGS-84（ESRI 原生支持）。

**批量验证**：海外案例一次跑完主坐标，统一对比修正，不逐个手动扣。

**内部分区 / 瓦片选择**：主题区无独立 POI，先 Photon 定主坐标再搜 OSM 锚点，无锚点参考卫星图推算。中国城区用高德，偏远地区用 ESRI。禁止 `scrollWheelZoom:true`。

### 3. 生成
复制模板 → 替换 `{{PLACEHOLDER}}` → 只填内容不改框架。

### 4. 自检

**代码规范**（7 项）：
```bash
grep -q 'html.*font-size.*17px' index.html || echo "MISSING 17px!"
grep -B1 '<div id="parkmap"' index.html | grep -q 'reveal' && echo "MAP REVEAL!" || echo "PASS map"
grep -n 'unpkg' index.html && echo "UNPKG!" || echo "PASS CDN"
grep -n 'integrity=' index.html | grep -qi leaflet && echo "SRI!" || echo "PASS SRI"
grep -nE '\bacre\b|\bsq ft\b|\bmile\b|°F' index.html && echo "IMPERIAL!" || echo "PASS units"
grep -nE '>[€$][0-9]' index.html && echo "FOREIGN CURRENCY FIRST!" || echo "PASS currency"
grep -o '<h2>[^<]*</h2>' index.html | sort | uniq -d | grep . && echo "DUP!" || echo "PASS sections"
```
自检失败必须修复再部署。

**资源可达性**：
```bash
python3 tools/link-check.py [slug]/index.html
```
验证外链状态码、地图瓦片覆盖、图片可加载。退出码 1 表示有问题，需修复后才能进入部署。超时/403 多为沙箱网络限制，真实环境重新跑一次确认。

### 5. 部署
```bash
git add [slug]/index.html && git commit -m "新增案例：[项目名]" && git push origin main
```
Push 后更新 `index.html`：卡片 grid 插入新卡片 → 更新 `.count` → commit + push。

## 红线

1. **公制单位**：公顷/m²、米/km、°C。禁止 acre/sq ft/mile/°F
2. **地图无 reveal**：`#parkmap` 及其祖先不得有 `.reveal`
3. **CDN**：`cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/`，禁止 unpkg / SRI
4. **坐标**：国内 amap→GCJ-02 禁止再转换；海外 Photon→WGS-84
5. **货币**：¥ 大字原币小字。日本 JP¥。严禁裸外币在数值首位
6. **标题无「案例研究」**：`<title>`、`<h1>`、footer 不得出现
7. **Hero 不放实景**：仅标题+副标题+4 KPI
8. **禁止外部图库**：不用 Unsplash/Pexels/Pixabay

## 设计规范

- `html { font-size:17px; }`，级差 ≥15%，≤5 级，最小字号 ≥0.78rem
- 标题 Playfair Display，正文 DM Sans，数据 DM Mono
- 数据表 `width:100%`，移动端 ≤2 列改卡片
- 深色仅 Hero + Footer。一项目一主题色
- 滚动渐显：IntersectionObserver + `.reveal`（地图除外）
- SVG 空间示意图：暗色背景 + 功能区矩形 + 水域/地标 + 指北针 + 图例

## 页面结构（12 模块）

1. Hero 2. 项目概览 3. 设计与建设 4. 技术指标总表 5. 空间布局（地图+SVG+分区）
6. 投资与建设时序 7. 运营指标 8. 核心技术指标 9. 配套设施 10. 最新动态 11. 延伸资料库 12. 浮动导航（🏠+↑+busuanzi）

## 品牌研究

品牌运营商（Club Med、Center Parcs 等）：世界级 zoom(2-4)，ESRI 地形底图，标注全球旗舰。
Hero KPI 突出全球规模。增加"中国市场"专节。空间布局→全球分布，技术指标→财务运营指标。
