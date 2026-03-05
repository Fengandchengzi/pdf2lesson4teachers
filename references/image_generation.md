# 图片获取参考

本文档覆盖 Step 4 中所有图片获取方式：textbook AI 生成、photo 搜索/AI 生成。

---

## 一、Textbook 类型图片（AI 生成）

### 定位

textbook 类型标注"此图内容来源于教材"，但**不直接截取教材原图**（截图质量低），而是根据 desc 描述用 AI 生成同内容的高质量图片，附带教材截图作为风格参考。

### 流程

```
1. 读取大纲中 type=textbook 的条目
2. 从 desc 字段获取图片内容描述（如"学生举手等待回答问题"）
3. 调用 scripts/generate_images.py：
   - --desc: 大纲 desc 字段
   - --usage: 大纲 usage 字段（决定尺寸）
   - --reference: input/ 中的教材截图（风格参考）
   - --style-dna: 视觉 DNA 风格定调句
4. 生成图片保存到 output/images/
```

### 脚本调用

```bash
# textbook 类型：AI 生成同内容图片，附带教材截图风格参考
python3 ~/.claude/skills/pdf2lesson4teachers/scripts/generate_images.py \
  --id img_textbook_cover \
  --desc "student raising hand waiting to answer question" \
  --usage "封面背景" \
  --reference ~/pdf2lesson4teachers/input/U1P1.jpg \
  --style-dna "Children's textbook cartoon illustration, bright saturated colors, clean black outlines, cute rounded shapes."
```

### 与 photo 类型的区别

| | textbook | photo |
|---|----------|-------|
| 来源标注 | 内容来自教材 | 通用场景图 |
| 处理方式 | 直接 AI 生成 | 先搜索，搜不到再 AI 生成 |
| 风格要求 | 必须附带 --reference 教材截图 | 推荐附带 |

---

## 二、Photo 无版权照片搜索下载

### 流程

```
1. 读取大纲中 type=photo 的条目
2. 用 desc 字段作为搜索关键词（英文），WebFetch 搜索 Unsplash 或 Pexels
3. 从搜索结果中选择最匹配的图片，下载保存到 output/images/
4. 文件命名 = 条目的 id 字段（如 img_hand_up.jpg）
```

### 搜索方式

使用 WebFetch 访问 Unsplash 搜索页面：

```
https://unsplash.com/s/photos/{搜索词}
```

搜索词 = 大纲 desc 字段中的英文关键词，空格用连字符连接。

**示例**：
- desc: `"student raising hand in classroom"` → 搜索 `student-raising-hand-classroom`
- desc: `"children waiting in line taking turns"` → 搜索 `children-waiting-in-line`

### 下载保存

从搜索结果中找到合适图片的 URL 后，用 Bash curl 下载：

```bash
curl -L -o ~/pdf2lesson4teachers/output/images/img_hand_up.jpg "图片URL"
```

### 注意事项

- 优先选择**简洁、主体突出、背景干净**的图片，适合课堂投影
- 搜不到合适图片时，直接跳过，后续由 AI 生图补充
- 同一 id 的图片只下载一次（大纲中复用的条目 desc 标注为"复用"）

---

## 三、AI 生图

### 定位

- **textbook 类型**：主要方案，直接用 AI 生成同内容高质量图片
- **photo 类型**：备选方案，当 Unsplash/Pexels 搜不到合适图片时调用

## API 信息

- **模型**: `gemini-3-pro-image-preview` (Nano Banana Pro)
- **Endpoint**: `https://api.laozhang.ai/v1/chat/completions`（OpenAI 兼容）
- **认证**: `Authorization: Bearer $LAOZHANG_API_KEY`（与 TTS 共用同一个 key）
- **费用**: $0.05/次

## 调用方式

### 文生图（纯文字 → 图片）

```bash
curl https://api.laozhang.ai/v1/chat/completions \
  -H "Authorization: Bearer $LAOZHANG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3-pro-image-preview",
    "messages": [{"role": "user", "content": "Generate an image: a yellow cleaning sponge on a white background, real photo style, clean and simple"}]
  }'
```

### 图片编辑（教材原图 + 指令 → 新图片）

