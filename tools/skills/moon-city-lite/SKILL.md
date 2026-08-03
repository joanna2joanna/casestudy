---
name: moon-city-lite
description: 月球科普系列「张走走想在月球盖座城」波普小卡片版——每期两个知识点+一条粉框趣闻
---

项目路径：`/Users/joanna/Projects/moon-city`
模板：`template-v2.html`
**所有命令必须 `cd` 到项目目录执行**。

## 结构（8 板块）

```
渐变顶条（四段撞色：黄/粉/青/黄）
品牌条（黄底黑字+白框+粉投影）
系列标签（青，纯文字无 emoji，如「引力 · 01」）
标题（黄 100px+双层粉阴影）
━━━ block ×2（青 ■ 小标题 + 左青竖线正文，恰好三行）
━━━ tidbit（5px 粉框+深青底，无标签，恰好两行）
━━━ 参考文献（24px 灰，居中，≥2 条，≤3 条）
━━━ 免责声明（24px 青，居中）
```

## CSS 基准（不可动）

| 参数 | 值 |
|------|-----|
| 画布 | 1080×1350，overflow hidden |
| body | padding 48px 78px 80px, flex column space-between |
| 标题 | 100px #FFE53B，letter-spacing 5px，双粉 shadow |
| 小标题 | 34px #00E5FF，前青色方块 10px |
| 正文 | 32px #FFFFFF，line-height 1.68，左青竖线 3px + 22px padding |
| 粉框 | 5px #FF5E8A，底色 #102530，box-shadow 6px 6px 0 |
| 加粗 | #FFE53B，font-weight 800 |
| ref | 24px #8899AA，居中 |
| disclaimer | 24px #00E5FF，居中 |

## 配色

| 色值 | 用途 |
|------|------|
| `#0B121C` | 底色 |
| `#FFE53B` | 标题、加粗、品牌底 |
| `#FF5E8A` | 粉框、标题阴影 |
| `#00E5FF` | 系列标签、小标题、方块、竖线、免责 |
| `#FFFFFF` | 正文 |
| `#8899AA` | 参考文献 |
| `#102530` | 粉框底色 |

## 字数

| 模块 | 字数 | 行数 |
|------|------|------|
| 标题 | ≤9 字（数字按视觉宽度），含「月」 | — |
| block ×2 | 各 65–85 字（**初稿靶位 70-76**，留 2-5 字空间。80+ 大概率 4 行） | 恰好 3 行 |
| tidbit | 45–50 字（**初稿靶位 45-48**，48+ 大概率 3 行，超 52 必 3 行） | 恰好 2 行 |
| **正文总计** | **~180–220** | — |

## 系列规划

六大步，全部偶数篇，每天两篇：

| 步 | 系列 | 篇数 |
|----|------|------|
| ① 认识脚下 | 引力 4 / 地质 4 / 温差 2 | 10 |
| ② 到达月面 | 着陆 4 / 轨道 4 | 8 |
| ③ 对抗环境 | 月尘 4 / 辐射 4 / 真空 2 | 10 |
| ④ 获取资源 | 水 4 / 氧气 4 / 能源 4 | 12 |
| ⑤ 动手建造 | 建材 4 / 施工 4 / 选址 4 | 12 |
| ⑥ 住下来过 | 生活系列 | 待定 |

## 工作流

1. **选题**：按系列收尾需要提 2-4 个，附带每篇与已有选题的概念边界检查。**仅此步需用户确认**
2. 选题确认后全自动：核实数据 → 写 HTML → **初稿自查** → 去 AI 味 → **三连检查**（计数+行数+高度一跑出）→ 截图 → 更新 README
3. **初稿自查**：写 HTML 后立刻自检每篇 block 字数，超过 80 字当场缩到 70-76（不等到三连报错才返工）。tidbit 超过 50 字当场缩到 45-48
4. **行数优先**：block 3 行 / tidbit 2 行是硬指标。字数通过不代表行数对——75 字也可能 4 行（视觉宽字符多），以渲染行数为准
5. 多篇批量时选题一次确认，随后全部并行走完，最终一次性汇总

## Git Push

```bash
cd /Users/joanna/Projects/moon-city && git add -A && git commit -m "moon-city #N-M：标题A + 标题B" && git push
```

push 一次不通则告知用户「commit 已存本地，网络恢复后手动 push」，不反复重试。

项目已配置 GitHub Pages，push 后自动部署到 https://joanna2joanna.github.io/moon-city/ 。

---

## 自检点

### 选题自检（提出选题前）

- □ 篇数符合作品集收尾需求（2-4 篇）？
- □ 不重复 README 已有选题？
- □ 各篇概念彼此独立，无大篇幅重叠？
- □ 标题 ≤9 字且含「月」？

