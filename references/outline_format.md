# PPT大纲结构化输出格式

## 概述

Step 3 的大纲输出是 Step 4 的直接输入。采用结构化格式，确保 PPT 制作时不丢失信息。

大纲由两部分组成：
```
① 元信息（课时信息、教学目标摘要）
② Slide 列表（每个 slide 的完整描述）
```

---

## 元信息

```
=== 大纲元信息 ===
课题: Growing Up — How can you help at home?
教材: Wonders 3C Week 1 (P2-P7)
课时: 40分钟
总Slide数: 29
环节分布:
  - cover: 1 slide
  - warmup: 2 slides (5min)
  - presentation: 11 slides (12min)
  - practice: 9 slides (13min)
  - production: 3 slides (6min)
  - wrapup: 3 slides (4min)
```

---

## Slide 格式

每个 Slide 必须包含以下字段：

```
Slide {N} — {标题}
  type: {slide类型ID}
  phase: {教学环节}
  content: {展示内容}
  images: [{id, desc, type, usage}, ...]
  tts: [{name, text, speed}, ...]
  interaction: {交互类型，无则写 —}
  teacher_note: {教师动作/提问/预期反应}
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| type | ✅ | 必须使用 Slide类型库 中的类型ID（cover/transition/vocab_card 等） |
| phase | ✅ | cover / warmup / presentation / practice / production / wrapup |
| content | ✅ | 该 slide 展示的具体内容（文字、词汇、题目等） |
| images | ✅ | 图片需求数组，无图片则写 `[]` |
| tts | ✅ | TTS 条目数组，无发音需求则写 `[]` |
| interaction | ✅ | 交互说明：点击翻转 / 拖放分类 / 选择答案 / 倒计时 / — |
| teacher_note | ✅ | 教师在此页做什么、问什么、预期学生反应 |

### images 条目格式

```
images: [
  {id: "img_broom", desc: "broom sweeping floor", type: "photo", usage: "词汇主图"},
  {id: "img_kitchen", desc: "family kitchen scene", type: "photo", usage: "背景图"}
]
```

**图片类型**：

| type | 说明 | 获取方式 |
|------|------|---------|
| `emoji` | Unicode 表情 | 直接内联，无需搜索 |
| `photo` | 无版权照片 | 搜索 Unsplash/Pexels 下载 |
| `textbook` | 教材相关图 | AI 根据 desc 描述生成（教材截图作为风格参考） |

注意：photo 类型优先搜索 Unsplash/Pexels，搜不到时降级为 AI 生图。textbook 类型直接走 AI 生图（附带教材截图作为参考）。AI 生图调用 laozhang.ai 图片生成 API。

**命名规则**：`img_{内容}`，同一图片在多个 slide 中复用时使用相同 id。

### tts 条目格式

```
tts: [
  {name: "word_broom", text: "broom", speed: "normal"},
  {name: "word_broom_slow", text: "broom", speed: "slow"},
  {name: "dialogue_boy", text: "Can I have some water?", speed: "normal", voice: "echo"}
]
```

字段说明：
- `name`/`text`/`speed`：必填
- `voice`：可选，不填则用默认声音（shimmer）。对话场景用不同 voice 区分角色：
  - `shimmer`/`nova`：女性
  - `echo`/`onyx`：男性
  - `alloy`/`fable`：中性

命名规则与 `references/tts_integration.md` 一致。

---

## 完整示例

```
=== 大纲元信息 ===
课题: Growing Up — How can you help at home?
教材: Wonders 3C Week 1 (P2-P7)
课时: 40分钟
总Slide数: 14（仅展示部分示例）
环节分布:
  - cover: 1 slide
  - warmup: 2 slides (5min)
  - presentation: 8 slides (10min)
  - practice: ...
  - production: ...
  - wrapup: ...

=== Slide 列表 ===

Slide 1 — 标题页
  type: cover
  phase: cover
  content: "Unit: How Things Change / Week 1: Growing Up / How can you help out at home?"
  images: []
  tts: [{name: "cover", text: "How Things Change. Growing Up.", speed: "normal"}]
  interaction: —
  teacher_note: 简单介绍今天的话题，不做停留，快速进入

--- WARM-UP ---

Slide 2 — 话题激活
  type: fullimage
  phase: warmup
  content: 大象家族图片 + "Look! Big elephants and baby elephants. How are they different?"
  images: [{id: "img_elephant_family", desc: "elephant mother with baby elephant in savanna", type: "photo", usage: "全屏背景图"}]
  tts: [{name: "warmup_q", text: "Look! Big elephants and baby elephants. How are they different?", speed: "normal"}]
  interaction: —
  teacher_note: 展示图片，给学生10秒观察，然后问 "How are they different?" 接受中文回答

Slide 3 — Essential Question
  type: focus_question
  phase: warmup
  content: "How can you help out at home?" + 思考气泡
  images: []
  tts: [{name: "eq", text: "How can you help out at home?", speed: "normal"}]
  interaction: —
  teacher_note: 请2-3个学生分享，用中文也可以。记录关键词在黑板上

