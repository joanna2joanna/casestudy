---
name: encard
description: 生成英文口语卡片（小红书版）。列出候选等确认，过了再生成。
---

项目路径：`/Users/joanna/Projects/smalltalk-en`

## 流程

### 1. 选题

列出候选（默认 2 个），说明字面 vs 真正意思 + trap 点，**等用户确认再往下**（用户默认两张全要）。说"换"才换。

**pre-flight（列给用户前必须全过，一条命令批跑）：**
```bash
cd /Users/joanna/Projects/smalltalk-en
for p in "候选A" "候选B"; do
  c=$(echo -n "$p" | wc -c | tr -d ' ')
  dup=$(grep -xFf data/_done.txt <<< "$p")
  echo "$p : ${c}字符 $( [ -z "$dup" ] && echo 'OK' || echo 'DONE-淘汰' )"
done
```
三项全绿（≤17 字符 + 不重复 + trap 自己想完觉得够荒谬）才列给用户。**字符数必须打印出来**，不能凭感觉。

**硬杠（缺一不可）：**

| 硬杠 | 说明 |
|------|------|
| **≤ 17 字符** | 当场数当场淘汰 |
| **不重复** | `grep -xFf data/_done.txt` 一行搞定 |
| **trap 够明显** | 字面越荒谬越好，反差要大。用户说"不够明显"直接换 |
| **现在还在说** | 搜索确认 2025-2026 年主流媒体/社交平台还有日常使用。淘汰信号：只在怀旧文章出现、90年代电影台词感、高中课本感、"蓝瘦香菇"级过时 |
| **出处可查 + 例句含短语** | 优先影视剧/播客/名人采访中的真实对话。**例句的 `en` 字段必须包含目标短语本身**（或其自然变体如 throwing/threw/throws）。Paris Is Burning 解释"shade 是什么"但从不说 "throw shade"——看似有出处，实则例句不合格。禁止自己编对话 |
| **本身是口语** | 想象两人路边聊天会不会自然用到。偏书面（如 bury the hatchet）淘汰 |

**搜索策略：**
1. 搜索前先想：这短语是不是"蓝瘦香菇"级别过时了？是就跳过
2. 每个候选两条搜索并行：
   - currency：`"phrase" 2025 2026 modern usage slang`
   - 含短语的对话：`"throwing phrase" OR "threw phrase" OR "throw phrase" OR "don't phrase" dialogue transcript TV interview`
     → 用动名词/过去式/否定式搜，比搜原形更容易命中真实对话
3. 出处搜完先过滤：搜索结果里有没有角色/受访者**嘴里说出来**的句子？只有"解释这个短语"的教程文章 → 这轮不算找到
4. 泛搜 1 轮 + 定点 1 轮 = 最多 2 轮。两轮找不到含短语的真实对话 → 淘汰
5. 六项全过就列表给用户确认，不中途换题加戏

### 2. 写 JSON

用户确认后写 `data/YYYY-MM-DDa.json` 等，多张并行写入。

**examples 铁律：**
- `source` 必须有搜索验证过的真实出处
- **每句 `en` 必须包含目标短语本身**（或其自然变体 throwing/threw/throws 等）。写 JSON 前逐个目检，搜到 ≠ 说了——Reese Witherspoon 颁奖礼在 shadow，嘴里没说过 "throw shade"
- 保留对话格式，超限缩中文翻译优先
- 字数由 `check-chars.js` 自动挡
- 禁止自己编中文典故来"丰富"释义（如 bury the hatchet → "化干戈为玉帛"是幻觉）

**字数速查（写 JSON 时照着卡，别等 check-chars 报错）：**

> ⚠️ **trap_check 最容易超。** 40 字符很短，善用 `\n` 断行。写完先自数。

| 字段 | 上限 | 字段 | 上限 |
|------|------|------|------|
| phrase_en | 17 | examples[].source | 45 |
| phrase_pron | 45 | examples[].en | 52 |
| meaning_cn | 18 | examples[].cn | 22 |
| trap_x | 40 | | |
| trap_check | 40 | | |

**trap_check 可换行**：JSON 里用 `\n` 断行即可，不占额外字符。

### 3. 生成

每张卡串行（check-chars → gen-html → gen-png → check-layout），多张之间并行。

```bash
cd /Users/joanna/Projects/smalltalk-en

node check-chars.js YYYY-MM-DDa
NODE_PATH=/Users/joanna/.workbuddy/binaries/node/workspace/node_modules node gen-html.js YYYY-MM-DDa < data/YYYY-MM-DDa.json
NODE_PATH=/Users/joanna/.workbuddy/binaries/node/workspace/node_modules node gen-png.js YYYY-MM-DDa
NODE_PATH=/Users/joanna/.workbuddy/binaries/node/workspace/node_modules node check-layout.js YYYY-MM-DDa
```

check-layout 报 2960px 是 Chromium 行为变动，gen-png.js 已有 clip 裁切到 1080×1440，用 `sips -g pixelHeight` 确认实际尺寸即可。

```bash
open /Users/joanna/Projects/smalltalk-en/issues/
```

检查有无 `⋯` 省略号截断，以及 g/p/y 等下降部字母是否被裁（已知 `line-height: 1.2` 不会裁）。**严禁手写 HTML 或改 CSS。**

## 已知问题

- `.phrase-en` 的 `line-height` 原为 1.05，g/p/y 下降部被 `overflow:hidden` 裁切。已改为 1.2。
- 去重原用双系统路径 `grep -ohP`，该路径不在本机，返回空时无报错。已改为 `grep -xFf data/_done.txt`。

## Git Push

```
cd /Users/joanna/Projects/smalltalk-en && git add -A && git commit -m "encard: 短语A + 短语B" && git push
```

## 版式

配色深蓝灰底暖金（`#2E2E48` + `#F0A500`），1080×1440px。短语 >15 字符 → 105px，>22 → 90px。5 级字号：120 / 48 / 34 / 28 / 20。