### 成稿自检（写 HTML 后、三连前）

- □ 去 AI 味六项手动过完？
- □ 改字眼没引入红线词？（「要命」「死」等直白情绪字眼，见下方语气与措辞）
- □ 无句首标点、句尾左括号？
- □ 无孤字行？
- □ 各模块行数初判在范围内？（block 3 / tidbit 2）

### 交付自检（三连通过后、截图后）

- □ 三连全部通过（计数 + 行数 + scrollHeight ≤ 1350）？
- □ README 已更新？
- □ PNG 已生成？

## 红线

- 画布 1080×1350px，overflow: hidden，scrollHeight > 1350 必须删内容（优先缩边距行高，仍不够再裁文字）
- 标题 ≤9 字（数字按视觉宽度算），含「月」，口语化优先
- 正文第三人称客观科普，不出现「我」「我们」
- 无句首标点、句尾左括号、孤字行
- 同一事物表述全文统一，不混用近义词
- 参考文献真实可查，≥2 条且 ≤3 条
- CSS 不动（以模板 `template-v2.html` 为准）
- 免责声明独立 `<div class="disclaimer">`，ref 之后、`</body>` 之前，不可塞进 ref 末尾
- 零 emoji（全卡包括系列标签均不含 emoji）
- 旧 `moon-city` skill 不动

## 语气与措辞

- 不用「咋」——用「怎」或「怎么」
- 不用直白情绪字眼（如「死」→ 用「终结」「结束」等中性表达）
- 不用「么」替代「怎么」
- 句式不加「的」可省略时不加，撑不满行时可适当用助词拉长
- 避免「怎么」「什么」类疑问词

## 数据核实

月球科学仍在快速推进，很多"常识"是过时结论或单一研究的一家之言。
生成前必须过以下关卡，不能盲信搜索结果，更不能盲信模型记忆。

### 核实流程（不可跳过）

1. **正面搜**：每个关键数字和因果陈述至少搜两个独立信源。
   信源优先级：NASA NSSDC / 同行评审期刊 / 机构白皮书 > 知名科普媒体 > 维基百科。
   不取自媒体、微信公众号、知乎、小红书。

2. **反面问**：正面搜完必须反向搜索——
   "XX 有争议吗""XX 被推翻了吗""XX 的例外情况"。
   如果反面搜索结果指向不同结论，必须在正文中体现不确定性。

3. **交叉验证**：同一事实至少两个独立信源的数字一致才可落笔。
   不一致时列出双方来源和年份，选最新或共识度最高的，参考文献如实标注。

4. **官方溯源**：引用 NASA、ESA、CNSA 等机构数据时，找到原始发布页而非二手转载。
   论文引用必须可查 DOI，不引用预印本或非同行评审来源。

5. **术语自检**：写完逐词过——每个专业术语自己能否用一句话解释清楚？
   解释不清的术语不写。不为了看起来专业而生造或堆砌术语缩写。

6. **删减红线**：去 AI 味、缩字数时，删的是修辞和冗余句式，不是事实和数据。
   数字、因果逻辑、限定词（约/大约/目前认为）不可删。删完必须回读确认事实完整。
   **删减不伤可读性**：「运力贵铜过重」「Kapton做绝缘」这类电报体比 AI 腔更难读，宁多两字不砍成断句。

7. **争议标注**：有活跃学术争议的结论，正文加限定词，不在科普里当定论写。

8. **没有来源的数字不落笔**

### 核实时效

每次核实完成后，在 HTML 注释中标注核实日期和信源访问 URL：

```html
<!-- 数据核实于 2026-07-10，信源：NASA NSSDC / Williams 2024 -->
```

同一批数据超过一天（24h）未使用，再次落笔前必须重新搜索确认。
时效性强的选题（正在进行的任务、最新发现、政策变动）必须当天重新核实。

### 典型陷阱（警惕）

- 搜索结果第一条可能是过时的 NASA 新闻稿，翻到第二页
- 中文科普号常把"假说"写成"定论"，查到原始论文才算数
- LLM 倾向于给确定答案，即使数据本身不确定——反向问才能逼出边界
- 数字互相印证不等于正确——可能是同一错误源头被反复引用
- 去 AI 味删字时容易顺手删掉限定词（"约""大约""目前认为"），补回来
- 术语不要凭空造——如果中文没有通用译名，保留英文原文，不要硬翻

## 去 AI 味

**≤4 篇：手动，>4 篇：走 skill 双扫。** 手动更快且不引入红线词。

写 HTML 后、三连前执行。

### 手动去味（≤4 篇，改字眼不改事实）

**1. 二元对比** — 「不是……而是……」「不是……是……」删前半句，直接说后半。

**2. 概括腔** — 「堪称」「可谓」「硬通货」「刚需」「奢侈品」换具体说法，不替读者下结论。

