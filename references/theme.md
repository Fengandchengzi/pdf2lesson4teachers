# PPT 默认视觉主题

## 定位

提供 ESL 课堂 PPT 的默认视觉规范（配色、字体、排版、组件样式）。Step 4.4 生成 HTML-PPT 时**必须使用此主题**作为基础样式。如需更高视觉质量，可额外调用 `frontend-design` skill 在此基础上定制。

设计原则：**清晰可读 > 视觉花哨**。6-10 岁学生 + 投影场景，需要高对比、大字号、友好圆润的风格。

---

## A. 字体导入

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
```

## B. CSS 变量 + 全局重置

```css
:root {
  /* 基础色 — 用户指定主题色时替换 --primary 即可 */
  --primary: #4A90D9;
  --primary-light: #D6EAF8;
  --primary-bg: #EBF5FB;
  --accent: #F39C12;
  --success: #27AE60;
  --danger: #E74C3C;
  --text: #2c3e50;
  --text-light: #7f8c8d;
  --white: #FFFFFF;
  --gradient: linear-gradient(135deg, var(--primary), #7FB3E0);

  /* 教学环节色（与 navigation.md 进度条一致） */
  --phase-warmup: #42A5F5;
  --phase-presentation: #66BB6A;
  --phase-practice: #FFA726;
  --phase-production: #AB47BC;
  --phase-wrapup: #EF5350;
}

*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Nunito', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #1a1a2e;
  overflow: hidden;
  width: 100vw;
  height: 100vh;
  user-select: none;
  -webkit-user-select: none;
}
```

## C. 排版规范

```css
/* 标题 — 响应式，投影下限 2rem */
.slide-title {
  font-size: clamp(28px, 4vw, 48px);
  font-weight: 800;
  color: var(--text);
  text-align: center;
  margin-bottom: 16px;
}

/* 副标题 */
.slide-subtitle {
  font-size: clamp(16px, 2.2vw, 24px);
  color: var(--text-light);
  font-weight: 600;
  text-align: center;
}

/* 封面标题 — 更大 */
.cover-title {
  font-size: clamp(36px, 6vw, 72px);
  font-weight: 900;
  color: var(--white);
  text-shadow: 0 4px 20px rgba(0,0,0,0.3);
  margin-bottom: 12px;
}

.cover-sub {
  font-size: clamp(18px, 3vw, 32px);
  font-weight: 600;
  color: var(--white);
  opacity: 0.9;
}

/* 过渡页大字 */
.big-text {
  font-size: clamp(36px, 5vw, 64px);
  font-weight: 900;
  text-shadow: 0 3px 12px rgba(0,0,0,0.15);
}
```

## D. Slide 背景规范

```css
/* 封面 — 渐变叠加背景图 */
.slide-cover {
  background-image: linear-gradient(135deg, rgba(74,144,217,0.75), rgba(44,62,80,0.7)),
    url('images/cover.jpg');
  background-size: cover;
  background-position: center;
  color: var(--white);
}

/* 环节过渡页 — 渐变全屏，白色文字 */
.slide-transition {
  background: var(--gradient);
  color: var(--white);
}
/* 各环节过渡页专用渐变（深色→中色，确保白字可读） */
.slide-transition[data-phase="warmup"]       { background: linear-gradient(135deg, #1E88E5, #42A5F5); }
.slide-transition[data-phase="presentation"] { background: linear-gradient(135deg, #43A047, #66BB6A); }
.slide-transition[data-phase="practice"]     { background: linear-gradient(135deg, #E65100, #FB8C00); }
.slide-transition[data-phase="production"]   { background: linear-gradient(135deg, #7B1FA2, #AB47BC); }
.slide-transition[data-phase="wrapup"]       { background: linear-gradient(135deg, #C62828, #EF5350); }

/* 内容 Slide — 浅色背景，按环节区分 */
.slide[data-phase="warmup"]       { background: #E3F2FD; }
.slide[data-phase="presentation"] { background: #E8F5E9; }
.slide[data-phase="practice"]     { background: #FFF3E0; }
.slide[data-phase="production"]   { background: #F3E5F5; }
.slide[data-phase="wrapup"]       { background: #FFEBEE; }
```

## E. 通用组件样式

```css
/* 环节徽章 */
.phase-badge {
  position: absolute;
  top: 16px; left: 16px;
  padding: 4px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 700;
  color: var(--white);
  text-transform: uppercase;
  z-index: 5;
}
.slide[data-phase="warmup"] .phase-badge       { background: var(--phase-warmup); }
.slide[data-phase="presentation"] .phase-badge { background: var(--phase-presentation); }
.slide[data-phase="practice"] .phase-badge     { background: var(--phase-practice); }
.slide[data-phase="production"] .phase-badge   { background: var(--phase-production); }
.slide[data-phase="wrapup"] .phase-badge       { background: var(--phase-wrapup); }

/* 卡片 */
.card {
  background: var(--white);
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  padding: 24px;
  transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

/* TTS 按钮 */
.tts-btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 10px 22px;
  border-radius: 30px;
  border: none;
  background: var(--gradient);
  color: var(--white);
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  transition: transform 0.15s, box-shadow 0.15s;
  box-shadow: 0 3px 12px rgba(74,144,217,0.3);
  min-width: 44px;
  min-height: 44px;
}
.tts-btn:hover { transform: scale(1.05); }
.tts-btn:active { transform: scale(0.97); }
.tts-btn.green { background: linear-gradient(135deg, #27AE60, #6FCF97); box-shadow: 0 3px 12px rgba(39,174,96,0.3); }
.tts-btn.slow  { background: linear-gradient(135deg, #F39C12, #F9CA63); box-shadow: 0 3px 12px rgba(243,156,18,0.3); }
```

## F. 动画库

```css
/* 过渡页图标弹入 */
@keyframes bounceIn {
  0%   { transform: scale(0.3); opacity: 0; }
  50%  { transform: scale(1.1); }
  70%  { transform: scale(0.95); }
  100% { transform: scale(1); opacity: 1; }
}

/* 内容渐入 */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* 错误反馈抖动 */
@keyframes shake {
  0%,100% { transform: translateX(0); }
  20% { transform: translateX(-12px); }
  40% { transform: translateX(12px); }
  60% { transform: translateX(-8px); }
  80% { transform: translateX(8px); }
}

.slide-transition .big-icon {
  font-size: 80px;
  margin-bottom: 20px;
  animation: bounceIn 0.7s ease;
}
```

## G. 投影适配

```css
/* 最小点击区域 44×44px（触屏友好） */
button, .clickable { min-width: 44px; min-height: 44px; }

/* 教师面板毛玻璃 */
.teacher-panel {
  background: rgba(45,55,72,0.92);
  backdrop-filter: blur(12px);
}
```

HTML `<head>` 中必须包含：
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

---

## 主题定制说明

用户指定主题色（如"用粉色"）时，只需修改 `:root` 中的 `--primary` 及其衍生变量：

```css
/* 示例：粉色主题 */
--primary: #E8637A;
--primary-light: #F5C6D0;
--primary-bg: #FFF0F3;
--gradient: linear-gradient(135deg, #E8637A, #F5A0B0);
```

其余所有组件因为引用 CSS 变量，会自动跟随变色。
