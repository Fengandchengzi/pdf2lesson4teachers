---
name: pdf2lesson4teachers
description: |
  教师课堂PPT设计器：从ESL教材PDF出发，经过教学设计，产出老师可以直接用来上一堂完整课的PPT。
  核心理念：不是把教材搬上屏幕，而是设计一堂课。
  五步流程：教材分析 → 教学目标+教案 → PPT大纲 → PPT制作 → 美化+资源。
  输入：ESL教材PDF页面（可同时接收pdf2lesson的JSON作为辅助参考）
  输出：一堂完整课的HTML-PPT，包含导入、呈现、操练、产出、总结全流程
  触发词：做教师课件、做上课PPT、教案+PPT、帮我备课、做课堂PPT
---

# PDF2Lesson4Teachers v2.0

从ESL教材出发，**设计一堂完整的课**，产出老师可以直接投影使用的课堂PPT。

## 核心理念

```
❌ 旧思路：教材每一页 → 投射到屏幕（无脑搬运）
✅ 新思路：教材内容 → 教学设计 → 课堂PPT（有设计的课）

区别在于：
- 教材P5(词汇) + P6(分类) 可能合并成PPT的一个教学环节
- 教材没有的"导入活动"需要PPT补充
- 教材的"写一写"环节需要PPT提供写作脚手架
- PPT的顺序不一定跟教材页码一致
- 每个Slide都有明确的教学功能（不是"展示第X页"）
```

## SKILL定位

```
┌─────────────────────────────────────────────────────────────┐
│  pdf2lesson                    pdf2lesson4teachers           │
│  (教材→App数据)                 (教材→教师课堂PPT)            │
│                                                              │
│  教材PDF → JSON                教材PDF → 教学设计 → PPT      │
│  服务：App渲染引擎             服务：老师上课投影               │
│  忠于教材结构                   忠于教学设计                   │
│  按页面拆分                     按教学环节组织                 │
│  22种题型模板                   PPT slide类型自由              │
│                                                              │
│  两者可以共存：                                               │
│  - pdf2lesson的JSON可作为参考输入（不强制）                    │
│  - pedagogical_assets 可以复用为教案素材                      │
│  - 但PPT结构独立于JSON结构                                   │
└─────────────────────────────────────────────────────────────┘
```

## 使用场景

| 场景 | 说明 |
|------|------|
| **老师备课** | 拿到教材，需要一份可以直接上课的PPT |
| **新老师** | 不熟悉教学流程，需要完整教案+PPT引导 |
| **Demo课** | 给学校展示完整的一堂课如何上 |
| **教研磨课** | 团队讨论教学设计，需要可视化的课堂流程 |

---

## 五步工作流

```
Step 1: 教材分析
    读教材 → 提取内容、识别教学要素
    ↓
Step 2: 教学设计
    教学目标 → 教案（Lesson Plan）
    ↓
Step 3: PPT大纲
    教案 → 每个Slide的功能、内容、交互方式
    ↓
Step 4: PPT制作
    大纲 → HTML-PPT（可选frontend-design美化 + TTS发音）
    ↓
Step 5: 审核优化
    检查教学完整性、节奏感、视觉质量
```

**重要：Step 2产出教案后需要与用户确认，再进入Step 3。**

---

## Step 1: 教材分析

### 1.1 输入

接受以下任意组合：
- **教材PDF截图**（最常见）
- **pdf2lesson产出的JSON**（可选辅助）
- **用户口头描述**（如"Wonders 3C Week 1 Growing Up"）

### 1.2 提取任务

从教材中识别以下教学要素：