```bash
curl https://api.laozhang.ai/v1/chat/completions \
  -H "Authorization: Bearer $LAOZHANG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3-pro-image-preview",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "text", "text": "Remove all text from this image, keep only the illustration"},
        {"type": "image_url", "image_url": {"url": "https://..."}}
      ]
    }]
  }'
```

## 返回值解析与保存

API 返回标准 chat completion 格式，图片以 data URI 嵌在 `content` 字符串中：

```
content: "![image](data:image/jpeg;base64,/9j/4AAQSkZ...)"
```

**提取并保存为文件**（Python）：

```python
import base64, re, json

# 从 API response 中提取
content = response["choices"][0]["message"]["content"]
match = re.search(r'data:image/(\\w+);base64,(.+?)\\)', content)
if match:
    fmt = match.group(1)        # jpeg / png
    b64_data = match.group(2)
    with open(f"output/images/{image_id}.{fmt}", "wb") as f:
        f.write(base64.b64decode(b64_data))
```

## 图片输出目录

与 TTS 音频目录平级：

```
output/
├── audio/          ← TTS MP3
├── images/         ← 图片文件
│   ├── img_hand_up.jpg
│   ├── img_take_turn.jpg
│   └── ...
├── tts_manifest.json
└── lesson.html     ← PPT 中用相对路径引用: <img src="images/img_hand_up.jpg">
```

文件命名 = 大纲 images 条目的 `id` 字段（如 `img_hand_up.jpg`）。

## usage → 尺寸映射

大纲中 images 的 `usage` 字段决定图片尺寸，在 prompt 中指定：

| usage | 尺寸要求 | prompt 追加 |
|-------|---------|------------|
| 词汇主图 / 规则主图 | 1:1 正方形 | `square format, 1:1 aspect ratio` |
| 全屏背景图 | 16:9 宽屏 | `wide format, 16:9 aspect ratio` |
| 网格缩略图 | 1:1 正方形 | 复用词汇主图，不重新生成 |
| 情景图 | 4:3 横版 | `landscape format, 4:3 aspect ratio` |
| 标题装饰 | — | emoji 类型，不走 AI 生图 |
| 封面背景 | 16:9 宽屏 | `wide format, 16:9 aspect ratio` |

## 视觉 DNA 分析（图片获取前必做）

在获取 photo 类型图片之前，Claude 先分析教材截图的视觉风格，提取"视觉 DNA"：

```
Claude 读取 input/ 中的教材截图 → 分析以下 7 个维度 → 输出风格定调句
```

| 维度 | 看什么 |
|------|--------|
| 插画风格 | 扁平/3D/手绘/水彩/矢量/摄影/混搭 |
| 角色设计 | 头身比、五官简化度、标志特征 |
| 色彩体系 | 主色、辅色、饱和度 |
| 线条特征 | 粗细、颜色、均匀/手绘感 |
| 构图习惯 | 人物占比、背景复杂度、留白 |
| 材质纹理 | 纯色块/渐变/水彩/笔触 |
| 文化表征 | 种族、场景文化 |

**输出**：一段风格定调句，同一课件所有 AI 生图共用。

**示例**（分析某教材后）：
```
Children's textbook cartoon illustration, bright saturated colors,
clean black outlines, cute rounded character shapes with 3-head
proportions, soft gradient shading, warm color palette (yellows,
pinks, light blues). Asian elementary school setting.
```

## Prompt 模板

使用视觉 DNA 的风格定调句替代固定模板，同时附带教材截图作为参考图：

```
Generate an image: {desc字段内容}.
{视觉DNA风格定调句}
NOT photorealistic. No text in the image.
Format: {根据usage映射的尺寸要求}
```

**无教材截图时**（降级）使用默认风格：
```
Style: bright, clean, child-friendly illustration suitable for elementary school ESL classroom.
```

**示例**（有视觉 DNA）：
```
Generate an image: student raising hand in classroom.
Children's textbook cartoon illustration, bright saturated colors,
clean black outlines, cute rounded character shapes. Asian school setting.
NOT photorealistic. No text in the image.
Format: square format, 1:1 aspect ratio
```

