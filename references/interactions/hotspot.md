# 热区点击（scene）

**用途**：场景探索 — 背景大图上的可点击热区，点击弹出词汇+TTS发音。

## HTML

```html
<div class="scene-container">
  <img class="scene-bg" src="images/img_kitchen.jpg" alt="Kitchen scene">

  <!-- 热区：用百分比定位 -->
  <div class="hotspot" style="top:30%;left:20%" onclick="showHotspot(this,'broom','扫帚')">
    <span class="hotspot-dot"></span>
  </div>
  <div class="hotspot" style="top:50%;left:60%" onclick="showHotspot(this,'sponge','海绵')">
    <span class="hotspot-dot"></span>
  </div>
  <div class="hotspot" style="top:25%;left:75%" onclick="showHotspot(this,'plate','盘子')">
    <span class="hotspot-dot"></span>
  </div>

  <!-- 弹出层 -->
  <div class="hotspot-popup" id="hotspot-popup">
    <span class="hotspot-popup-word" id="popup-word"></span>
    <span class="hotspot-popup-meaning" id="popup-meaning"></span>
    <button class="tts-btn" id="popup-tts" onclick="play(this.dataset.audio)">🔊</button>
    <button class="hotspot-popup-close" onclick="hideHotspot()">✕</button>
  </div>
</div>
```

## CSS

```css
.scene-container {
  position: relative; width: 100%; height: 100%;
  display: flex; justify-content: center; align-items: center;
}
.scene-bg {
  width: 100%; height: 100%; object-fit: cover;
}
.hotspot {
  position: absolute; cursor: pointer; z-index: 10;
}
.hotspot-dot {
  display: block; width: 36px; height: 36px;
  background: rgba(255, 165, 0, 0.7); border: 3px solid white;
  border-radius: 50%; box-shadow: 0 0 0 6px rgba(255,165,0,0.3);
  animation: hotspot-pulse 2s infinite;
}
@keyframes hotspot-pulse {
  0%, 100% { box-shadow: 0 0 0 6px rgba(255,165,0,0.3); }
  50% { box-shadow: 0 0 0 12px rgba(255,165,0,0.1); }
}
.hotspot-popup {
  display: none; position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  background: white; border-radius: 16px; padding: 24px 32px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.3); z-index: 20;
  text-align: center; min-width: 200px;
}
.hotspot-popup.visible { display: block; }
.hotspot-popup-word {
  display: block; font-size: 36px; font-weight: 700; color: #2c3e50;
  margin-bottom: 8px;
}
.hotspot-popup-meaning {
  display: block; font-size: 18px; color: #7f8c8d; margin-bottom: 16px;
}
.hotspot-popup-close {
  position: absolute; top: 8px; right: 12px;
  background: none; border: none; font-size: 20px; color: #BDC3C7;
  cursor: pointer;
}
```

## JS

```javascript
function showHotspot(el, audioName, meaning) {
  var popup = document.getElementById('hotspot-popup');
  document.getElementById('popup-word').textContent = audioName;
  document.getElementById('popup-meaning').textContent = meaning;
  document.getElementById('popup-tts').dataset.audio = audioName;
  popup.classList.add('visible');
  play(audioName);
}

function hideHotspot() {
  document.getElementById('hotspot-popup').classList.remove('visible');
}
```

## 注意事项

- 热区位置用**百分比**（`top/left`），适配不同分辨率
- `hotspot-pulse` 动画使用 `box-shadow` 而非 `animation-fill-mode: forwards`（遵守导航规则）
- 大纲中需标注每个热区的大致位置和对应词汇