```
=== 教材分析报告 ===

【基本信息】
- 教材：Wonders 3C (McGraw-Hill)
- 单元：How Things Change
- 周次：Week 1 — Growing Up
- 页码范围：P2-P9
- 目标年龄：6-8岁（低年级ESL）

【教学要素清单】
| 要素 | 教材位置 | 内容 |
|------|---------|------|
| Big Idea | P2-3 | How do things change? |
| Essential Question | P4 | How can you help out at home? |
| Weekly Concept | P4 | Growing Up — 厨房场景 |
| Oral Vocabulary | P5 | 8个家务物品 |
| Words & Categories | P6 | 5个婴儿用品 → "帮助宝宝"分类 |
| Phonics | P7 | a_e 长元音 (lake, gate, cake, rake) |
| Words to Know | P9 | 高频词/视觉词 |
| Shared Read | P12-19 | Jake and Dale Help! |

【教材意图分析】
这一周围绕"Growing Up"主题，通过家务和照顾宝宝的场景，
让学生在真实语境中学习相关词汇，同时引入a_e发音规则。
教材的设计意图是：话题激活 → 词汇建构 → 语音规则 → 阅读应用。
```

### 1.3 确定课时范围

一套教材内容通常对应多个课时。需要和用户确认：

```
📋 这些内容建议分成 2-3 个课时：
  课时1: Big Idea + Weekly Concept + Oral Vocabulary (P2-P5)
  课时2: Words & Categories + Phonics + Words to Know (P6-P9)
  课时3: Shared Read (P12-P19)

您想做哪个课时的PPT？还是合并成一个完整课时？
```

---

## Step 2: 教学设计

### 2.1 教学目标

针对选定的课时，写出ABCD格式的教学目标：

```
=== 教学目标 (Teaching Objectives) ===

【知识目标 Knowledge】
1. 学生能识别并说出8个家务相关词汇 (trash bag, broom, sponge, 
   laundry basket, plate & bowl, make the bed, toy box, walk the dog)
2. 学生能识别a_e发音规则，正确朗读lake, gate, cake, rake

【技能目标 Skills】
3. 学生能用 "I can help by ___ing" 句型描述自己在家做的事
4. 学生能听到a_e单词时识别长元音/eɪ/

【情感目标 Affect】
5. 学生乐于分享自己帮助家人的经历
6. 学生对英语学习保持好奇和兴趣
```

### 2.2 教案 (Lesson Plan)

用PPP/ESA等主流教学框架，设计完整课堂流程：

```
=== 教案 (Lesson Plan) ===

课时：40分钟
框架：PPP (Presentation-Practice-Production) + Warm-up/Wrap-up

┌────────────────────────────────────────────────────────┐
│  1. Warm-up 热身导入 (5min)                             │
│     目的：激活背景知识，建立话题联结                       │
│     活动：                                               │
│     - 展示大象家族图片，引出"change"话题                  │
│     - 问学生："你小时候会做什么？现在会做什么？"            │
│     - 引出Essential Question: How can you help at home?  │
│     PPT需要：大图+问题+引导语                            │
├────────────────────────────────────────────────────────┤
│  2. Presentation 呈现 (10min)                           │
│     目的：输入目标词汇                                   │
│     活动：                                               │
│     - 厨房场景图：引导学生描述"谁在做什么"                │
│     - 逐个呈现8个词汇：图片+单词+发音+简单例句            │
│     - 分类游戏：哪些是"清洁"的？哪些是"整理"的？         │
│     PPT需要：场景图+词汇卡+分类活动                      │
├────────────────────────────────────────────────────────┤
│  3. Practice 操练 (12min)                               │
│     目的：巩固词汇+引入发音规则                          │
│     活动：                                               │
│     3a. 词汇操练 (6min)                                 │
│       - 看图说词（闪卡快速反应）                         │
│       - "What's missing?" 遮盖游戏                      │
│     3b. Phonics 发音规则 (6min)                          │
│       - 引入lake：听音→看词→发现规则                     │
│       - 总结a_e规则                                     │
│       - 练习：gate, cake, rake                           │
│       - 挑战：你还知道哪些a_e单词？                      │
│     PPT需要：闪卡+遮盖+发音规则卡+练习                   │
├────────────────────────────────────────────────────────┤
│  4. Production 产出 (8min)                              │
│     目的：真实输出，综合运用                              │
│     活动：                                               │
│     - "I Can Help!" 海报：画出自己在家帮忙的场景          │
│       并写 "I can help by ___ing."                      │
│     - Pair Share：和同桌互相分享                          │
│     PPT需要：示范+句型框架+分享指引                      │
├────────────────────────────────────────────────────────┤
│  5. Wrap-up 总结 (5min)                                 │
│     目的：回顾+预告                                     │
│     活动：                                               │
│     - 快速复习：你今天学了哪些词？                       │
│     - 回到Big Idea：How do things change?                │
│     - 预告下节课：We Can Play!                           │
│     PPT需要：词汇回顾墙+下节课预告                      │
└────────────────────────────────────────────────────────┘
```

