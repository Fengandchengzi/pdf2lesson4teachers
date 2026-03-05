# PPT 导航系统参考

## 定位

提供经过验证的导航代码模板，Step 4.4 生成 HTML-PPT 时**必须使用此模板**，不要从零编写导航逻辑。

## 核心原则

1. 所有 Slide 始终在 DOM 中，用 `display` 切换显示/隐藏
2. **禁止使用一次性 CSS 动画**（animation-fill-mode: forwards 等），否则后退时内容不可见
3. 导航状态只依赖 `currentSlide` 索引，前进后退逻辑对称
4. 三种翻页方式同时支持：键盘、按钮点击、触摸滑动

## HTML 结构

```html
<!-- 所有 Slide -->
<section class="slide" data-phase="cover" id="slide-1">...</section>
<section class="slide" data-phase="warmup" id="slide-2">...</section>
<!-- ... -->

<!-- 底部导航区域（分段进度条 + 按钮） -->
<div class="bottom-bar">
  <!-- 分段配色进度条 -->
  <div class="phase-progress" id="phase-progress"></div>

  <!-- 导航按钮 -->
  <nav class="slide-nav">
    <button class="nav-btn nav-prev" onclick="prevSlide()" title="上一页 (←)">‹</button>
    <span class="nav-info">
      <span id="nav-current">1</span> / <span id="nav-total"></span>
    </span>
    <button class="nav-btn nav-next" onclick="nextSlide()" title="下一页 (→)">›</button>
  </nav>
</div>

<!-- 教师面板（T 键切换） -->
<div class="teacher-panel">
  <h3>教师备注</h3>
  <div class="note-content"></div>
</div>
```

## CSS 模板

```css
/* === 导航核心样式 === */

/* Slide 默认隐藏 */
.slide {
  display: none;
  width: 100vw;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

/* 当前 Slide 显示 */
.slide.active {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

/* 底部导航区域 */
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-bottom: 8px;
  background: linear-gradient(transparent, rgba(0,0,0,0.15));
  pointer-events: none;
}

.bottom-bar > * {
  pointer-events: auto;
}

/* 导航按钮 */
.slide-nav {
  display: flex;
  align-items: center;
  gap: 20px;
  background: rgba(0, 0, 0, 0.6);
  padding: 6px 20px;
  border-radius: 30px;
  margin-bottom: 6px;
}

.nav-btn {
  background: none;
  border: none;
  color: white;
  font-size: 28px;
  cursor: pointer;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s;
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.nav-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.nav-info {
  color: white;
  font-size: 14px;
  min-width: 60px;
  text-align: center;
}

/* 分段配色进度条 */
.phase-progress {
  display: flex;
  width: 90%;
  height: 6px;
  border-radius: 3px;
  overflow: hidden;
  background: rgba(0,0,0,0.1);
}

.phase-progress .seg {
  height: 100%;
  transition: opacity 0.3s;
}

/* 未到达的段半透明 */
.phase-progress .seg.future {
  opacity: 0.3;
}

/* 环节配色 */
.phase-progress .seg[data-phase="cover"]        { background: #9E9E9E; }
.phase-progress .seg[data-phase="warmup"]       { background: #42A5F5; }
.phase-progress .seg[data-phase="presentation"] { background: #66BB6A; }
.phase-progress .seg[data-phase="practice"]     { background: #FFA726; }
.phase-progress .seg[data-phase="production"]   { background: #AB47BC; }
.phase-progress .seg[data-phase="wrapup"]       { background: #EF5350; }

/* 教师面板 */
.teacher-panel {
  display: none;
  position: fixed;
  right: 0;
  top: 0;
  width: 320px;
  height: 100vh;
  background: rgba(0, 0, 0, 0.85);
  color: white;
  padding: 20px;
  overflow-y: auto;
  z-index: 999;
  font-size: 14px;
  line-height: 1.6;
}

.teacher-panel.visible {
  display: block;
}

.teacher-panel h3 {
  color: #4A90D9;
  margin-bottom: 10px;
}
```

## JavaScript 模板

