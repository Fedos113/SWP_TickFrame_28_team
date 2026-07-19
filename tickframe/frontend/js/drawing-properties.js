var DrawingProperties = (function () {
  var _panel = null;
  var _visible = false;
  var _currentId = null;
  var _initialized = false;

  var _COLORS = ['#00ff88', '#00c46a', '#3b82f6', '#ff4d5e', '#f97316', '#eab308', '#a855f7', '#ffffff'];


  function init() {
    if (_initialized) return;
    _initialized = true;
    _panel = document.getElementById('drawingProperties');
    if (!_panel) {
      _panel = document.createElement('div');
      _panel.id = 'drawingProperties';
      _panel.className = 'drawing-properties';
      document.body.appendChild(_panel);
    }
    DrawingEvents.on('drawing:selected', function (d) {
      if (d.drawing) { _show(d.drawing); } else { _hide(); }
    });
    DrawingEvents.on('drawing:deselected', _hide);
  }

  function _show(drawing) {
    _currentId = drawing.id;
    var style = drawing.style || {};
    _panel.innerHTML = '';
    _panel.style.display = 'block';
    _visible = true;

    var title = document.createElement('div');
    title.className = 'dp-title';
    title.textContent = drawing.type || 'Drawing';
    _panel.appendChild(title);

    _panel.appendChild(_buildSection('Color', _buildColors(style.lineColor || '#ffffff')));
    _panel.appendChild(_buildSection('Width', _buildSlider('lineWidth', style.lineWidth || 2, 1, 8, 1)));
    _panel.appendChild(_buildSection('Opacity', _buildSlider('fillOpacity', (style.fillOpacity || 0.2) * 100, 0, 100, 5)));
    _panel.appendChild(_buildSection('Style', _buildLineStyle(style.lineDash || [])));

    if (drawing.options && drawing.options.hasOwnProperty('extendLeft') !== undefined) {
      _panel.appendChild(_buildSection('Extend Left', _buildToggle('extendLeft', !!drawing.options.extendLeft)));
      _panel.appendChild(_buildSection('Extend Right', _buildToggle('extendRight', !!drawing.options.extendRight)));
    }

    _panel.appendChild(_buildSection('Lock', _buildToggle('locked', !!drawing.options.locked)));

    var closeBtn = document.createElement('button');
    closeBtn.className = 'dp-close';
    closeBtn.innerHTML = '<i data-lucide="x" style="width:16px;height:16px;stroke-width:2;"></i>';
    closeBtn.addEventListener('click', _hide);
    _panel.appendChild(closeBtn);

    _position();
    if (window.lucide) lucide.createIcons();
  }

  function _buildSection(label, content) {
    var sec = document.createElement('div');
    sec.className = 'dp-section';
    var lbl = document.createElement('div');
    lbl.className = 'dp-section-label';
    lbl.textContent = label;
    sec.appendChild(lbl);
    if (typeof content === 'string') { sec.innerHTML += content; }
    else { sec.appendChild(content); }
    return sec;
  }

  function _buildColors(active) {
    var wrap = document.createElement('div');
    wrap.className = 'dp-colors';
    _COLORS.forEach(function (c) {
      var dot = document.createElement('button');
      dot.className = 'dp-color' + (c === active ? ' active' : '');
      dot.style.background = c;
      dot.addEventListener('click', function () {
        _updateStyle('lineColor', c);
        wrap.querySelectorAll('.dp-color').forEach(function (b) { b.classList.remove('active'); });
        dot.classList.add('active');
      });
      wrap.appendChild(dot);
    });
    return wrap;
  }

  function _buildSlider(key, value, min, max, step) {
    var wrap = document.createElement('div');
    wrap.className = 'dp-slider-wrap';
    var input = document.createElement('input');
    input.type = 'range';
    input.className = 'dp-slider';
    input.min = min;
    input.max = max;
    input.step = step;
    input.value = value;
    input.addEventListener('input', function () {
      var v = parseFloat(input.value);
      if (key === 'fillOpacity') _updateStyle(key, v / 100);
      else _updateStyle(key, v);
    });
    var val = document.createElement('span');
    val.className = 'dp-slider-val';
    val.textContent = value;
    input.addEventListener('input', function () { val.textContent = input.value; });
    wrap.appendChild(input);
    wrap.appendChild(val);
    return wrap;
  }

  function _buildLineStyle(active) {
    var wrap = document.createElement('div');
    wrap.className = 'dp-line-styles';
    var styles = [
      { dash: [], label: 'Solid' },
      { dash: [6, 4], label: 'Dashed' },
      { dash: [2, 4], label: 'Dotted' },
    ];
    styles.forEach(function (s) {
      var btn = document.createElement('button');
      btn.className = 'dp-line-style' + (JSON.stringify(s.dash) === JSON.stringify(active) ? ' active' : '');
      btn.title = s.label;
      var canvas = document.createElement('canvas');
      canvas.width = 40;
      canvas.height = 10;
      var ctx = canvas.getContext('2d');
      ctx.strokeStyle = '#d1d4dc';
      ctx.lineWidth = 1.5;
      ctx.setLineDash(s.dash);
      ctx.beginPath(); ctx.moveTo(2, 5); ctx.lineTo(38, 5); ctx.stroke();
      btn.appendChild(canvas);
      btn.addEventListener('click', function () {
        _updateOptions('lineDash', s.dash);
        wrap.querySelectorAll('.dp-line-style').forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
      });
      wrap.appendChild(btn);
    });
    return wrap;
  }

  function _buildToggle(key, value) {
    var wrap = document.createElement('label');
    wrap.className = 'dp-toggle';
    var input = document.createElement('input');
    input.type = 'checkbox';
    input.checked = value;
    input.addEventListener('change', function () {
      _updateOptions(key, input.checked);
    });
    var slider = document.createElement('span');
    slider.className = 'dp-toggle-slider';
    wrap.appendChild(input);
    wrap.appendChild(slider);
    return wrap;
  }

  function _updateStyle(key, value) {
    if (!_currentId) return;
    var update = {};
    update[key] = value;
    DrawingController.updateDrawingStyle(_currentId, update);
  }

  function _updateOptions(key, value) {
    if (!_currentId) return;
    var update = {};
    update[key] = value;
    DrawingController.updateDrawingOptions(_currentId, update);
  }

  function _position() {
    if (!_panel) return;
    var toolbar = document.getElementById('drawingToolbar');
    if (toolbar) {
      var tr = toolbar.getBoundingClientRect();
      _panel.style.left = (tr.right + 12) + 'px';
      _panel.style.top = Math.max(70, tr.top) + 'px';
    }
  }

  function _hide() {
    if (!_panel) return;
    _panel.style.display = 'none';
    _visible = false;
    _currentId = null;
  }

  return { init: init };
})();