### 2.3 ⚠️ 用户确认

```
请确认以上教案：
1. 教学目标是否准确？
2. 活动设计是否合理？时间分配是否OK？
3. 有没有需要增删的环节？
4. 学生水平是否匹配？（需要调难度吗？）

确认后我将生成PPT大纲。
```

---

## Step 3: PPT大纲

教案确认后，将每个教学环节拆解为具体的PPT slides。

### 3.1 Slide规划原则

```
原则1: 每个Slide有且仅有一个教学功能
  ✅ Slide 5: 呈现词汇 "broom" — 图片+单词+发音+例句
  ❌ Slide 5: 呈现全部8个词汇（信息过载）

原则2: Slide之间有过渡逻辑
  ✅ Slide 4→5: "这是什么？" → 揭示"broom" → "用它可以做什么？"
  ❌ Slide 4→5: 词汇A → 词汇B（无过渡，像背单词）

原则3: 练习Slide要有交互
  ✅ 闪卡快速反应：倒计时+图片→学生抢答→揭示答案
  ❌ 静态展示所有答案

原则4: 每个环节有"信号Slide"
  ✅ 环节过渡页："Time to Practice! 🎯" 
  ❌ 直接从呈现跳到练习，学生不知道切换了
```

### 3.2 大纲模板

**大纲模式选择**：生成大纲前，**必须停下来询问用户选择模式，等待用户回复后再继续。禁止默认选择任何模式直接生成大纲。** 使用 AskUserQuestion 工具提问：
- **简易模式**：按下方模板直接生成大纲，省 token，适合快速出稿
- **结构化模式**：读取 `references/outline_format.md`，为每个 Slide 补充结构化的 `images` 和 `tts` 字段，PPT 质量更高但消耗更多 token

```
=== PPT大纲 ===

Slide 1 — 标题页
  类型：cover
  内容：单元标题 + 周次 + 课题
  视觉：教材风格背景+大标题

--- WARM-UP 热身导入 ---

Slide 2 — 话题激活
  类型：fullimage
  内容：大象家族图片 + "Look! Big elephants and baby elephants."
  教师动作：问 "How are they different?"
  TTS：问题朗读

Slide 3 — Essential Question
  类型：focus_question
  内容："How can you help out at home?" + 引导思考气泡
  教师动作：请2-3个学生分享
  TTS：问题朗读

--- PRESENTATION 呈现 ---

Slide 4 — 环节过渡页
  类型：transition
  内容："Let's Learn New Words! 📚"
  视觉：动画渐入

Slide 5 — 场景导入
  类型：scene
  内容：厨房场景 + 热区标注
  教师动作：引导描述 "What are they doing?"
  交互：点击热区弹出词汇+TTS发音

Slide 6-13 — 词汇呈现（每词一页）
  类型：vocab_card
  内容：大图+单词+例句
  教师动作：带读→个别读→齐读
  TTS：单词发音+慢速
  节奏：每词约1分钟

Slide 14 — 词汇分类
  类型：categorize
  内容：8个词分成"打扫清洁"vs"整理收拾"两类
  交互：拖拽/点击分类
  教师动作：请学生说理由

--- PRACTICE 操练 ---

Slide 15 — 环节过渡页
  类型：transition
  内容："Time to Practice! 🎯"

Slide 16 — 闪卡游戏
  类型：flashcard
  内容：快速显示图片→倒计时→揭示单词
  交互：点击翻转

Slide 17 — What's Missing?
  类型：whats_missing
  内容：显示7个词→ 猜缺了哪个
  交互：选择答案

Slide 18 — Phonics导入
  类型：phonics_discover
  内容：lake 图片+单词 → 引导发现a_e规则
  TTS：正常速度+慢速
  教师动作："Look at the red letter. What sound does it make?"

Slide 19 — Phonics规则
  类型：phonics_rule
  内容：a + consonant + e = long /eɪ/ + 对比 can vs cane
  TTS：对比朗读
  视觉：字母动画高亮

Slide 20-22 — Phonics练习
  类型：phonics_practice
  内容：gate / cake / rake 各一页（图+词+发音）
  TTS：每词发音
  教师动作：带读+个别读

Slide 23 — Phonics挑战
  类型：challenge
  内容："Can you think of more a_e words?" + 示例列表
  教师动作：小组讨论→全班分享

--- PRODUCTION 产出 ---

Slide 24 — 环节过渡页
  类型：transition
  内容："Your Turn! ✏️"

Slide 25 — 产出任务
  类型：task_brief
  内容："I Can Help!" 海报制作说明
  句型框架："I can help by ___ing."
  示范：教师示范作品

Slide 26 — Pair Share
  类型：pair_share
  内容：分享规则 + 互评提示
  倒计时：2分钟

--- WRAP-UP 总结 ---

Slide 27 — 词汇回顾
  类型：review_wall
  内容：今天学的所有词汇（网格展示）
  TTS：全部词汇朗读
  教师动作："Let's say them together!"

Slide 28 — 回到Big Idea
  类型：closure
  内容："How do things change?" → 联系本节课
  教师动作：请学生回答

Slide 29 — 预告+结束
  类型：ending
  内容：下节课预告 + "Great job today! ⭐"
```

