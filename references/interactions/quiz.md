# 单选题（whats_missing）

**用途**：What's missing / 选择题 — 显示选项按钮，选择后即时反馈对错。

## HTML

```html
<div class="quiz-container">
  <h2 class="quiz-question">Which word is missing?</h2>
  <div class="quiz-context">
    <!-- 已显示的词汇（提供语境） -->
    <span class="quiz-word">broom</span>
    <span class="quiz-word">sponge</span>
    <span class="quiz-word">plate</span>
    <span class="quiz-word quiz-missing">?</span>
  </div>
  <div class="quiz-options" id="quiz1-options">
    <button class="quiz-option" onclick="checkAnswer(this,'quiz1','A',false)">A. cake</button>
    <button class="quiz-option" onclick="checkAnswer(this,'quiz1','B',true)">B. trash bag</button>
    <button class="quiz-option" onclick="checkAnswer(this,'quiz1','C',false)">C. lake</button>
    <button class="quiz-option" onclick="checkAnswer(this,'quiz1','D',false)">D. gate</button>
  </div>
  <div class="quiz-feedback" id="quiz1-feedback"></div>
</div>
```

## CSS

```css
.quiz-container {
  text-align: center; padding: 40px; max-width: 700px; width: 100%;
}
.quiz-question {
  font-size: 32px; color: #2c3e50; margin-bottom: 24px;
}
.quiz-context {
  display: flex; justify-content: center; gap: 16px; flex-wrap: wrap;
  margin-bottom: 32px;
}
.quiz-word {
  padding: 12px 24px; background: #EAF2F8; border-radius: 12px;
  font-size: 22px; color: #2c3e50; font-weight: 600;
}
.quiz-missing {
  background: #F39C12; color: white; font-size: 28px; min-width: 80px;
}
.quiz-options {
  display: grid; grid-template-columns: repeat(2, 1fr);
  gap: 16px; max-width: 500px; margin: 0 auto;
}
.quiz-option {
  padding: 16px 24px; border: 3px solid #BDC3C7; border-radius: 12px;
  background: white; font-size: 20px; cursor: pointer;
  transition: all 0.2s; text-align: left;
}
.quiz-option:hover { border-color: #3498DB; background: #EBF5FB; }
.quiz-option.correct {
  border-color: #27AE60; background: #E8F8F5; color: #27AE60; font-weight: 700;
}
.quiz-option.wrong {
  border-color: #E74C3C; background: #FDEDEC; color: #E74C3C;
}
.quiz-option:disabled { cursor: not-allowed; opacity: 0.6; }
.quiz-feedback {
  margin-top: 20px; font-size: 24px; font-weight: 700; min-height: 36px;
}
```

## JS

```javascript
function checkAnswer(btn, quizId, label, isCorrect) {
  var options = document.querySelectorAll('#' + quizId + '-options .quiz-option');
  var feedback = document.getElementById(quizId + '-feedback');

  // 禁用所有按钮
  options.forEach(function(opt) { opt.disabled = true; });

  if (isCorrect) {
    btn.classList.add('correct');
    feedback.textContent = '✓ Correct!';
    feedback.style.color = '#27AE60';
  } else {
    btn.classList.add('wrong');
    feedback.textContent = '✗ Try again next time!';
    feedback.style.color = '#E74C3C';
    // 高亮正确答案
    options.forEach(function(opt) {
      if (opt.onclick.toString().includes('true')) {
        opt.classList.add('correct');
      }
    });
  }
}
```

## 注意事项

- 每道题用不同的 `quizId`（如 quiz1, quiz2）区分
- 正确答案通过 `isCorrect` 参数传入，不要硬编码在 JS 中
- 如需多选题，改为 toggle 选中状态 + "提交"按钮