**3. 金句收尾** — 末尾不拔高。平实收束，不喊口号。

**4. 破折号** — 全文 ≤1 个。多出来的换逗号或分号。

**5. 句长打散** — 连续三句差不多长，打散一句。读出声判断最准。

**6. 查红线词** — 「要命」「死」→ 中性表达（「终结」「结束」）。

### 自动去味（>4 篇）

提取正文纯文本 → humanizer-zh → shuorenhua（scene: public-writing, level: standard, scope: structural）→ 回写 HTML。回写后逐条过以上六项。

## 孤字行检查

渲染后逐段检查：每个 block 和 tidbit 的最后一行不得只有 1 个字符（中文字、标点或数字）。若出现孤字行，调整前文措辞使最后一行至少 3–4 字，或把孤字挤入上一行。

## 高度收紧策略（当 scrollHeight 超标时，按优先级依次应用）

1. 缩 block margin（flex space-between 下用 gap 替代）
2. 缩行高：`.block .text { line-height: 1.58; }`（原 1.68）
3. 缩内边距：`.tidbit { padding: 24px 44px; }`（原 32px）
4. 缩底部 padding（原 80px）
5. 仍不够再裁文字

## 命令速查

```bash
cd /Users/joanna/Projects/moon-city

# 三连检查（计数+渲染行数+scrollHeight，一跑出）
NODE_PATH=/Users/joanna/.workbuddy/binaries/node/workspace/node_modules \
  node -e "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.setViewportSize({width:1080,height:1350});await p.goto('file://'+process.cwd()+'/issues/moon-city-NN.html');const info=await p.evaluate(()=>{const texts=document.body.querySelectorAll('.block .text, .tidbit .txt');return Array.from(texts).map((el,i)=>{const h=el.getBoundingClientRect().height;const lh=parseFloat(getComputedStyle(el).lineHeight);return {el:i,type:el.closest('.block')?'block':'tidbit',lines:Math.round(h/lh),chars:el.textContent.length};});});const sh=await p.evaluate(()=>document.body.scrollHeight);console.log('行数+字数:',JSON.stringify(info));console.log('scrollHeight:',sh);await b.close();})();"

# 截图（已内置去导航符号）
NODE_PATH=/Users/joanna/.workbuddy/binaries/node/workspace/node_modules \
  node -e "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.setViewportSize({width:1080,height:1350});await p.goto('file://'+process.cwd()+'/issues/moon-city-NN.html');await p.evaluate(()=>{const el=document.querySelector('.nav-fixed');if(el)el.remove();});await p.screenshot({path:'issues/moon-city-NN.png'});await b.close();})();"

# 超标调试：打印每个元素的 bottom 坐标
NODE_PATH=/Users/joanna/.workbuddy/binaries/node/workspace/node_modules \
  node -e "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.setViewportSize({width:1080,height:1350});await p.goto('file://'+process.cwd()+'/issues/moon-city-NN.html');const sh=await p.evaluate(()=>document.body.scrollHeight);const positions=await p.evaluate(()=>{return Array.from(document.body.querySelectorAll('body > *')).map(e=>({cls:e.className,bottom:e.getBoundingClientRect().bottom}));});console.log('scrollHeight:',sh);console.log(JSON.stringify(positions,null,2));await b.close();})();"

# 单独计数（不需要渲染时用）
python3 count_chars_v2.py issues/moon-city-NN.html
```

## 文件创建

**新增 HTML 文件用 bash heredoc，不要用 Write 工具**。Write 要求文件已被 Read（即已存在于 git），全新文件会报错。

```bash
cd /Users/joanna/Projects/moon-city
cat > issues/moon-city-NN.html << 'ENDOFFILE'
...完整 HTML...
ENDOFFILE
```

已有文件的修改仍用 Edit 工具。

## 制图提示词

用户说「出图/提示词/制图」时，直接出完整提示词，不分节点不等确认。

**输出前第一步：重读制图宪章。** 打开 memory `moon-city-graphic-constitution` 刷新波普美漫质感、三色域分配、七模块模板。以下为补充规范，与宪章冲突时以宪章为准。

提示词写完直接保存在聊天里逐张列出（用户可复制），同时用 heredoc 保存到对应 `moon-city-NN-prompt.txt` 文件，最后 add+commit+push。

### 画面感铁律

提示词是写给 AI 生图工具的——描述的是**画面长什么样**，不是代码怎么排。禁止出现：
- CSS 参数：px、色号（#FFE53B）、letter-spacing、padding、flex
- HTML 结构词：block、tidbit、div、class
- 排版术语：三行矩形、左竖线缩进、行距

