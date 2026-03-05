# 拖放分类（categorize）

**用途**：词汇/概念分类活动 — 将词汇拖到对应类别区域。

## HTML

```html
<div class="drag-container">
  <h2 class="drag-title">Sort the words!</h2>

  <!-- 待拖放的词汇 -->
  <div class="drag-items" id="drag-source">
    <div class="drag-item" draggable="true" data-answer="catA" id="item1">broom</div>
    <div class="drag-item" draggable="true" data-answer="catB" id="item2">toy box</div>
    <div class="drag-item" draggable="true" data-answer="catA" id="item3">sponge</div>
    <div class="drag-item" draggable="true" data-answer="catB" id="item4">laundry basket</div>
  </div>

  <!-- 放置区 -->
  <div class="drop-zones">
    <div class="drop-zone" id="catA" ondrop="handleDrop(event)" ondragover="event.preventDefault()">
      <h3>Cleaning</h3>
      <div class="drop-list"></div>
    </div>
    <div class="drop-zone" id="catB" ondrop="handleDrop(event)" ondragover="event.preventDefault()">
      <h3>Organizing</h3>
      <div class="drop-list"></div>
    </div>
  </div>

  <div class="drag-feedback" id="drag-feedback"></div>
</div>
```

## CSS

```css
.drag-container {
  text-align: center; padding: 30px; max-width: 800px; width: 100%;
}
.drag-title {
  font-size: 32px; color: #2c3e50; margin-bottom: 20px;
}
.drag-items {
  display: flex; flex-wrap: wrap; justify-content: center;
  gap: 12px; margin-bottom: 24px; min-height: 50px;
}
.drag-item {
  padding: 12px 24px; background: #F39C12; color: white;
  border-radius: 12px; font-size: 20px; font-weight: 600;
  cursor: grab; user-select: none; transition: transform 0.2s, opacity 0.2s;
}
.drag-item:active { cursor: grabbing; transform: scale(1.05); }
.drag-item.placed { opacity: 0.4; pointer-events: none; }
.drop-zones {
  display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px;
}
.drop-zone {
  background: #EAF2F8; border: 3px dashed #BDC3C7; border-radius: 16px;
  padding: 20px; min-height: 180px; transition: border-color 0.2s, background 0.2s;
}
.drop-zone.over {
  border-color: #3498DB; background: #D6EAF8;
}
.drop-zone h3 {
  font-size: 22px; color: #2c3e50; margin-bottom: 12px;
}
.drop-list {
  display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;
}
.drop-list .drag-item {
  background: #27AE60; cursor: default; font-size: 18px;
}
.drop-list .drag-item.wrong-place {
  background: #E74C3C;
}
.drag-feedback {
  margin-top: 20px; font-size: 24px; font-weight: 700; min-height: 36px;
}
```

## JS

```javascript
// 拖放事件
document.querySelectorAll('.drag-item').forEach(function(item) {
  item.addEventListener('dragstart', function(e) {
    e.dataTransfer.setData('text/plain', item.id);
    setTimeout(function() { item.style.opacity = '0.5'; }, 0);
  });
  item.addEventListener('dragend', function() {
    item.style.opacity = '1';
  });
});

// 放置区视觉反馈
document.querySelectorAll('.drop-zone').forEach(function(zone) {
  zone.addEventListener('dragenter', function(e) {
    e.preventDefault(); zone.classList.add('over');
  });
  zone.addEventListener('dragleave', function() {
    zone.classList.remove('over');
  });
});

function handleDrop(e) {
  e.preventDefault();
  var zone = e.currentTarget;
  zone.classList.remove('over');

  var itemId = e.dataTransfer.getData('text/plain');
  var item = document.getElementById(itemId);
  if (!item) return;

  var correctZone = item.getAttribute('data-answer');
  var dropList = zone.querySelector('.drop-list');

  // 克隆到放置区
  var clone = item.cloneNode(true);
  clone.draggable = false;
  clone.style.opacity = '1';
  clone.removeAttribute('id');

  if (zone.id === correctZone) {
    clone.classList.remove('wrong-place');
  } else {
    clone.classList.add('wrong-place');
  }

  dropList.appendChild(clone);
  item.classList.add('placed');

  // 检查是否全部放完
  var remaining = document.querySelectorAll('#drag-source .drag-item:not(.placed)');
  if (remaining.length === 0) {
    checkDragResult();
  }
}

function checkDragResult() {
  var wrong = document.querySelectorAll('.drop-list .wrong-place');
  var feedback = document.getElementById('drag-feedback');
  if (wrong.length === 0) {
    feedback.textContent = '✓ All correct!';
    feedback.style.color = '#27AE60';
  } else {
    feedback.textContent = wrong.length + ' wrong — try moving them!';
    feedback.style.color = '#E74C3C';
  }
}
```

## 触屏适配（可选）

在拖放 JS 之后添加以下代码，移动端自动切换为点击模式：

```javascript
if ('ontouchstart' in window) {
  var selectedItem = null;
  document.querySelectorAll('.drag-item[draggable]').forEach(function(item) {
    item.draggable = false;
    item.addEventListener('click', function() {
      if (item.classList.contains('placed')) return;
      document.querySelectorAll('.drag-item').forEach(function(i) { i.style.outline = ''; });
      item.style.outline = '3px solid #3498DB';
      selectedItem = item;
    });
  });
  document.querySelectorAll('.drop-zone').forEach(function(zone) {
    zone.addEventListener('click', function() {
      if (!selectedItem) return;
      handleDrop({ preventDefault: function(){}, currentTarget: zone,
        dataTransfer: { getData: function() { return selectedItem.id; } } });
      selectedItem.style.outline = '';
      selectedItem = null;
    });
  });
}
```

## 注意事项

- `data-answer` 属性值必须与目标 `drop-zone` 的 `id` 一致
- 类别数量可扩展，调整 `grid-template-columns` 即可
