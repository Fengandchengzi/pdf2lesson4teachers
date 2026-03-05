# TTS集成参考 — TTS-1 HD API

## 概述

PPT使用预生成的高质量MP3音频，**不使用 Web Speech API**。
通过 `scripts/generate_tts.py` 脚本批量调用 laozhang.ai TTS-1 HD API 生成音频。

## 三步流程

```
① 收集文本 → 写入 tts_manifest.json
② 调用脚本 → 批量生成 MP3 到 output/audio/
③ HTML引用 → play('filename') 播放本地MP3
```

---

## Step ①：生成TTS清单

在制作HTML-PPT时，收集所有需要发音的文本，写入JSON清单文件。

### 清单格式

```json
[
  {"name": "cover", "text": "Class Rules. Why are class rules important?", "speed": "normal"},
  {"name": "rule1", "text": "Put up your hand", "speed": "normal"},
  {"name": "rule1_slow", "text": "Put up your hand", "speed": "slow"},
  {"name": "chant_full", "text": "We follow rules to help us learn. Put up your hand...", "speed": "normal"},
  {"name": "chant_v1_l1", "text": "We follow rules to help us learn.", "speed": "normal"},
  {"name": "closure1", "text": "Because rules help us learn.", "speed": "normal"}
]
```

### 命名规则

| 类型 | 命名格式 | 示例 |
|------|---------|------|
| 普通语速 | `{功能}` | `rule1`, `eq`, `warmup_q` |
| 慢速版本 | `{功能}_slow` | `rule1_slow`, `word3_slow` |
| Chant逐句 | `chant_v{段}_l{句}` | `chant_v1_l2`, `chant_v2_l4` |
| Chant完整 | `chant_full` | `chant_full` |
| Phonics | `phonics_{词}` | `phonics_lake`, `phonics_cake` |

### 清单保存位置

```
~/pdf2lesson4teachers/output/tts_manifest.json
```

用 Write 工具写入此文件。

---

## Step ②：调用脚本生成音频

### 命令

```bash
export LAOZHANG_API_KEY='用户的API密钥'

python3 ~/.claude/skills/pdf2lesson4teachers/scripts/generate_tts.py \
  --manifest ~/pdf2lesson4teachers/output/tts_manifest.json \
  --output-dir ~/pdf2lesson4teachers/output/audio \
  --voice shimmer \
  --speed 0.9 \
  --slow-speed 0.6
```

### 脚本参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--manifest` | JSON清单文件路径 | (必填) |
| `--output-dir` | 音频输出目录 | `~/pdf2lesson4teachers/output/audio` |
| `--voice` | 语音选择 | `shimmer` |
| `--speed` | 普通语速 (0.25-4.0) | `0.9` |
| `--slow-speed` | 慢速 (0.25-4.0) | `0.6` |
| `--force` | 强制重新生成已存在的文件 | false |
| `--stdin` | 从stdin读取JSON（替代--manifest） | false |

### 可用语音

alloy / echo / fable / onyx / nova / shimmer

### 脚本特性

- 已存在的MP3文件自动跳过（增量生成）
- API Key 通过环境变量 `LAOZHANG_API_KEY` 传入
- 输出目录不存在时自动创建

### API Key获取

需要用户提供 laozhang.ai 的 API Key。如果用户没有设置环境变量，提示：
```
请提供您的 laozhang API Key，用于生成高质量TTS语音。
运行：export LAOZHANG_API_KEY='你的密钥'
```

---

## Step ③：HTML中引用音频

### 播放函数

```javascript
var AUDIO_BASE = 'audio/';
var currentAudio = null;

function play(name) {
  if (currentAudio) { currentAudio.pause(); currentAudio.currentTime = 0; }
  currentAudio = new Audio(AUDIO_BASE + name + '.mp3');
  currentAudio.play();
}
```

### 顺序播放（用于 Read All / Chant Full）

```javascript
function playSequence(names, gap) {
  gap = gap || 300;
  var i = 0;
  function next() {
    if (i >= names.length) return;
    if (currentAudio) { currentAudio.pause(); }
    currentAudio = new Audio(AUDIO_BASE + names[i] + '.mp3');
    currentAudio.onended = function() { i++; setTimeout(next, gap); };
    currentAudio.play();
  }
  next();
}
```

### 按钮调用示例

```html
<!-- 单个播放 -->
<button class="tts-btn" onclick="play('rule1')">🔊 Normal</button>
<button class="tts-btn slow" onclick="play('rule1_slow')">🐢 Slow</button>

<!-- Chant逐句（点击行高亮+播放） -->
<div class="chant-line" onclick="playAndHighlight(this,'chant_v1_l1')">We follow rules...</div>

<!-- 全部播放 -->
<button onclick="playSequence(['rule1','rule2','rule3','rule4','rule5','rule6'])">🔊 Read All</button>
```

---

## TTS按钮出现位置

| Slide类型 | 按钮 |
|-----------|------|
| **vocab_card** | 🔊 Normal + 🐢 Slow |
| **focus_question / fullimage** | 🔊 Listen |
| **phonics_discover / phonics_practice** | 🔊 Normal + 🐢 Slow |
| **chant** | 逐句点击播放 + 🔊 Play Full Chant |
| **review_wall** | 每卡片点击播放 + 🔊 Read All |
| **closure** | 每答案点击播放 |

---

## 输出文件结构

```
~/pdf2lesson4teachers/output/
  {lesson_name}.html          ← PPT主文件
  tts_manifest.json           ← TTS清单
  audio/                      ← 音频目录
    cover.mp3
    rule1.mp3
    rule1_slow.mp3
    chant_full.mp3
    chant_v1_l1.mp3
    ...
```
