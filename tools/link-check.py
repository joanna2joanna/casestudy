#!/usr/bin/env python3
"""link-check.py — 案例研究 HTML 交付前资源可达性验证

用法: python3 tools/link-check.py <slug>/index.html

验证三类资源:
  1. 外部参考链接 — curl 状态码 + 重定向跟随
  2. 地图瓦片     — 源类型匹配 + 中心区域 3×3 抽查
  3. 图片         — src 可达性

输出: 终端彩色报告 + 机器可读 JSON（--json）
"""

import re
import sys
import json
import ssl
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────

TIMEOUT = 12
TILE_ZOOMS = [12, 14]  # 抽查的 zoom 级别
TILE_SAMPLE = 2        # 每个 zoom 取 N×N 瓦片（实际请求 tile_sample²）
MIN_TILE_BYTES = 1024  # 小于此值视为空白瓦片
UA = "link-check/1.0 (case-study validator)"

# tile URL 模板特征 → 源类型
TILE_PATTERNS = {
    "autonavi.com":  "amap",       # 高德
    "arcgisonline.com": "esri",    # ESRI ArcGIS
}

# 反爬虫站点 — 403/429 不视为损坏
ANTI_CRAWL_DOMAINS = [
    "thepaper.cn", "zhihu.com", "weixin.qq.com", "mp.weixin.qq.com",
    "facebook.com", "instagram.com", "twitter.com", "x.com",
    "douyin.com", "bilibili.com", "xiaohongshu.com",
]


# ── 提取 ──────────────────────────────────────────────

def extract_links(html):
    """提取所有外部参考链接（排除 CDN/字体/内部链接）"""
    hrefs = re.findall(r'href="(https?://[^"]+)"', html)
    refs = []
    infra = []
    for url in hrefs:
        if any(d in url for d in ["fonts.googleapis.com", "fonts.gstatic.com",
                                    "cdn.jsdelivr.net", "unpkg.com",
                                    "joanna2joanna.github.io"]):
            infra.append(url)
        elif any(url.startswith(p) for p in ["mailto:", "tel:", "#"]):
            continue
        else:
            refs.append(url)
    return refs, infra


def extract_images(html):
    """提取所有 <img> 的 src"""
    return re.findall(r'<img[^>]+src="(https?://[^"]+)"', html)


def extract_tiles(html):
    """提取所有 tile layer URL 模板"""
    tiles = []
    for m in re.finditer(r"L\.tileLayer\('(https?://[^']+)'", html):
        tiles.append(m.group(1))
    return tiles


def detect_tile_source(tile_url):
    """根据 URL 模板识别瓦片源类型"""
    for pattern, name in TILE_PATTERNS.items():
        if pattern in tile_url:
            return name
    return "unknown"


def detect_region(html, tile_urls):
    """推断项目区域：china / overseas / unknown"""
    # 有高德瓦片 → 中国
    for u in tile_urls:
        if detect_tile_source(u) == "amap":
            return "china"
    # 模板中标记（中国模板的特征）
    if '高德' in html or 'amap' in html.lower():
        return "china"
    # 有 ESRI 瓦片 → 海外
    for u in tile_urls:
        if detect_tile_source(u) == "esri":
            return "overseas"
    return "unknown"


def get_map_center(html):
    """从 HTML 中提取地图中心坐标"""
    m = re.search(r"\.setView\(\[(\d+\.?\d*),\s*(\d+\.?\d*)\]", html)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(r'center:\s*\[(\d+\.?\d*),\s*(\d+\.?\d*)\]', html)
    if m:
        return float(m.group(1)), float(m.group(2))
    return None


# ── 验证 ──────────────────────────────────────────────

def safe_url(url):
    """将非 ASCII 字符进行百分号编码，避免 urllib 崩溃"""
    parts = urllib.parse.urlsplit(url)
    # 编码路径和 query 中的非 ASCII 部分
    path = urllib.parse.quote(parts.path, safe='/:@!$&\'()*+,;=-._~')
    query = urllib.parse.quote(parts.query, safe='/:@!$&\'()*+,;=-._~')
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, path, query, parts.fragment))


def check_url(url, timeout=TIMEOUT):
    """检查单个 URL。返回 (status_code, final_url, error_message, content_length)"""
    url = safe_url(url)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            content = resp.read()
            return resp.status, resp.url, None, len(content)
    except urllib.error.HTTPError as e:
        return e.code, url, None, 0
    except urllib.error.URLError as e:
        return None, url, str(e.reason), 0
    except Exception as e:
        return None, url, str(e), 0


