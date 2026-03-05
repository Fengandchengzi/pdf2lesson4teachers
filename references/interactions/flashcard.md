# 闪卡翻转（flashcard）

**用途**：词汇闪卡游戏 — 展示图片/提示，点击翻转揭示答案并播放 TTS。

## HTML

```html
<div class="flashcard-grid">
  <div class="flashcard" onclick="this.classList.toggle('flipped');play('word1')">
    <div class="flashcard-inner">
      <div class="flashcard-front">
        <img src="images/img_word1.jpg" alt="Word 1">
        <p>What is it?</p>
      </div>
      <div class="flashcard-back">
        <p>broom</p>
        <button class="tts-btn" onclick="event.stopPropagation();play('word1')">🔊</button>
      </div>
    </div>
  </div>
  <!-- 更多 flashcard ... -->
</div>
```

## CSS

```css
.flashcard-grid {
  display: grid; grid-template-columns: repeat(2, 1fr);
  gap: 24px; padding: 20px 80px; max-width: 900px; width: 100%;
}
.flashcard {
  perspective: 800px; height: 240px; cursor: pointer;
}
.flashcard-inner {
  position: relative; width: 100%; height: 100%;
  transition: transform 0.6s; transform-style: preserve-3d;
}
.flashcard.flipped .flashcard-inner { transform: rotateY(180deg); }
.flashcard-front, .flashcard-back {
  position: absolute; inset: 0; backface-visibility: hidden;
  border-radius: 16px; display: flex; flex-direction: column;
  justify-content: center; align-items: center; padding: 16px;
}
.flashcard-front {
  background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.flashcard-front img {
  width: 100%; height: 140px; object-fit: cover; border-radius: 10px;
  margin-bottom: 10px;
}
.flashcard-front p { font-size: 16px; color: #e74c3c; font-weight: 600; }
.flashcard-back {
  background: #27AE60; color: white; transform: rotateY(180deg);
}
.flashcard-back p { font-size: 20px; font-weight: 700; text-align: center; }
.flashcard-back .tts-btn { margin-top: 10px; background: rgba(255,255,255,0.2); color: white; }
```

## JS

无额外 JS — 使用内联 `onclick="this.classList.toggle('flipped')"` 即可。

## 注意事项

- `event.stopPropagation()` 防止背面 TTS 按钮点击时触发翻转
- `backface-visibility: hidden` 是 3D 翻转的关键
- 网格默认 2 列，可按卡片数量调整为 `repeat(3, 1fr)` 或 `repeat(4, 1fr)`
