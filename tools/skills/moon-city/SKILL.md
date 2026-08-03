---
name: moon-city
description: 月球科普系列「张走走想在月球盖座城」——微信贴图号，1080×1350px
---

项目路径：`/Users/joanna/Projects/moon-city`
**所有命令必须 `cd` 到项目目录执行**（screenshot.js 和 count_chars.py 用相对路径）。

## 工作流

1. 提出选题（每次两个，不重复 README，贴日常生活），**仅此步需用户确认**
2. 选题确认后全自动：写 HTML（CSS 不动）→ 去AI味自查（见下方「去AI味」节）→ `count_chars.py` 验证 → 截图 → scrollHeight 检查 → 更新 README
3. 多篇批量时选题一次确认，随后全部并行走完，最终一次性汇总，不逐篇确认
4. **初稿写完先自查**：insight 是最常见超标源（目标 65–70），highlight 次之（目标 30–35），两个都偏短了 block 再补——先跑计数，超标再改浪费轮回

## Git Push

确认完成后执行：

```
cd /Users/joanna/Projects/moon-city && git add -A && git commit -m "moon-city #N-M：标题A + 标题B" && git push
```

项目已配置 GitHub Pages，push 后自动部署到 https://joanna2joanna.github.io/moon-city/ 。

## 自检点

三个卡口，每次执行前对自己逐条过，不跳。

### 选题自检（提出选题前）

- □ 给了两个？
- □ 不重复 README 已有选题？
- □ 选题贴日常生活？（读者能想象自己在月球上碰到这件事）
- □ 标题 ≤9 字且含「月球」前缀？

### 成稿自检（去AI味后、count_chars 前）

- □ 去AI味 5 项全扫了？
- □ 改字眼没引入红线词？（「要命」「死」等直白情绪字眼）
- □ 各模块字数目测在范围内？（去AI味最容易让 Block2 偏短，适当多写几字留余量）

### 交付自检（截图后、汇报前）

- □ count_chars 全部通过？
- □ scrollHeight ≤ 1350？
- □ README 已更新？

## 红线

- 画布 1080×1350px，overflow: hidden，scrollHeight > 1350 必须删内容（优先缩边距和行高，仍不够再裁文字）
- 标题 ≤9 字（数字按视觉宽度算，不计入汉字字数，如「2030」不拆成 4 字符），带「月球」前缀，口语化优先，避免「怎么」「什么」
- **count_chars.py 超标时先报用户，不自作主张改标题**——标题修改必须确认
- 正文第三人称客观科普，不出现「我」「我们」
- 无句首标点、句尾左括号、孤字行
- 同一事物表述全文统一，不混用近义词
- 参考文献真实，≤3 条
- CSS 不动（所有参数以模板 `issues/moon-city-48.html` 为准——包含 `.disclaimer` 规则）
- **免责声明**：独立于参考文献之外，用 `<div class="disclaimer">` 包裹 `本文为公开信息整理笔记，非严肃学术科普。`，不可塞进 `.ref` 末尾
  - CSS：`font-size: 18px; color: #6B7D99; margin-top: 14px; line-height: 1.5; text-align: center;`
  - DOM 顺序：`.ref` 之后、`</body>` 之前

## 数据核实

不做伪科普——轻松口吻不妨碍事实靠谱。数字写上去就得站住：

- **模型知识截止 2025 年 5 月，生成前必须 WebSearch 确认最新信息。**
- **时效性信息 → 搜索交叉核对**：计划编号、时间表、政策等会变动的东西，落笔前搜索比对两个以上信源
- **准确性数据 → 模型推敲**：物理常数、化学性质等训练时就学过的，自己推一遍，数字之间能互相印证
- **没有来源的数字不落笔**：核实不过来的细节宁可少写，写了的必须对

## 语气与措辞

- 不用「咋」——用「怎」或「怎么」
- 不用直白情绪字眼（如「死」→ 用「终结」「结束」等中性表达）
- 不用「么」替代「怎么」
- 句式不加「的」可省略时不加，撑不满行时可适当用助词拉长

## 去AI味

写 HTML 后、count_chars 前，扫一遍正文，有则改，不改事实不改结构，只动字眼和句式。

**1. 二元对比** — 「不是……而是……」「不是……是……」删前半句，直接说后半。

> 改前：在太空洗澡不是能不能洗的问题，是洗完花两小时收拾水珠值不值的问题。
> 改后：在太空洗澡，洗完花两小时收拾水珠，多数人选择不洗。

**2. 概括腔** — 「堪称」「可谓」「硬通货」「刚需」「奢侈品」换具体说法，不替读者下结论。