改**用自然语言描述视觉效果**：「七个巨大粗黄字」「一道青色细线沿左边缘」「字距偏松」「粉红色粗边框」「右下角影子偏出去」。

### 全系列统一版式

所有提示词必须版式一致。固定区域如下，仅视觉层每张不同：

| 区域 | 位置 | 内容 | 说法 |
|------|------|------|------|
| 画幅声明 | 每张开头第一句 | 画幅 1080×1350，竖版 4:5。画面铺满，不额外加框或分割线 | 每张重复 |
| 顶部撞色细线 | 画面最上缘 | 黄、粉、青、黄四截等分极细色带，横跨全宽 | 每张重复 |
| 品牌签 | 撞色线下居中 | 黄底黑字小横条「张走走想在月球盖座城」，字克制极小，外勾白细线框，右下微微粉影 | 每张重复 |
| 系列标签 | 品牌签下居中 | 青色小字「系列 · 编号」 | 每张替换 |
| 标题 | 系列标签下居中 | 七个巨大粗字，工业黄，黑色粗描边，字距偏松，右下叠双层亮洋红投影（一层实一层虚）。全画面最抢眼 | 每张替换标题文字 |
| **视觉层** | 标题下，画面核心区 | **三层叠合——每张不同，是唯一差异化区域** | 每张创新 |
| 工程概览 | 左下板块 | 左栏文字，≤150 字 | 每张替换 |
| 数据来源 | 右下板块 | 右栏文字，2-4 条真实文献，带「参考文献：」标签 | 每张替换 |
| 免责声明 | 底部居中 | 青色微小字「*本文为公开信息整理笔记，非严肃学术科普。*」 | 每张重复 |
| 色彩分配 | 末尾 | 钴蓝/工业黄/亮洋红三色域 + 粗黑描边 + 波普粗网点 + 禁暖色 | 每张替换 |

### 出图自检（发完前逐张过）

- □ 每张开头写了「画幅 1080×1350，竖版 4:5」？
- □ 画面铺满、不加外框分割线这句写了？
- □ 品牌签、标题区、底部双栏、免责声明位置各张一致？
- □ 视觉层是否仅此张独有、不跟其他张雷同？
- □ 无 px、色号、CSS 术语？
- □ 无「品牌胶囊」四字？
- □ 免责声明写了完整原文？
- □ 参考文献带了「参考文献：」标签？
- □ 色彩分配写了三色域 + 网点 + 禁暖色？
- □ 全卡零 emoji？

### 术语禁语

- 「品牌胶囊」→「黄底黑字横条「张走走想在月球盖座城」」
- 色号、px、letter-spacing 等一切 CSS 参数
- block / tidbit / div / padding / flex 等一切 HTML 结构词

## 经验教训

### 字数与行数
- count_chars_v2.py 把数字拆成单字符，标题 ≤9 字**以视觉宽度为准**
- block 初稿靶位 70-76 字，超 80 大概率 4 行
- tidbit 初稿靶位 45-48 字，48+ 大概率 3 行
- **count_chars 通过不代表行数对**，必须三连同跑（计数+行数+高度一跑出）
- block 4 行时优先缩**视觉宽字符**（「粒子」→「子」），删一字比加半句更有效
- 去 AI 味会缩 2-5 字，Block2 最易掉出下限，写完自查

### 内容质量
- 标题数字后必须带单位（「差三百」→「差三百度」）
- 两篇 block 概念必须独立，不能同概念换壳
- 标题避免误导（如「引力坑坑洼洼」——引力场不均匀 ≠ 引力砸坑）
- 去 AI 味时警惕引入红线词（「死」「要命」）
- 删减不伤可读性，宁多两字不砍成电报体

### 制图
- 出图前先读 memory `moon-city-graphic-constitution`，不凭记忆写
- 提示词是画面描述不是 HTML 描述——禁用 px/色号/block/tidbit/padding/flex
- 用自然语言：「七个巨大粗黄字」「粗黑描边」「右下粉影偏出去」
- 禁用「品牌胶囊」→「黄底黑字横条「张走走想在月球盖座城」」
- 免责声明完整原文：「*本文为公开信息整理笔记，非严肃学术科普。*」
- 参考文献必带「参考文献：」标签
- 工程概览中图层标注留在视觉层内，独立文字才独立成段
- 底部双栏固定左右并排，不随视觉层移动
- 标题固定居中偏上，不左飘右移
- 视觉层每层至少 2-3 句具体描述（形状、颜色、质感、空间关系）
- 写完后用 heredoc 保存到 `moon-city-NN-prompt.txt` 并 push

### 工程
- 截图命令已内置 `remove nav-fixed`，不用额外处理
- push 不通一次即停，告知用户「commit 已存本地」，不重试
- 所有命令必须 `cd /Users/joanna/Projects/moon-city` 再执行