### 3.3 Slide类型库

PPT中可用的Slide类型（与pdf2lesson的22种模板无关，是PPT的功能类型）：

| Slide类型 | 功能 | 典型内容 | 交互 |
|-----------|------|---------|------|
| **cover** | 封面 | 标题+副标题+教材信息 | — |
| **transition** | 环节过渡 | 大字标题+图标+动画 | — |
| **fullimage** | 全屏图+提问 | 背景图+叠加文字+TTS | 🔊 |
| **focus_question** | 聚焦问题 | 大字问题+思考提示 | 🔊 |
| **scene** | 场景交互 | 背景图+可点击热区 | 模板: `interactions/hotspot.md` |
| **vocab_card** | 单词呈现 | 大图+单词+例句 | 模板: `interactions/pronounce_card.md` |
| **vocab_grid** | 多词总览 | 多卡网格 | 🔊 |
| **categorize** | 分类活动 | 类别标签+可拖放词汇 | 模板: `interactions/drag_drop.md` |
| **flashcard** | 闪卡游戏 | 图片→翻转→单词 | 模板: `interactions/flashcard.md` |
| **whats_missing** | 缺失猜测 | N-1个词+问号 | 模板: `interactions/quiz.md` |
| **phonics_discover** | 发音发现 | 示范词+引导发现规则 | 模板: `interactions/phonics_highlight.md` |
| **phonics_rule** | 规则展示 | 规则公式+对比词 | 模板: `interactions/phonics_highlight.md` |
| **phonics_practice** | 发音练习 | 图+词+发音 | 模板: `interactions/pronounce_card.md` |
| **challenge** | 开放挑战 | 问题+示例+思考 | — |
| **task_brief** | 任务说明 | 任务要求+示范+句型 | — |
| **pair_share** | 分享活动 | 规则+倒计时 | 模板: `interactions/countdown.md` |
| **review_wall** | 复习墙 | 所有词汇网格 | 🔊全部 |
| **closure** | 收束回顾 | 回到核心问题 | 🔊 |
| **ending** | 结束页 | 预告+感谢 | — |

---

## Step 4: PPT制作

**执行顺序强制约束（必须严格按序，禁止跳步或调换）：**

```
4.0 获取 API Key → 4.1 生成图片 → 用户确认图片
    → 4.2 生成 TTS 音频 → 4.3 准备教师备注
    → 4.4 生成 HTML-PPT（引用已就绪的图片和音频）
```

