---
name: skate
description: 大湾区滑板地图——搜索、geocode 并添加新城市滑板场地数据
---

项目路径：`/Users/joanna/Projects/skate`

## 添加场地流程

### 1. 搜索
```bash
WebSearch "[城市名] 滑板场 滑板公园"
WebSearch "[城市名] 滑板培训 室内"
WebSearch "[城市名] 街头滑板 spot"
```

### 2. Geocode（GCJ-02，高德返回即用，不转换）
优先 geocode：
```bash
curl -s "https://restapi.amap.com/v3/geocode/geo?key=932c51e85a92fe6ac1a04008ee818d0a&address=城市+场地名"
```
搜不到用 POI：
```bash
curl -s "https://restapi.amap.com/v3/place/text?key=932c51e85a92fe6ac1a04008ee818d0a&keywords=场地名&city=城市"
```

### 3. 写数据文件 `data/{citypinyin}.js`
```js
const {citypinyin}Spots = [
  // -- 滑板公园 --
  { id: 104, city: 'XX', name: '...', type: 'venue', lat: ..., lng: ..., scale: '', operator: '', price: '', description: '', features: [] },
];
```
- **只加有实际场地可滑的**，规划中/建设中一律不加
- type 三选一：`venue` / `training` / `street`
- ID 按城市分段，同类场地放一起，注释分组

### 4. 接入页面
- `index.html` 加 `<script src="data/{citypinyin}.js"></script>`（在 `spots.js` 前）
- `index.html` 的 `cityCenters` 加坐标
- `data/spots.js` 加 spread

### 5. 验证
```bash
for f in data/*.js; do node --check "$f"; done
```

### 6. 提交
```bash
git add -A && git commit -m "add [城市名] 滑板场地数据" && git push git@github.com:joanna2joanna/skate.git main
```

## 注意事项
- 私人自建场地搜索引擎难找，需用户提供
- 免费场地不写"约XX元/次"，预约制标注清楚
- Git push 用 SSH，HTTPS 443 被阻断