--- PRESENTATION ---

Slide 4 — 环节过渡
  type: transition
  phase: presentation
  content: "Let's Learn New Words! 📚"
  images: [{id: "emoji_books", desc: "📚", type: "emoji", usage: "标题装饰"}]
  tts: [{name: "transition_vocab", text: "Let's Learn New Words!", speed: "normal"}]
  interaction: —
  teacher_note: —

Slide 5 — 词汇: broom
  type: vocab_card
  phase: presentation
  content: 单词 "broom" + 例句 "I use a broom to sweep the floor."
  images: [{id: "img_broom", desc: "broom sweeping floor, household cleaning tool", type: "photo", usage: "词汇主图"}]
  tts: [
    {name: "word_broom", text: "broom", speed: "normal"},
    {name: "word_broom_slow", text: "broom", speed: "slow"},
    {name: "sent_broom", text: "I use a broom to sweep the floor.", speed: "normal"}
  ]
  interaction: 🔊普通 + 🐢慢速
  teacher_note: 带读2遍 → 个别学生读 → 齐读。问 "Do you have a broom at home?"

Slide 6 — 词汇: sponge
  type: vocab_card
  phase: presentation
  content: 单词 "sponge" + 例句 "We clean the table with a sponge."
  images: [{id: "img_sponge", desc: "yellow cleaning sponge", type: "photo", usage: "词汇主图"}]
  tts: [
    {name: "word_sponge", text: "sponge", speed: "normal"},
    {name: "word_sponge_slow", text: "sponge", speed: "slow"},
    {name: "sent_sponge", text: "We clean the table with a sponge.", speed: "normal"}
  ]
  interaction: 🔊普通 + 🐢慢速
  teacher_note: 带读2遍 → 做擦桌子动作 TPR → 齐读

--- PRACTICE ---

Slide 10 — 闪卡游戏
  type: flashcard
  phase: practice
  content: 8个词汇的图片闪卡，点击翻转显示单词
  images: [
    {id: "img_broom", desc: "复用", type: "photo", usage: "闪卡图片面"},
    {id: "img_sponge", desc: "复用", type: "photo", usage: "闪卡图片面"}
  ]
  tts: [
    {name: "word_broom", text: "broom", speed: "normal"},
    {name: "word_sponge", text: "sponge", speed: "normal"}
  ]
  interaction: 点击翻转（图片面 → 单词面）
  teacher_note: 先给3秒看图，学生抢答，再点击翻转验证。节奏要快

--- WRAP-UP ---

Slide 14 — 词汇回顾墙
  type: review_wall
  phase: wrapup
  content: 本课所有词汇网格展示
  images: [
    {id: "img_broom", desc: "复用", type: "photo", usage: "网格缩略图"},
    {id: "img_sponge", desc: "复用", type: "photo", usage: "网格缩略图"},
    {id: "img_trash_bag", desc: "复用", type: "photo", usage: "网格缩略图"}
  ]
  tts: [
    {name: "word_broom", text: "broom", speed: "normal"},
    {name: "word_sponge", text: "sponge", speed: "normal"},
    {name: "word_trash_bag", text: "trash bag", speed: "normal"}
  ]
  interaction: 每卡点击播放 + 🔊 Read All
  teacher_note: "Let's say them together!" 全班齐读一遍，然后用 Read All 播放确认
```

---

## 大纲 → Step 4 的消费方式

| 大纲字段 | Step 4 用途 |
|----------|------------|
| type | 决定 HTML `<section>` 结构和交互组件 |
| phase | 决定 `data-phase` 属性和进度条分色 |
| content | 填充 slide 内容 |
| images | 汇总所有条目 → 按 id 去重 → 按 type 获取图片 |
| tts | 汇总所有条目 → 生成 tts_manifest.json |
| interaction | 决定 JS 交互逻辑（翻转/拖放/倒计时等） |
| teacher_note | 填入教师面板 `<aside class="teacher-panel">` |

### images 提取规则

从所有 Slide 的 images 字段中：
1. 收集全部条目
2. 按 id 去重（同 id 表示复用同一张图，如闪卡复用词汇卡图片）
3. 按 type 分类处理：
   - `emoji`：直接内联 Unicode，无需获取
   - `photo`：搜索 Unsplash/Pexels 下载
   - `textbook`：AI 根据 desc 生成（附带教材截图作为风格参考）
4. 如果 photo 搜不到合适图片，降级为 AI 生图（调用 Nano Banana Pro，模型 `gemini-3-pro-image-preview`，API 详见 `references/image_generation.md`）

### tts_manifest.json 提取规则

从所有 Slide 的 tts 字段中：
1. 收集全部条目
2. 按 name 去重（同名的只保留一条，如 review_wall 复用 vocab_card 的音频）
3. 输出为 `references/tts_integration.md` 中定义的 JSON 格式