**禁止先生成 HTML 再补图片/音频。** HTML 是最后一步，必须在图片和音频全部就绪后才生成，确保所有资源路径真实有效。

### 4.0 获取 API Key

生成图片和 TTS 都需要 API Key。**在开始 4.1 之前，必须先确认 `LAOZHANG_API_KEY` 环境变量已设置。** 如果未设置，使用 AskUserQuestion 向用户索取，拿到后再继续。

### 4.1 图片获取

完整流程见 `references/image_generation.md`，核心步骤：

```
① 视觉 DNA 分析：读取 input/ 中的教材截图，分析插画风格/色彩/线条等 7 维度
   → 输出一段风格定调句，同一课件所有 AI 生图共用
② 从大纲提取所有 images 条目，按 id 去重
③ 按 type 分类处理，全部直接存到 output/images/：
   - emoji → 直接内联 Unicode，无需获取文件
   - textbook → 直接调用 scripts/generate_images.py（--reference 教材截图 + --style-dna）
     根据 desc 描述 + 教材风格参考，AI 生成同内容高质量图片
   - photo → 用 WebFetch 搜索 Unsplash/Pexels，下载保存
     搜不到时 → 调用 scripts/generate_images.py（附带 --reference 教材截图 + --style-dna 风格定调句）
④ 全部完成后，告知用户 output/images/ 的绝对路径，请用户一次性查看确认
⑤ 不满意 → 逐张替换：收集反馈 → AI 生成预览到 images_preview/
   → 用户查看预览 → 满意则确认覆盖 → 再问"全部满意吗？"→ 循环直到满意
⑥ 全部满意 → 进入 4.2 TTS
```

### 4.2 TTS集成（TTS-1 HD预生成音频）

**不使用 Web Speech** **API**，使用预生成的高质量MP3音频。

详细流程见 `references/tts_integration.md`，核心三步：

```Plain
① 收集PPT中所有发音文本 → 写入 tts_manifest.json
② 调用 scripts/generate_tts.py → 批量生成MP3到 output/audio/
③ HTML中用 play('filename') 播放本地MP3
```

调用命令：

```Bash
export LAOZHANG_API_KEY='用户API密钥'
python3 ~/.claude/skills/pdf2lesson4teachers/scripts/generate_tts.py \
  --manifest ~/pdf2lesson4teachers/output/tts_manifest.json \
  --output-dir ~/pdf2lesson4teachers/output/audio
```

### 4.3 教师备注

每个Slide附带教师备注（不在投影中显示，只在教师面板中可见）：

```
教师备注内容 = 大纲每个Slide的 teacher_note 字段
- 这一页要做什么
- 问什么问题
- 预期学生反应
- 时间建议
- 差异化建议（如果有高/低水平学生）
```

教师面板快捷键：`T` 切换显示，`L` 中英切换

### 4.4 HTML-PPT结构

导航系统（翻页、进度条、教师面板）**必须使用 `references/navigation.md` 中的模板代码**，不要从零编写。该模板已验证前进/后退功能正确。

交互组件**必须使用 `references/interactions/` 下的模板代码**。根据 PPT 大纲中实际用到的 Slide 类型，只读取对应的模板文件（见 3.3 表格"交互"列），不要一次性读取全部。

视觉主题**必须使用 `references/theme.md` 中的 CSS 变量和排版规范**。如需更高视觉质量，可额外调用 `frontend-design` skill 在此基础上升级。

HTML 整体结构：

```
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    字体 <link>（来自 theme.md A 节）
    <style>
      主题 CSS 变量 + 全局重置（来自 theme.md B-F 节）
      + 导航模板 CSS（来自 navigation.md）
      + Slide 类型样式
      + 交互组件样式（来自 interactions/）
    </style>
  </head>
  <body>
    <section class="slide" data-phase="cover" data-teacher-note="...">Slide 1</section>
    <section class="slide" data-phase="warmup" data-teacher-note="...">Slide 2</section>
    ...更多 Slide（大纲每个 Slide 对应一个 section）

    导航按钮 HTML（来自 navigation.md）
    进度条 HTML（来自 navigation.md）
    教师面板 HTML（来自 navigation.md）

    <script>
      导航 IIFE（来自 navigation.md，三段式：声明 → 函数 → init()）
      + TTS play()/playSequence()（来自 navigation.md）
      + 交互组件逻辑（闪卡翻转/倒计时等）
    </script>
  </body>
</html>
```

