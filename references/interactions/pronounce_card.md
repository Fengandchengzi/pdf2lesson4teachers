# 双速发音卡（phonics_practice, vocab_card）

**用途**：单词/发音练习 — 大图+大字+两个速度的发音按钮（正常速/慢速）。

## HTML

```html
<div class="pronounce-card">
  <img class="pronounce-img" src="images/img_lake.jpg" alt="lake">
  <div class="pronounce-word">lake</div>
  <div class="pronounce-phonetic">/leɪk/</div>
  <div class="pronounce-btns">
    <button class="tts-btn normal" onclick="play('lake')">🔊 Normal</button>
    <button class="tts-btn slow" onclick="play('lake_slow')">🐢 Slow</button>
  </div>
  <div class="pronounce-sentence" onclick="play('lake_sentence')">
    🔊 I swim in the <strong>lake</strong>.
  </div>
</div>
```

## CSS

```css
.pronounce-card {
  text-align: center; padding: 40px; max-width: 600px; width: 100%;
}
.pronounce-img {
  width: 280px; height: 200px; object-fit: cover; border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15); margin-bottom: 20px;
}
.pronounce-word {
  font-size: 56px; font-weight: 800; color: #2c3e50;
  margin-bottom: 8px; letter-spacing: 4px;
}
.pronounce-phonetic {
  font-size: 24px; color: #7f8c8d; margin-bottom: 20px;
  font-family: serif;
}
.pronounce-btns {
  display: flex; justify-content: center; gap: 16px; margin-bottom: 24px;
}
/* .tts-btn 基础样式来自 theme.md，此处只定义变体 */
.pronounce-sentence {
  font-size: 22px; color: #2c3e50; padding: 16px;
  background: #F8F9FA; border-radius: 12px; cursor: pointer;
  transition: background 0.2s;
}
.pronounce-sentence:hover { background: #EAF2F8; }
.pronounce-sentence strong {
  color: #E74C3C; font-size: 24px;
}
```

## JS

无额外 JS — 使用内联 `onclick="play('filename')"` 和 `play('filename_slow')` 即可。

## 注意事项

- TTS 生成时需要为每个词生成两个音频：正常速和慢速
- 慢速音频命名约定：`{word}_slow.mp3`
- 例句中用 `<strong>` 标注目标词，点击例句可播放整句
