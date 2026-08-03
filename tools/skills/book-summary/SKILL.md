---
name: book-summary
description: 读书摘要——添加新书，创建数据文件、预计算布局、验证结果
---

项目路径：`/Users/joanna/Projects/summary`

## 添加新书流程

### 1. 创建 `books/<书名>/data.json`
格式参考 `books/三体-黑暗森林/data.json` 或 `books/太白金星有点烦/data.json`。

```json
{
  "meta": { "title": "书名", "author": "作者", "summary": "一句话简介" },
  "factions": [{ "name": "阵营名", "color": "#hex" }],
  "characters": [{ "id": "英文ID", "name": "人物名", "role": "角色", "desc": "描述", "color": "#阵营色" }],
  "relationships": [{ "source": "id", "target": "id", "type": "关系" }],
  "xiaohongshuCards": [{ "id": "card-1", "title": "标题", "label": "标签", "icon": "emoji", "theme": "warm|teal|mist", "quote": "引用", "content": ["p1","p2","p3"], "footnote": "" }]
}
```

### 2. 预计算布局
```bash
cd /Users/joanna/Projects/summary && node precompute-layout.js <书名>
```
多次迭代直到上下留白均匀。画布 1100×1400px，PAD=120，4列×4行网格。中文名2-4字，角色10-12个，关系数≈角色数×1.5，小红书卡片4-6张。

### 3. 注册到 `js/app.js`
```js
{ slug: '书名', title: '书名', author: '作者' }
```

### 4. 验证
- 打开 `http://localhost:8080?book=<书名>`
- 检查人物关系图节点均匀、标签不重叠
- 检查小红书卡片内容完整