> 改前：堪称鼻塞时代的饮食刚需
> 改后：鼻子越堵越离不开

**3. 金句收尾** — insight 末尾不拔高。「XXX是XXX的产物」「可能比任何XXX都更XXX」回平实收束。

> 改前：可能比任何技术突破都更让人想哭
> 改后：大概比技术突破本身来得更实在

**4. 破折号** — 全文 ≤2 个。多出来的换逗号或分号。

**5. 句长打散** — 扫一眼连续三句差不多长，打散一句。读出声判断最准。

## 结构与字数

3 block + 1 highlight + 1 insight + 免责声明 + 参考文献

| 模块 | 字数 | 说明 |
|------|------|------|
| Block（×3） | 100–150 | 3–4 行 |
| Highlight | 30–35 | 1 行金句 |
| Insight | 65–70 | ≤2 行 |
| **正文总计** | **460–510** | 优先瞄准 480–490 |

## 高度收紧策略（当 scrollHeight 超标时，按优先级依次应用）

注意：`.disclaimer` 为独立元素，约占 35–40px，新增或加回时可能触发溢出。

1. 缩边距：`.block { margin-bottom: 10px; }`（原 12px）——模板已默认 10px
2. 缩行高：`.block .text { line-height: 1.48; }`（原 1.58）——最常见有效手段，不必一步到位，先试 1.53
3. 缩内边距：`.highlight, .insight { padding: 17px 28px; }`（原 18px 28px）
4. 缩底部：`body { padding: 32px 72px 48px; }`（原 56px）
5. 仍不够再裁文字

## 命令速查

```bash
cd /Users/joanna/Projects/moon-city

# 计数
python3 count_chars.py issues/moon-city-NN.html

# 截图
NODE_PATH=/Users/joanna/.workbuddy/binaries/node/workspace/node_modules \
  node screenshot.js issues/moon-city-NN.html issues/moon-city-NN.png

# 高度检查
NODE_PATH=/Users/joanna/.workbuddy/binaries/node/workspace/node_modules \
  node -e "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.setViewportSize({width:1080,height:1350});await p.goto('file://'+process.cwd()+'/issues/moon-city-NN.html');console.log(await p.evaluate(()=>document.body.scrollHeight));await b.close();})();"

# 超标时调试：打印最后一个元素的 bottom 坐标定位溢出源
NODE_PATH=/Users/joanna/.workbuddy/binaries/node/workspace/node_modules \
  node -e "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.setViewportSize({width:1080,height:1350});await p.goto('file://'+process.cwd()+'/issues/moon-city-NN.html');const sh=await p.evaluate(()=>document.body.scrollHeight);const last=await p.evaluate(()=>{const els=document.body.querySelectorAll('*');const e=els[els.length-1];return{tag:e.tagName,bottom:e.getBoundingClientRect().bottom,text:e.textContent?.substring(0,50)}});const bb=await p.evaluate(()=>{const r=document.body.getBoundingClientRect();return{height:r.height}});console.log('scrollHeight:',sh,'lastEl:',JSON.stringify(last),'bodyHeight:',bb.height);await b.close();})();"
```

## 经验教训

- **cd 到项目目录**是所有命令的前提，路径错浪费多轮
- 初稿正文尽量瞄准 **480–490 字**，宁可偏上限回删，不偏下限回补
- 多篇并行写 HTML、并行计数、并行截图、并行高度检查可大幅节省时间
- count_chars.py 把数字拆成单字符（"2030"→4 字），标题≤9 字以视觉宽度为准
- 正文超标可以自己精简，**标题超标必须报用户**
- 标题始终带「月球」前缀，以后不变——不用再问
- 标题字号默认 100px，极少数特例可破例缩小到 90px，但必须确认，下次恢复 100px
- **事实错误必须纠正**：译名、年份、数据等用户记错了要指出，不顺着写
- scrollHeight 超标时优先从边距/行高/内边距下手，裁文字是最后手段
- 免责声明是独立 `.disclaimer` div，不是 `.ref` 的尾行——塞进去会视觉混合，iOS 微信预览尤其明显
- 批量回改（如全部加免责结构）用 Python 字符串替换脚本，一次性处理全系列，不必逐张手改
- **选题始终给两个**，用户确认后两篇都做，并行推进
- **去AI味会缩字数**，Block2 最易掉出下限，改后多写几字留余量，省一轮回补
- **去AI味时警惕引入红线词**：改字眼可能无意间踩中「死」「要命」等直白情绪字眼（"麻烦了"而不是"要命的是"）
- **README 查行用 `tail` 不用 `grep`**：`grep -E "# 68"` 的 `#` 被当作注释符，查不到东西
