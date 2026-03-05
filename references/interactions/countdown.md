# 倒计时器（pair_share）

**用途**：分享/讨论环节的倒计时 — 老师点击启动，支持暂停/恢复。

## HTML

```html
<div class="task-content">
  <h2>Tell your partner: What do you like?</h2>
  <button class="tts-btn normal" onclick="play('question')" style="margin:16px auto">🔊 Listen</button>
  <div class="countdown" id="countdown">2:00</div>
  <button class="countdown-btn" id="countdown-btn" onclick="toggleCountdown()">▶ Start Timer</button>
</div>
```

## CSS

```css
.countdown {
  font-size: 64px; font-weight: 800; color: #8E44AD; margin: 20px 0;
  font-variant-numeric: tabular-nums;
}
.countdown-btn {
  padding: 12px 32px; border: none; border-radius: 30px;
  font-size: 18px; cursor: pointer; background: #8E44AD; color: white;
  transition: background 0.2s;
}
.countdown-btn:hover { background: #7D3C98; }
.countdown-btn:disabled { opacity: 0.5; cursor: not-allowed; }
```

## JS

```javascript
var countdownInterval = null;
var countdownSeconds = 120;   // ← 按需修改：60=1分钟，120=2分钟
var countdownRunning = false;

function toggleCountdown() {
  var btn = document.getElementById('countdown-btn');
  if (countdownRunning) {
    clearInterval(countdownInterval);
    countdownRunning = false;
    btn.textContent = '▶ Resume';
  } else {
    countdownRunning = true;
    btn.textContent = '⏸ Pause';
    countdownInterval = setInterval(function() {
      countdownSeconds--;
      if (countdownSeconds <= 0) {
        clearInterval(countdownInterval);
        countdownRunning = false;
        countdownSeconds = 0;
        btn.textContent = '✓ Done';
        btn.disabled = true;
      }
      var m = Math.floor(countdownSeconds / 60);
      var s = countdownSeconds % 60;
      document.getElementById('countdown').textContent = m + ':' + (s < 10 ? '0' : '') + s;
    }, 1000);
  }
}
```

## 注意事项

- `font-variant-numeric: tabular-nums` 保证数字等宽，倒计时不会跳动
- 如果同一 PPT 有多个倒计时 Slide，需要用不同的 id 和变量名区分
