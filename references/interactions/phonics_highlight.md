# 字母高亮（phonics_discover, phonics_rule）

**用途**：Phonics 规则展示 — 高亮目标字母/字母组合，点击触发发音对比。

## HTML

```html
<div class="phonics-container">
  <h2 class="phonics-title">Find the pattern!</h2>

  <div class="phonics-words">
    <div class="phonics-word" onclick="play('lake')">
      l<span class="phonics-highlight">a</span>k<span class="phonics-highlight">e</span>
    </div>
    <div class="phonics-word" onclick="play('gate')">
      g<span class="phonics-highlight">a</span>t<span class="phonics-highlight">e</span>
    </div>
    <div class="phonics-word" onclick="play('cake')">
      c<span class="phonics-highlight">a</span>k<span class="phonics-highlight">e</span>
    </div>
    <div class="phonics-word" onclick="play('rake')">
      r<span class="phonics-highlight">a</span>k<span class="phonics-highlight">e</span>
    </div>
  </div>

  <!-- 规则公式 -->
  <div class="phonics-rule">
    <span class="rule-part">a</span> + consonant + <span class="rule-part">e</span>
    = long <span class="rule-sound">/eɪ/</span>
  </div>

  <!-- 对比区 -->
  <div class="phonics-compare">
    <div class="compare-item" onclick="play('can')">
      <span class="compare-label">Short a</span>
      c<span class="phonics-short">a</span>n
    </div>
    <div class="compare-arrow">→</div>
    <div class="compare-item" onclick="play('cane')">
      <span class="compare-label">Long a</span>
      c<span class="phonics-highlight">a</span>n<span class="phonics-highlight">e</span>
    </div>
  </div>
</div>
```

## CSS

```css
.phonics-container {
  text-align: center; padding: 40px; max-width: 700px; width: 100%;
}
.phonics-title {
  font-size: 32px; color: #2c3e50; margin-bottom: 30px;
}
.phonics-words {
  display: flex; justify-content: center; gap: 24px; flex-wrap: wrap;
  margin-bottom: 30px;
}
.phonics-word {
  font-size: 48px; font-weight: 700; color: #2c3e50;
  padding: 16px 28px; background: white; border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1); cursor: pointer;
  transition: transform 0.2s; letter-spacing: 4px;
}
.phonics-word:hover { transform: scale(1.05); }
.phonics-highlight {
  color: #E74C3C; font-weight: 800;
  text-decoration: underline; text-decoration-thickness: 3px;
  animation: phonics-glow 1.5s ease-in-out infinite alternate;
}
@keyframes phonics-glow {
  from { text-shadow: 0 0 4px rgba(231,76,60,0.3); }
  to { text-shadow: 0 0 12px rgba(231,76,60,0.6); }
}
.phonics-short {
  color: #3498DB; font-weight: 800;
}
.phonics-rule {
  font-size: 28px; color: #7f8c8d; margin: 24px 0;
  padding: 16px; background: #FEF9E7; border-radius: 12px;
}
.rule-part {
  color: #E74C3C; font-weight: 800; font-size: 32px;
}
.rule-sound {
  color: #27AE60; font-weight: 800; font-size: 32px;
}
.phonics-compare {
  display: flex; align-items: center; justify-content: center;
  gap: 20px; margin-top: 24px;
}
.compare-item {
  font-size: 40px; font-weight: 700; color: #2c3e50;
  padding: 16px 24px; background: white; border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1); cursor: pointer;
  letter-spacing: 3px;
}
.compare-item:hover { transform: scale(1.05); }
.compare-label {
  display: block; font-size: 14px; color: #95a5a6; font-weight: 400;
  margin-bottom: 4px; letter-spacing: 0;
}
.compare-arrow {
  font-size: 32px; color: #BDC3C7;
}
```

## JS

无额外 JS — 使用内联 `onclick="play('word')"` 即可。高亮通过 CSS `.phonics-highlight` class 实现。

## 注意事项

- `phonics-glow` 动画使用 `alternate` 方向，不使用 `forwards`
- 字母高亮用 `<span class="phonics-highlight">` 包裹目标字母
- 对比区展示 short vs long 发音差异，帮助学生发现规则
