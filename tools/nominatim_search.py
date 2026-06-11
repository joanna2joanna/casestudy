#!/usr/bin/env python3
"""Photon POI搜索 — 输入地点名+区域列表，输出海外模板 areas 数组（WGS-84）

Photon 基于 OpenStreetMap 数据，全球覆盖，免费，无需 API Key。
https://photon.komoot.io/
"""
import urllib.request, urllib.parse, json, sys, math, time

PHOTON = "https://photon.komoot.io/api/"
UA = "casestudy-script/1.0 (joanna@example.com)"
TIMEOUT = 20


def api_get(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read()
            return json.loads(body)
    except Exception as e:
        print(f"  API 错误: {e}", file=sys.stderr)
        return None


def search(q, limit=5):
    """Photon 搜索，返回 GeoJSON features"""
    params = {"q": q, "limit": limit}
    url = PHOTON + "?" + urllib.parse.urlencode(params)
    data = api_get(url)
    if not data:
        return []
    return data.get("features", [])


def dist(lng1, lat1, lng2, lat2):
    dx = (lng1 - lng2) * 102400
    dy = (lat1 - lat2) * 111000
    return math.sqrt(dx*dx + dy*dy)


def find_zone(park_lng, park_lat, park_name, zone_name, max_dist=5000):
    """搜索区域坐标，过滤距离，选最佳匹配"""
    clean = zone_name.split("·")[0].split("（")[0].strip()

    # 组合关键词
    kw = f"{park_name} {clean}"
    features = search(kw, limit=5)
    if not features:
        features = search(clean, limit=5)

    if not features:
        return None

    best = None
    best_score = -1

    for f in features:
        props = f.get("properties", {})
        geom = f.get("geometry", {})
        coords = geom.get("coordinates")
        if not coords or len(coords) < 2:
            continue

        lng, lat = coords[0], coords[1]
        d = dist(park_lng, park_lat, lng, lat)
        if d > max_dist:
            continue

        name = props.get("name", "")
        osm_key = props.get("osm_key", "")
        osm_value = props.get("osm_value", "")

        score = 0
        if osm_key in ("tourism", "leisure") and osm_value in (
            "theme_park", "attraction", "water_park", "hotel", "resort", "zoo", "park", "museum", "garden"
        ):
            score += 5
        if clean.lower() in (name or "").lower():
            score += 4
        # 偏向有 name 的结果
        if name:
            score += 2
        score += (max_dist - d) / max_dist * 2

        if score > best_score:
            best_score = score
            best = ([lng, lat], name or str(props.get("city", "") + " " + props.get("country", "")), d)

    return best


def main():
    if len(sys.argv) < 2:
        print("用法: python3 nominatim_search.py <地点名> [区域1 区域2 ...]")
        print()
        print("海外案例 (Photon / OSM):")
        print("  python3 nominatim_search.py 'Europa-Park Rust' 德国 意大利 法国 西班牙")
        print("  python3 nominatim_search.py 'Tokyo DisneySea' 地中海港湾 美国海滨 神秘岛")
        print()
        print("只查主POI (不传区域):")
        print("  python3 nominatim_search.py 'Europa-Park Rust'")
        print()
        print("注意: 限速 ~1 req/s")
        sys.exit(1)

    place = sys.argv[1]
    zones = sys.argv[2:]

    if not zones:
        features = search(place, limit=1)
        if features:
            f = features[0]
            coords = f["geometry"]["coordinates"]
            props = f["properties"]
            print(f"// {place}")
            print(f"// center: [{coords[1]:.6f}, {coords[0]:.6f}] zoom ~15")
            print(f"// name: {props.get('name', 'N/A')}")
            print(f"// city: {props.get('city', '')}, country: {props.get('country', '')}")
        else:
            print(f" 未找到: {place}")
        return

    print(f"地点: {place}")
    print(f"区域: {', '.join(zones)}")
    print()

    # 查主POI
    features = search(place, limit=3)
    if not features:
        print(" 未找到主POI")
        return

    best = features[0]
    coords = best["geometry"]["coordinates"]
    park_lng, park_lat = coords[0], coords[1]
    props = best["properties"]
    print(f"主POI: {props.get('name', place)}")
    print(f"坐标: ({park_lat:.6f}, {park_lng:.6f})")
    print()

    colors = ["#E53935", "#FF8F00", "#9C27B0", "#0088B0",
              "#4CAF50", "#8BC34A", "#FFC107", "#FF5722",
              "#2196F3", "#795548"]

    results = []
    for i, zone in enumerate(zones):
        time.sleep(1.1)
        park_short = best["properties"].get("name", "") or place.split(",")[0].strip()
        found = find_zone(park_lng, park_lat, park_short, zone, max_dist=5000)
        if found:
            (lng, lat), matched, d = found
            print(f"    {zone}: ({lat:.6f}, {lng:.6f})  {d:.0f}m  [{matched}]")
            results.append({
                "name": zone, "lat": round(lat, 6), "lng": round(lng, 6),
                "color": colors[i % len(colors)]
            })
        else:
            print(f"  x {zone}: 无可信POI，使用公园中心")
            results.append({
                "name": zone, "lat": round(park_lat, 6), "lng": round(park_lng, 6),
                "color": colors[i % len(colors)]
            })

    print()
    print("=" * 60)
    print("// areas 数组 (WGS-84), 直接贴到海外模板:")
    print("const areas = [")
    for i, a in enumerate(results):
        comma = "," if i < len(results) - 1 else ""
        print(f"  {{ name: '{a['name']}', lat: {a['lat']}, lng: {a['lng']}, color: '{a['color']}', textColor: '#fff' }}{comma}")
    print("];")
    print()
    print(f"// map center:")
    print(f"center: [{park_lat:.4f}, {park_lng:.4f}],")
    print(f"zoom: 15")


if __name__ == "__main__":
    main()
