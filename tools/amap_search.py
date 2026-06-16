#!/usr/bin/env python3
"""高德POI搜索 — 输入公园名+区域名列表，输出 zonesWgs 坐标数组"""
import urllib.request, urllib.parse, json, sys, math, time

API_KEY = "932c51e85a92fe6ac1a04008ee818d0a"
AMAP_SEARCH = "https://restapi.amap.com/v3/place/text"


def api_get(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  API错误: {e}", file=sys.stderr)
        return None


def search(keywords, city="佛山", offset=10):
    """搜索POI，返回全部结果（限3页）"""
    results = []
    for page in [1, 2, 3]:
        params = {"key": API_KEY, "keywords": keywords, "city": city,
                  "offset": offset, "page": page, "extensions": "all"}
        url = AMAP_SEARCH + "?" + urllib.parse.urlencode(params)
        data = api_get(url)
        if not data or data.get("status") != "1":
            break
        pois = data.get("pois", [])
        if not pois:
            break
        results.extend(pois)
        if page * offset >= int(data.get("count", 0)):
            break
        time.sleep(0.3)
    return results


def dist(lng1, lat1, lng2, lat2):
    dx = (lng1 - lng2) * 102400
    dy = (lat1 - lat2) * 111000
    return math.sqrt(dx*dx + dy*dy)


def find_zone(park_lng, park_lat, park_name, zone_name, city, max_dist=800):
    """搜索区域坐标，过滤距离，选最佳匹配"""
    clean = zone_name.split("·")[0].split("（")[0].strip()
    short = park_name[:4]

    # 唯一关键词: 公园全名 + 区域名
    kw = f"{park_name} {clean}"
    rs = search(kw, city, offset=10)
    if not rs:
        # 降级: 只用区域名
        rs = search(clean, city, offset=10)

    if not rs:
        return None

    best = None
    best_score = -1

    for r in rs:
        name = r.get("name", "")
        addr = r.get("address", "")
        loc_str = r.get("location", "")
        if not loc_str:
            continue
        lng, lat = [float(x) for x in loc_str.split(",")]
        d = dist(park_lng, park_lat, lng, lat)
        if d > max_dist:
            continue

        # 评分: 名称匹配 + 距离
        score = 0
        if short in name:
            score += 3
        if short in addr:
            score += 2
        # 检查区域关键词是否出现在名称或地址中
        for part in [clean, clean[:2]]:  # 全名和前2字
            if part in name:
                score += 4
            if part in addr:
                score += 2
        score += (max_dist - d) / max_dist * 2

        if score > best_score:
            best_score = score
            best = ([lng, lat], name, d)

    return best


def main():
    if len(sys.argv) < 3:
        print("用法: python3 amap_search.py <公园名> <城市> <区域1> <区域2> ...")
        print("示例: python3 amap_search.py 长鹿旅游休博园 佛山 尖叫岛 童话动物王国 长鹿度假村")
        sys.exit(1)

    park = sys.argv[1]
    city = sys.argv[2]
    zones = sys.argv[3:]

    print(f"公园: {park} | 城市: {city}")
    print(f"区域: {', '.join(zones)}\n")

    # 找公园主POI
    park_pois = search(park, city, offset=3)
    if not park_pois:
        print("❌ 未找到公园POI")
        return
    park_loc = park_pois[0]["location"]
    park_lng, park_lat = [float(x) for x in park_loc.split(",")]
    print(f"公园主POI: {park_pois[0]['name']} ({park_lng:.6f}, {park_lat:.6f})")

    # 逐区域搜索
    colors = ["#E53935", "#FF8F00", "#9C27B0", "#0088B0",
              "#4CAF50", "#8BC34A", "#FFC107", "#FF5722",
              "#2196F3", "#795548"]
    results = []
    for i, zone in enumerate(zones):
        found = find_zone(park_lng, park_lat, park, zone, city)
        if found:
            (lng, lat), matched, d = found
            print(f"  ✓ {zone}: ({lng:.6f}, {lat:.6f}) ← {matched} ({d:.0f}m)")
            results.append({
                "name": zone, "lng": round(lng, 6), "lat": round(lat, 6),
                "color": colors[i % len(colors)]
            })
        else:
            print(f"  ✗ {zone}: 无可信POI，使用公园中心")
            results.append({
                "name": zone, "lng": round(park_lng, 6), "lat": round(park_lat, 6),
                "color": colors[i % len(colors)]
            })
        time.sleep(0.3)

    print(f"\n{'='*60}")
    print("// 高德API返回 GCJ-02 坐标，直接用于高德瓦片，禁止再次转换")
    print("var zonesGcj02 = [")
    for i, z in enumerate(results):
        comma = "," if i < len(results) - 1 else ""
        print(f"  {{ name: '{z['name']}', lng: {z['lng']}, lat: {z['lat']}, color: '{z['color']}' }}{comma}")
    print("];")
    print(f"\n// map center:")
    print(f"map.setView([{park_lat:.4f}, {park_lng:.4f}], 16);")


if __name__ == "__main__":
    main()