def classify_link_result(status, url):
    """分类链接验证结果"""
    if status is None:
        return "error"
    if 200 <= status < 400:
        return "ok"
    if status in (404, 410):
        return "dead"
    if status in (403, 429):
        domain = urllib.parse.urlparse(url).netloc
        for ad in ANTI_CRAWL_DOMAINS:
            if ad in domain:
                return "uncertain"
        return "dead"  # 非已知反爬站点的 403 视为损坏
    if status >= 500:
        return "dead"
    return "uncertain"


def sample_tile_urls(tile_url_template, center, zooms, n):
    """给定 tile URL 模板和中心坐标，生成周边 n×n 瓦片 URL"""
    import math
    urls = []
    for z in zooms:
        lat, lng = center
        # lat/lng → tile x/y
        lat_rad = math.radians(lat)
        x = int((lng + 180.0) / 360.0 * (1 << z))
        y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * (1 << z))
        half = n // 2
        for dx in range(-half, half + 1):
            for dy in range(-half, half + 1):
                tx, ty = x + dx, y + dy
                # 处理 subdomain 占位符 {s}
                url = tile_url_template.replace("{s}", "1").replace("{x}", str(tx)).replace("{y}", str(ty)).replace("{z}", str(z))
                urls.append((z, tx, ty, url))
    return urls


# ── 报告 ──────────────────────────────────────────────

def green(s):  return f"\033[92m{s}\033[0m"
def red(s):    return f"\033[91m{s}\033[0m"
def yellow(s): return f"\033[93m{s}\033[0m"
def bold(s):   return f"\033[1m{s}\033[0m"


def report(results, json_mode=False):
    """输出验证报告"""
    if json_mode:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return results.get("has_issues", False)

    # ── 终端报告 ──
    links = results["links"]
    tiles = results["tiles"]
    images = results["images"]
    region = results.get("region", "unknown")

    print()

    # 链接
    total = links["total"]
    n_ok = len(links["ok"])
    n_dead = len(links["dead"])
    n_uncertain = len(links["uncertain"])
    n_error = len(links["error"])
    print(bold(f"🔗 外链验证 ({total} total)"))
    if n_ok:     print(f"   {green('✅')} {n_ok} passed")
    if n_dead:   print(f"   {red('❌')} {n_dead} failed")
    if n_uncertain: print(f"   {yellow('⚠️')}  {n_uncertain} uncertain (possible anti-crawl)")
    if n_error: print(f"   {red('💥')} {n_error} network errors")
    for item in links["dead"] + links["error"]:
        print(f"      {item['url']} → {item.get('status', 'N/A')} {item.get('error', '')}")
    for item in links["uncertain"]:
        print(f"      {item['url']} → {item.get('status', 'N/A')} (需人工确认)")
    if total == 0:
        print(f"   ⏭️  No external links to check")

    # 地图瓦片
    print()
    print(bold("🗺️  地图瓦片"))
    if tiles["sources"]:
        for src in tiles["sources"]:
            stype = src["type"]
            match_icon = {"amap_china": "✅", "esri_overseas": "✅",
                          "amap_overseas": "⚠️", "esri_china": "⚠️",
                          "unknown_any": "⚠️"}.get(f"{stype}_{region}", "⚠️")
            print(f"   {match_icon} 源: {stype} (区域: {region}) — {src['url'][:80]}...")
            if src["samples"]["total"] > 0:
                total_s = src["samples"]["total"]
                ok_s = src["samples"]["ok"]
                thin_s = src["samples"]["thin"]
                dead_s = src["samples"]["dead"]
                parts = []
                if ok_s: parts.append(green(f"{ok_s} ok"))
                if thin_s: parts.append(yellow(f"{thin_s} thin (<1KB)"))
                if dead_s: parts.append(red(f"{dead_s} unreachable"))
                print(f"      抽查 {total_s} tiles: {', '.join(parts)}")
                if src["samples"]["details"]:
                    for d in src["samples"]["details"]:
                        print(f"      z={d['z']} x={d['x']} y={d['y']}: "
                              f"HTTP {d['status']} {d['size']}B {d.get('note','')}")
            if stype == "esri" and region == "china":
                print(f"      {yellow('⚠️')} 国内项目使用 ESRI 瓦片——中国地区可能无覆盖或偏移")
            if stype == "amap" and region == "overseas":
                print(f"      {yellow('⚠️')} 海外项目使用高德瓦片——海外无覆盖")
    else:
        print(f"   ⏭️  No tile layers found")

    # 图片
    print()
    print(bold(f"🖼️  图片 ({images['total']} total)"))
    if images["ok"]:
        print(f"   {green('✅')} {images['ok']} loaded")
    if images["dead"]:
        print(f"   {red('❌')} {images['dead']} failed")
        for item in images["details"]:
            if item["status"] not in (200, None) or item.get("error"):
                print(f"      {item['url']} → {item.get('status', 'N/A')}")
    if images["total"] == 0:
        print(f"   ⏭️  No images to check")

    # ── 总结 ──
    print()
    has_issues = bool(n_dead) or bool(n_error) or bool(tiles.get("warnings")) or bool(images["dead"])
    if has_issues:
        print(red(bold("📊 存在问题，修复后再部署")))
    else:
        print(green(bold("📊 全部通过，可以部署")))

    return has_issues