```javascript
// === PPT 导航系统 ===

(function() {
  const slides = document.querySelectorAll('.slide');
  const totalSlides = slides.length;
  let currentSlide = 0;

  // 初始化
  document.getElementById('nav-total').textContent = totalSlides;
  buildPhaseProgress();
  showSlide(0);

  // 构建分段进度条（每个 slide 一个小段，按 data-phase 配色）
  function buildPhaseProgress() {
    const bar = document.getElementById('phase-progress');
    if (!bar) return;

    slides.forEach(s => {
      const seg = document.createElement('div');
      seg.className = 'seg';
      seg.setAttribute('data-phase', s.getAttribute('data-phase') || 'other');
      seg.style.flex = 1;
      bar.appendChild(seg);
    });
  }

  // 核心：显示指定 Slide
  function showSlide(index) {
    // 边界检查
    if (index < 0 || index >= totalSlides) return;

    // 隐藏所有 Slide
    slides.forEach(s => s.classList.remove('active'));

    // 显示目标 Slide
    currentSlide = index;
    slides[currentSlide].classList.add('active');

    // 更新导航信息
    document.getElementById('nav-current').textContent = currentSlide + 1;

    // 更新按钮状态
    document.querySelector('.nav-prev').disabled = (currentSlide === 0);
    document.querySelector('.nav-next').disabled = (currentSlide === totalSlides - 1);

    // 更新分段进度条
    updatePhaseProgress();

    // 更新教师备注
    updateTeacherNote();
  }

  // 更新分段进度条（按 slide 索引：已过的亮，未到的半透明）
  function updatePhaseProgress() {
    const bar = document.getElementById('phase-progress');
    if (!bar) return;
    const segs = bar.querySelectorAll('.seg');

    segs.forEach((seg, i) => {
      if (i <= currentSlide) {
        seg.classList.remove('future');
      } else {
        seg.classList.add('future');
      }
    });
  }

  // 前进 / 后退
  function nextSlide() { showSlide(currentSlide + 1); }
  function prevSlide() { showSlide(currentSlide - 1); }

  // 暴露到全局（供 onclick 调用）
  window.nextSlide = nextSlide;
  window.prevSlide = prevSlide;
  window.showSlide = showSlide;

  // 键盘导航
  document.addEventListener('keydown', function(e) {
    switch(e.key) {
      case 'ArrowRight':
      case 'ArrowDown':
      case ' ':
        e.preventDefault();
        nextSlide();
        break;
      case 'ArrowLeft':
      case 'ArrowUp':
        e.preventDefault();
        prevSlide();
        break;
      case 't':
      case 'T':
        toggleTeacherPanel();
        break;
    }
  });

  // 触摸滑动
  let touchStartX = 0;
  document.addEventListener('touchstart', function(e) {
    touchStartX = e.changedTouches[0].screenX;
  });
  document.addEventListener('touchend', function(e) {
    const diff = touchStartX - e.changedTouches[0].screenX;
    if (Math.abs(diff) > 50) {
      if (diff > 0) nextSlide();  // 左滑 → 下一页
      else prevSlide();            // 右滑 → 上一页
    }
  });

  // 教师面板
  const teacherPanel = document.querySelector('.teacher-panel');
  const teacherNotes = {};

  // 收集所有教师备注（从 data-teacher-note 属性）
  slides.forEach((slide, i) => {
    const note = slide.getAttribute('data-teacher-note');
    if (note) teacherNotes[i] = note;
  });

  function updateTeacherNote() {
    if (!teacherPanel) return;
    const noteEl = teacherPanel.querySelector('.note-content');
    if (noteEl) {
      noteEl.textContent = teacherNotes[currentSlide] || '（无备注）';
    }
  }

  function toggleTeacherPanel() {
    if (teacherPanel) {
      teacherPanel.classList.toggle('visible');
    }
  }
  window.toggleTeacherPanel = toggleTeacherPanel;

})();
```

## TTS 播放函数

与导航系统配合使用（音频文件在 `audio/` 目录）：

```javascript
// 播放单个音频
function play(filename) {
  const audio = new Audio('audio/' + filename + '.mp3');
  audio.play();
}

// 顺序播放多个音频
function playSequence(filenames, index = 0) {
  if (index >= filenames.length) return;
  const audio = new Audio('audio/' + filenames[index] + '.mp3');
  audio.onended = () => playSequence(filenames, index + 1);
  audio.play();
}
```

## Slide 中教师备注的写法

每个 `<section>` 通过 `data-teacher-note` 属性携带教师备注：

```html
<section class="slide" data-phase="warmup" id="slide-2"
  data-teacher-note="展示图片，给学生10秒观察，问 What are they doing? 接受中文回答。">
  <!-- slide 内容 -->
</section>
```

## 检查清单

生成 HTML-PPT 后必须检查：

```
□ 所有 Slide 都有 class="slide" 和 data-phase 属性
□ 第一个 Slide 有 class="slide active"（或由 JS 初始化）
□ 底部导航区域（.bottom-bar）包含分段进度条和导航按钮
□ nav-total 正确显示总 Slide 数
□ 按 ← 能回到上一页且内容正确显示
□ 按 → 到最后一页时按钮禁用
□ 按 ← 到第一页时按钮禁用
□ 没有使用 animation-fill-mode: forwards
□ 教师备注面板按 T 能切换
□ 分段进度条颜色随环节变化，未到达段半透明
```
