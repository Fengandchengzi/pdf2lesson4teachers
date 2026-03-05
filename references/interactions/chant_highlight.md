# 行高亮播放（chant 等）

**用途**：歌谣/韵文逐句跟读 — 点击某行高亮并播放该行音频，其余行取消高亮。

## HTML

```html
<div class="chant-container">
  <div class="chant-line" onclick="highlightAndPlay(this,'chant_line1')">
    <span class="icon">🔊</span> We follow rules to help us learn.
  </div>
  <div class="chant-line" onclick="highlightAndPlay(this,'chant_line2')">
    <span class="icon">🔊</span> Put up your hand and take your turn.
  </div>
  <div class="chant-line" onclick="highlightAndPlay(this,'chant_line3')">
    <span class="icon">🔊</span> We listen, ask and answer.
  </div>
  <div class="chant-line" onclick="highlightAndPlay(this,'chant_line4')">
    <span class="icon">🔊</span> This all makes learning fun.
  </div>
</div>
```

## CSS

```css
.chant-container { padding: 0 80px; max-width: 800px; width: 100%; }
.chant-line {
  padding: 16px 24px; margin: 8px 0; border-radius: 12px;
  font-size: 26px; cursor: pointer; transition: background 0.2s;
  display: flex; align-items: center; gap: 12px; color: #2c3e50;
}
.chant-line:hover { background: rgba(0,0,0,0.05); }
.chant-line.highlight { background: #F39C12; color: white; }
.chant-line .icon { font-size: 20px; }
```

## JS

```javascript
function highlightAndPlay(el, audioName) {
  var container = el.parentElement;
  var lines = container.querySelectorAll('.chant-line');
  lines.forEach(function(l) { l.classList.remove('highlight'); });
  el.classList.add('highlight');
  play(audioName);
}
```

## 注意事项

- 作用域限定在 `parentElement` 内，多个 chant 容器互不干扰
- 可选：添加"全部播放"按钮，用 `playSequence()` 自动逐行高亮