# ── 主流程 ──────────────────────────────────────────

def check_html(filepath):
    html = Path(filepath).read_text(encoding="utf-8")

    ref_links, infra_links = extract_links(html)
    img_urls = extract_images(html)
    tile_urls = extract_tiles(html)
    region = detect_region(html, tile_urls)
    center = get_map_center(html) or (0, 0)

    results = {
        "file": filepath,
        "region": region,
        "links": {"total": 0, "ok": [], "dead": [], "uncertain": [], "error": [], "infra_skipped": len(infra_links)},
        "tiles": {"sources": [], "warnings": []},
        "images": {"total": 0, "ok": 0, "dead": 0, "details": []},
        "has_issues": False,
    }

    # ── 验证链接 ──
    seen = set()
    for url in ref_links:
        if url in seen:
            continue
        seen.add(url)
        status, final_url, error, _ = check_url(url)
        category = classify_link_result(status, url)
        entry = {"url": url, "status": status, "final_url": final_url}
        if error:
            entry["error"] = error
        results["links"][category].append(entry)
    results["links"]["total"] = len(seen)

    # ── 验证瓦片 ──
    for tpl in tile_urls:
        stype = detect_tile_source(tpl)
        src_result = {"url": tpl, "type": stype, "samples": {"total": 0, "ok": 0, "thin": 0, "dead": 0, "details": []}}

        # 区域匹配警告
        if stype == "esri" and region == "china":
            results["tiles"]["warnings"].append(f"国内项目使用 ESRI 瓦片，可能无覆盖或坐标系偏移")
        if stype == "amap" and region == "overseas":
            results["tiles"]["warnings"].append(f"海外项目使用高德瓦片，海外无覆盖")

        # 抽查瓦片（仅当有中心坐标时）
        if center != (0, 0):
            sample_urls = sample_tile_urls(tpl, center, TILE_ZOOMS, TILE_SAMPLE)
            for z, tx, ty, url in sample_urls:
                status, _, error, size = check_url(url)
                src_result["samples"]["total"] += 1
                detail = {"z": z, "x": tx, "y": ty, "url": url, "status": status, "size": size}
                if status and 200 <= status < 300:
                    if size < MIN_TILE_BYTES:
                        src_result["samples"]["thin"] += 1
                        detail["note"] = "空白瓦片？"
                        src_result["samples"]["details"].append(detail)
                    else:
                        src_result["samples"]["ok"] += 1
                else:
                    src_result["samples"]["dead"] += 1
                    if error:
                        detail["error"] = error
                    src_result["samples"]["details"].append(detail)
        results["tiles"]["sources"].append(src_result)

    # ── 验证图片 ──
    for url in img_urls:
        results["images"]["total"] += 1
        status, _, error, size = check_url(url)
        entry = {"url": url, "status": status, "size": size}
        if error:
            entry["error"] = error
        results["images"]["details"].append(entry)
        if status and 200 <= status < 300:
            results["images"]["ok"] += 1
        else:
            results["images"]["dead"] += 1

    # ── 汇总 ──
    has_issues = bool(
        results["links"]["dead"] or
        results["links"]["error"] or
        results["tiles"]["warnings"] or
        results["images"]["dead"] or
        any(s["samples"]["thin"] > s["samples"]["total"] * 0.5 for s in results["tiles"]["sources"])
    )
    results["has_issues"] = has_issues

    return results


def main():
    json_mode = "--json" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if not args:
        print("用法: python3 tools/link-check.py <slug>/index.html [--json]", file=sys.stderr)
        sys.exit(1)

    filepath = args[0]
    if not Path(filepath).exists():
        print(f"错误: 文件不存在 — {filepath}", file=sys.stderr)
        sys.exit(1)

    results = check_html(filepath)
    has_issues = report(results, json_mode=json_mode)
    sys.exit(1 if has_issues else 0)


if __name__ == "__main__":
    main()