教师备注通过 `data-teacher-note` 属性写在每个 `<section>` 上，导航 JS 自动读取并显示。

### 4.5 导航增强：环节进度

已集成到 `references/navigation.md` 底部导航区域模板中，无需额外处理：

```
底部区域自上而下：
  ① 分段进度条： [■Warm-up■|■■Presentation■■|■Practice■|■Prod■|■Wrap■]
                  蓝色        绿色             橙色       紫色    红色
  ② 导航按钮：  ‹  8/29  ›

- 进度条按 slide 数量自动分配宽度
- 已到达的段高亮，未到达的段半透明
- data-phase 属性驱动，无需手动配色
```

---

## Step 5: 审核优化

### 5.1 教学完整性检查

```
□ 导入环节是否有效激活了背景知识？
□ 目标词汇是否全部呈现并有练习机会？
□ 发音规则是否有"发现→总结→练习"的完整过程？
□ 是否有产出环节（学生说/写）？
□ 总结是否回扣了Big Idea/Essential Question？
□ 环节过渡是否自然？
```

### 5.2 节奏感检查

```
□ 没有连续超过3个"静态展示"slide？
□ 每5-7个slide有一次互动/活动切换？
□ 过渡页是否过多（不超过5个）？
□ 单词呈现没有变成"背词模式"（要有语境）？
□ 总时长合理（25-45分钟）？
```

### 5.3 视觉质量检查

```
□ 使用了 theme.md 的 CSS 变量（非硬编码颜色）
□ 配色方案已应用
□ 图片真实清晰（非emoji占位）
□ TTS按钮位置合理不遮挡
□ 过渡动画流畅不卡顿
□ 教师面板可隐藏（投影时不显示）
□ 字号在投影下可读（标题≥2rem，正文≥1.2rem）
```

---

## 与 pdf2lesson JSON 的关系

pdf2lesson 的 JSON **可以但不必须**作为输入：

| 场景 | 做法 |
|------|------|
| **有JSON** | 复用词汇列表、发音数据、pedagogical_assets；但PPT结构独立设计 |
| **无JSON** | 直接从PDF截图提取内容，完全独立工作 |
| **JSON + PDF** | 最佳：JSON提供结构化数据，PDF提供视觉参考 |

复用映射：
```
JSON → PPT
─────────────
content.word → vocab_card的单词
content.images → vocab_card的图片线索（搜索无版权图片或AI生图）
questions[].hint → phonics_practice的练习词
pedagogical_assets.lead_in → 教师备注（导入阶段）
pedagogical_assets.process_support → 教师备注（操练阶段）
pedagogical_assets.error_correction → 教师备注（练习阶段）
pedagogical_assets.enrichment → 教师备注（产出阶段）
```

---

## Prompt交互流程示例

```
用户：帮我做Wonders 3C Week 1的上课PPT [上传6张教材截图]

Claude：
  Step 1 → 分析教材，输出分析报告
  → "这些内容建议分2个课时，您想做哪个？"

用户：做第一个课时（P2-P7）

Claude：
  Step 2 → 输出教学目标+教案
  → "请确认教案，有什么需要调整的？"

用户：时间压缩到30分钟，去掉分类活动

Claude：
  Step 3 → 输出调整后的PPT大纲
  → "大纲确认后我开始制作PPT"

用户：OK，做吧

Claude：
  Step 4 → 获取图片+配色（可选frontend-design美化）
         → 制作HTML-PPT（含TTS+交互+教师面板）
  Step 5 → 自查+输出

  → 输出：wonders_3c_w1_lesson1.html
```