**关键原则**（借鉴 lesson-image-prompter）：
1. 结构交给参考图 — 不要用文字过度描述形状/位置
2. prompt 只管：风格定调 + 物品名 + 色彩材质 + 格式
3. 同批图共用风格定调句，保持风格一致

## 使用场景

| 场景 | 说明 |
|------|------|
| 词汇图搜不到 | 生僻词汇在 Unsplash 找不到合适照片 |
| 需要特定风格 | 教材风格统一的卡通插画 |
| textbook 类型 | 教材相关内容，AI 生成同内容高质量图 |
| 场景图定制 | 需要特定教学场景（如教室、操场） |
| 用户不满意 | 用户查看图片后要求替换 |

---

## 用户确认流程

所有图片直接存到 `output/images/`，全部完成后**一次性**请用户确认：

```
① textbook AI 生成 → 保存到 output/images/
② photo 搜索下载 / AI 生图 → 保存到 output/images/
③ 全部完成后，告知用户绝对路径，请用户查看：
   "所有图片已保存到 /Users/xxx/pdf2lesson4teachers/output/images/，请查看后告诉我是否满意。"
      ↓
   用户满意 → 进入 Step 4.2 TTS
   用户不满意 → "哪张图片不满意？有什么要求？"
      ↓
   收集反馈（图片 id + 修改要求）
      ↓
   调用 generate_images.py → 生成到 output/images_preview/
      ↓
   告知用户预览图绝对路径，请用户查看
      ↓
   满意 → 调用 generate_images.py --confirm → 覆盖到 output/images/
   不满意 → 再次收集反馈 → 重新生成
      ↓
   询问："现在对所有图片都满意吗？"
   → 全部满意 → 进入 Step 4.2 TTS
   → 还有不满意的 → 继续逐张替换
```

**关键原则**：
- 所有图片直接存 `output/images/`，不做预览中转
- 全部完成后**只确认一次**，给用户绝对路径方便查看
- 只有 AI 替换不满意的图片时才用 `images_preview/` 预览目录
- 每次只替换一张，循环直到用户全部满意

## 脚本调用方式

脚本路径：`~/.claude/skills/pdf2lesson4teachers/scripts/generate_images.py`

每次只替换一张图片，流程：生成预览 → 用户查看 → 满意则确认覆盖。

### 1. 生成预览图

```bash
export LAOZHANG_API_KEY='用户API密钥'

# 基础用法：从大纲条目自动拼 prompt
python3 ~/.claude/skills/pdf2lesson4teachers/scripts/generate_images.py \
  --id img_hand_up \
  --desc "student raising hand in classroom" \
  --usage "规则主图"

# 推荐用法：附带教材截图作为风格参考 + 视觉DNA风格定调
python3 ~/.claude/skills/pdf2lesson4teachers/scripts/generate_images.py \
  --id img_hand_up \
  --desc "student raising hand in classroom" \
  --usage "规则主图" \
  --reference ~/pdf2lesson4teachers/input/U1P1.jpg \
  --style-dna "Children's textbook cartoon illustration, bright saturated colors, clean black outlines, cute rounded shapes."

# 加用户反馈（最高优先级，覆盖风格DNA和默认风格）
python3 ~/.claude/skills/pdf2lesson4teachers/scripts/generate_images.py \
  --id img_hand_up \
  --desc "student raising hand in classroom" \
  --usage "规则主图" \
  --reference ~/pdf2lesson4teachers/input/U1P1.jpg \
  --feedback "要真实照片风格，不要卡通，亚洲小学生"

# 完全自定义 prompt（跳过模板）
python3 ~/.claude/skills/pdf2lesson4teachers/scripts/generate_images.py \
  --id img_hand_up \
  --prompt "A real photo of an Asian elementary student raising hand in a bright classroom"
```

**风格优先级**：用户反馈 > 视觉DNA > 默认风格模板

生成结果保存在 `output/images_preview/`，不影响原图。

### 2. 确认覆盖

用户查看预览图满意后：

```bash
python3 ~/.claude/skills/pdf2lesson4teachers/scripts/generate_images.py \
  --confirm --confirm-id img_hand_up
```

将预览图覆盖到 `output/images/`。
