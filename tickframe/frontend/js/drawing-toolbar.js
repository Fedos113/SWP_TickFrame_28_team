var TOOL_GROUPS = [
  {
    id: 'pointer', label: '',
    tools: [{ id: 'cursor', type: null, icon: 'Pointer', title: 'Pointer', shortcut: 'V' }],
  },
  {
    id: 'lines', label: 'Lines',
    tools: [
      { id: 'trend-line', type: 'trend-line', icon: 'MoveUpRight', title: 'Trend Line', shortcut: 'L' },
      { id: 'horizontal-line', type: 'horizontal-line', icon: 'Minus', title: 'Horizontal Line', shortcut: 'H' },
      { id: 'vertical-line', type: 'vertical-line', icon: 'SeparatorVertical', title: 'Vertical Line', shortcut: 'Shift+V' },
      { id: 'ray', type: 'ray', icon: 'ArrowUpFromLine', title: 'Ray' },
      { id: 'cross-line', type: 'cross-line', icon: 'Crosshair', title: 'Cross Line' },
      { id: 'info-line', type: 'info-line', icon: 'Info', title: 'Info Line' },
    ],
  },
  {
    id: 'channels', label: 'Channels',
    tools: [
      { id: 'parallel-channel', type: 'parallel-channel', icon: 'GitCompare', title: 'Parallel Channel' },
      { id: 'regression-trend', type: 'regression-trend', icon: 'TrendingUp', title: 'Regression Trend' },
    ],
  },
  {
    id: 'fibonacci', label: 'Fibonacci',
    tools: [
      { id: 'fib-retracement', type: 'fib-retracement', icon: 'Percent', title: 'Fib Retracement' },
      { id: 'fib-extension', type: 'fib-extension', icon: 'ArrowRightFromLine', title: 'Fib Extension' },
      { id: 'fib-channel', type: 'fib-channel', icon: 'GitBranch', title: 'Fib Channel' },
      { id: 'fib-time-zone', type: 'fib-time-zone', icon: 'Clock', title: 'Fib Time Zone' },
    ],
  },
  {
    id: 'gann', label: 'Gann',
    tools: [
      { id: 'gann-box', type: 'gann-box', icon: 'LayoutGrid', title: 'Gann Box' },
      { id: 'gann-fan', type: 'gann-fan', icon: 'Fan', title: 'Gann Fan' },
    ],
  },
  {
    id: 'shapes', label: 'Shapes',
    tools: [
      { id: 'rectangle', type: 'rectangle', icon: 'Square', title: 'Rectangle', shortcut: 'R' },
      { id: 'circle', type: 'circle', icon: 'Circle', title: 'Circle', shortcut: 'C' },
      { id: 'triangle', type: 'triangle', icon: 'Triangle', title: 'Triangle', shortcut: 'T' },
    ],
  },
  {
    id: 'annotations', label: 'Annotate',
    tools: [
      { id: 'arrow', type: 'arrow', icon: 'ArrowUpRight', title: 'Arrow', shortcut: 'A' },
      { id: 'price-label', type: 'price-label', icon: 'Tag', title: 'Price Label' },
      { id: 'flag-mark', type: 'flag-mark', icon: 'Flag', title: 'Flag Mark' },
    ],
  },
  {
    id: 'measure', label: 'Measure',
    tools: [
      { id: 'price-range', type: 'price-range', icon: 'ArrowUpDown', title: 'Price Range' },
      { id: 'date-range', type: 'date-range', icon: 'ArrowLeftRight', title: 'Date Range' },
      { id: 'date-price-range', type: 'date-price-range', icon: 'MoveDiagonal', title: 'Date & Price' },
    ],
  },
  {
    id: 'positions', label: 'Trades',
    tools: [
      { id: 'long-position', type: 'long-position', icon: 'TrendingUp', title: 'Long Position' },
      { id: 'short-position', type: 'short-position', icon: 'TrendingDown', title: 'Short Position' },
    ],
  },
  {
    id: 'actions', label: '',
    tools: [
      { id: 'delete', type: 'delete', icon: 'Trash2', title: 'Delete Selected', shortcut: 'Del' },
      { id: 'clear', type: 'clear', icon: 'Eraser', title: 'Clear All' },
    ],
  },
];

var _COLORS = ['#00ff88', '#00c46a', '#2962FF', '#ff4d5e', '#f97316', '#eab308', '#a855f7', '#ec4899', '#5f8f72', '#ffffff'];

var _LINE_STYLES = [
  { dash: [], label: 'Solid' },
  { dash: [6, 4], label: 'Dashed' },
  { dash: [2, 4], label: 'Dotted' },
];

var DrawingToolbar = (function () {
  var _toolbarEl = null;
  var _tooltipEl = null;
  var _settingsPanel = null;
  var _settingsVisible = false;
  var _initialized = false;
  var _dragState = null;

  function init() {
    if (_initialized) return;
    _toolbarEl = document.getElementById('drawingToolbar');
    if (!_toolbarEl) return;
    _createTooltip();
    _createSettingsPanel();
    _build();
    DrawingEvents.on('tool:changed', function (d) { _highlight(d.toolId); if (_settingsVisible) _refreshSettings(); });
    _loadPosition();
    _initialized = true;
  }

  function _createTooltip() {
    _tooltipEl = document.createElement('div');
    _tooltipEl.className = 'dt-tooltip';
    _tooltipEl.style.display = 'none';
    document.body.appendChild(_tooltipEl);
  }

  function _build() {
    _toolbarEl.innerHTML = '';
    var handle = document.createElement('div');
    handle.className = 'dt-drag-handle';
    handle.innerHTML = '<i data-lucide="GripVertical" style="width:14px;height:14px;stroke-width:2;"></i>';
    _toolbarEl.appendChild(handle);
    _initDrag(handle);
    var settingsBtn = document.createElement('button');
    settingsBtn.className = 'dt-btn';
    settingsBtn.setAttribute('data-tool', '_settings');
    settingsBtn.setAttribute('aria-label', 'Drawing Defaults');
    settingsBtn.innerHTML = '<i data-lucide="Settings" style="width:16px;height:16px;stroke-width:2;"></i>';
    settingsBtn.addEventListener('click', _toggleSettings);
    _toolbarEl.appendChild(settingsBtn);
    TOOL_GROUPS.forEach(function (group) {
      var groupEl = document.createElement('div');
      groupEl.className = 'dt-group';
      group.tools.forEach(function (tool) {
        var btn = document.createElement('button');
        btn.className = 'dt-btn' + (tool.type === null ? ' active' : '');
        btn.setAttribute('data-tool', tool.id);
        btn.setAttribute('aria-label', tool.title + (tool.shortcut ? ' (' + tool.shortcut + ')' : ''));
        var iconEl = document.createElement('i');
        iconEl.setAttribute('data-lucide', tool.icon);
        iconEl.setAttribute('data-tool-id', tool.id);
        iconEl.style.cssText = 'width:14px;height:14px;stroke-width:1.75;';
        btn.appendChild(iconEl);
        btn.addEventListener('click', function () { _click(tool); });
        btn.addEventListener('mouseenter', function (e) { _showTooltip(e, tool); });
        btn.addEventListener('mouseleave', function () { _hideTooltip(); });
        btn.addEventListener('mousemove', function (e) { _moveTooltip(e); });
        groupEl.appendChild(btn);
      });
      _toolbarEl.appendChild(groupEl);
    });
    if (window.lucide) {
      try { lucide.createIcons(); } catch (e) { console.warn('Lucide icons error:', e); }
    }
  }

  function _click(tool) {
    if (!window.DrawingController) { console.error('DrawingController not available'); return; }
    if (tool.type === 'delete') { DrawingController.deleteSelection(); return; }
    if (tool.type === 'clear') { if (confirm('Clear all drawings?')) { DrawingController.clearAll(); } return; }
    DrawingController.activateTool(tool.type);
  }

  function _highlight(toolId) {
    _toolbarEl.querySelectorAll('.dt-btn').forEach(function (b) { b.classList.remove('active'); });
    if (!toolId || toolId === 'cursor') {
      var pointer = _toolbarEl.querySelector('[data-tool="cursor"]');
      if (pointer) pointer.classList.add('active');
      return;
    }
    var btn = _toolbarEl.querySelector('[data-tool="' + toolId + '"]');
    if (btn) btn.classList.add('active');
  }

  function _showTooltip(e, tool) {
    var text = tool.title;
    if (tool.shortcut) text += ' <span class="dt-tooltip-shortcut">' + tool.shortcut + '</span>';
    _tooltipEl.innerHTML = text;
    _tooltipEl.style.display = 'block';
    _positionTooltip(e);
  }

  function _moveTooltip(e) { _positionTooltip(e); }

  function _positionTooltip(e) {
    var x = e.clientX + 14;
    var y = e.clientY - 10;
    var rect = _tooltipEl.getBoundingClientRect();
    if (x + rect.width > window.innerWidth - 10) x = e.clientX - rect.width - 14;
    if (y + rect.height > window.innerHeight - 10) y = window.innerHeight - rect.height - 10;
    if (y < 10) y = 10;
    _tooltipEl.style.left = x + 'px';
    _tooltipEl.style.top = y + 'px';
  }

  function _hideTooltip() { _tooltipEl.style.display = 'none'; }

  function _initDrag(handle) {
    handle.addEventListener('mousedown', function (e) {
      e.preventDefault();
      e.stopPropagation();
      var left = _toolbarEl.style.left || getComputedStyle(_toolbarEl).left;
      var top = _toolbarEl.style.top || getComputedStyle(_toolbarEl).top;
      _dragState = {
        startX: e.clientX,
        startY: e.clientY,
        origLeft: parseInt(left, 10) || 26,
        origTop: parseInt(top, 10) || 40,
      };
      handle.classList.add('dragging');
      document.addEventListener('mousemove', _onDragMove);
      document.addEventListener('mouseup', _onDragEnd);
    });
  }

  function _onDragMove(e) {
    if (!_dragState) return;
    var dx = e.clientX - _dragState.startX;
    var dy = e.clientY - _dragState.startY;
    _toolbarEl.style.left = (_dragState.origLeft + dx) + 'px';
    _toolbarEl.style.top = (_dragState.origTop + dy) + 'px';
  }

  function _onDragEnd(e) {
    if (!_dragState) return;
    document.removeEventListener('mousemove', _onDragMove);
    document.removeEventListener('mouseup', _onDragEnd);
    var handle = _toolbarEl.querySelector('.dt-drag-handle');
    if (handle) handle.classList.remove('dragging');
    var left = parseInt(_toolbarEl.style.left, 10);
    var top = parseInt(_toolbarEl.style.top, 10);
    _dragState = null;
    if (!isNaN(left) && !isNaN(top)) {
      _savePosition(left, top);
    }
  }

  function _loadPosition() {
    fetch('/api/toolbar-position')
      .then(function (r) { return r.json(); })
      .then(function (pos) {
        if (pos.left != null) _toolbarEl.style.left = pos.left + 'px';
        if (pos.top != null) _toolbarEl.style.top = pos.top + 'px';
      })
      .catch(function () {});
  }

  function _savePosition(left, top) {
    fetch('/api/toolbar-position', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ left: left, top: top }),
    }).catch(function () {});
  }

  /* === Settings Panel === */

  function _createSettingsPanel() {
    _settingsPanel = document.createElement('div');
    _settingsPanel.className = 'dt-settings-panel';
    _settingsPanel.style.display = 'none';
    document.body.appendChild(_settingsPanel);
  }

  function _toggleSettings() {
    if (_settingsVisible) _hideSettings(); else _showSettings();
  }

  function _showSettings() {
    _refreshSettings();
    _settingsPanel.style.display = 'block';
    _settingsVisible = true;
    _positionPanel();
  }

  function _hideSettings() {
    _settingsPanel.style.display = 'none';
    _settingsVisible = false;
  }

  function _refreshSettings() {
    var toolType = null;
    var allDrawings = window.DrawingController ? window.DrawingController.getManager().getAllDrawings() : [];
    if (allDrawings.length > 0) {
      var last = allDrawings[allDrawings.length - 1];
      toolType = last.toolType;
    }
    var mgr = window.DrawingController ? window.DrawingController.getManager() : null;
    var active = mgr ? mgr.getActiveTool() : null;
    if (active) toolType = active;
    if (!toolType) toolType = 'trend-line';
    var defaults = (window.DrawingSettings || {}).getDefaults ? DrawingSettings.getDefaults(toolType) : {};
    _renderPanelContent(toolType, defaults);
  }

  function _renderPanelContent(toolType, settings) {
    _settingsPanel.innerHTML = '';
    var title = document.createElement('div');
    title.className = 'dt-settings-title';
    title.textContent = 'Defaults: ' + (toolType || '?');
    _settingsPanel.appendChild(title);

    var hasLineViz = ['trend-line','horizontal-line','vertical-line','ray','cross-line','info-line',
      'parallel-channel','regression-trend','fib-retracement','fib-extension','fib-channel',
      'gann-box','gann-fan','rectangle','circle','triangle','arrow',
      'price-range','date-range','date-price-range'
    ].indexOf(toolType) >= 0;

    var hasFillViz = ['parallel-channel','fib-retracement','fib-extension','fib-channel',
      'gann-box','rectangle','circle','triangle'
    ].indexOf(toolType) >= 0;

    var content = document.createElement('div');
    content.className = 'dt-settings-content';

    if (hasLineViz) {
      content.appendChild(_buildSwatchRow('lineColor', 'Line', settings.lineColor || '#00ff88', function (val) {

        settings.lineColor = val;
        DrawingSettings.save(toolType, settings);
      }));
      content.appendChild(_buildStyleRow(settings.lineWidth || 2, settings.lineDash || [], function (w, d) {
        settings.lineWidth = w;
        settings.lineDash = d;
        DrawingSettings.save(toolType, settings);
      }));
    }

    if (hasFillViz) {
      content.appendChild(_buildSwatchRow('fillColor', 'Fill', settings.fillColor || 'rgba(0,255,136,0.2)', function (val) {

        settings.fillColor = val;
        DrawingSettings.save(toolType, settings);
      }));
      content.appendChild(_buildOpacityRow(settings.fillOpacity != null ? settings.fillOpacity : 0.12, function (val) {
        settings.fillOpacity = val;
        DrawingSettings.save(toolType, settings);
      }));
    }

    _settingsPanel.appendChild(content);
    _settingsPanel.appendChild(_buildCloseBtn());
  }

  function _buildSwatchRow(key, label, current, onChange) {
    var row = document.createElement('div');
    row.className = 'dt-settings-row';
    var lbl = document.createElement('span');
    lbl.className = 'dt-settings-label';
    lbl.textContent = label;
    row.appendChild(lbl);
    var swatches = document.createElement('div');
    swatches.className = 'dt-settings-swatches';
    _COLORS.forEach(function (c) {
      var sw = document.createElement('button');
      sw.className = 'dt-color-swatch';
      sw.style.background = c;
      if (c === current) sw.classList.add('active');
      sw.addEventListener('click', function () {
        swatches.querySelectorAll('.dt-color-swatch').forEach(function (s) { s.classList.remove('active'); });
        sw.classList.add('active');
        onChange(c);
      });
      swatches.appendChild(sw);
    });
    row.appendChild(swatches);
    return row;
  }

  function _buildStyleRow(width, dash, onChange) {
    var row = document.createElement('div');
    row.className = 'dt-settings-row dt-settings-style-row';
    var lbl = document.createElement('span');
    lbl.className = 'dt-settings-label';
    lbl.textContent = 'Style';
    row.appendChild(lbl);
    var inner = document.createElement('div');
    inner.className = 'dt-settings-style-inner';

    var widthSlider = document.createElement('input');
    widthSlider.type = 'range';
    widthSlider.min = 1;
    widthSlider.max = 5;
    widthSlider.step = 1;
    widthSlider.value = width;
    widthSlider.className = 'dt-width-slider';
    var widthVal = document.createElement('span');
    widthVal.className = 'dt-width-value';
    widthVal.textContent = width;
    widthSlider.addEventListener('input', function () {
      widthVal.textContent = widthSlider.value;
      onChange(parseInt(widthSlider.value, 10), dash);
    });
    inner.appendChild(widthSlider);
    inner.appendChild(widthVal);

    var dashRow = document.createElement('div');
    dashRow.className = 'dt-settings-dash-row';
    _LINE_STYLES.forEach(function (ls) {
      var btn = document.createElement('button');
      btn.className = 'dt-dash-btn';
      if (JSON.stringify(ls.dash) === JSON.stringify(dash)) btn.classList.add('active');
      var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('width', '36');
      svg.setAttribute('height', '10');
      svg.setAttribute('viewBox', '0 0 36 10');
      var line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('x1', '2');
      line.setAttribute('y1', '5');
      line.setAttribute('x2', '34');
      line.setAttribute('y2', '5');
      line.setAttribute('stroke', '#ccc');
      line.setAttribute('stroke-width', '2');
      if (ls.dash.length > 0) line.setAttribute('stroke-dasharray', ls.dash.join(','));
      svg.appendChild(line);
      btn.appendChild(svg);
      btn.addEventListener('click', function () {
        dashRow.querySelectorAll('.dt-dash-btn').forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        onChange(width, ls.dash);
      });
      dashRow.appendChild(btn);
    });
    inner.appendChild(dashRow);
    row.appendChild(inner);
    return row;
  }

  function _buildOpacityRow(current, onChange) {
    var row = document.createElement('div');
    row.className = 'dt-settings-row';
    var lbl = document.createElement('span');
    lbl.className = 'dt-settings-label';
    lbl.textContent = 'Opacity';
    row.appendChild(lbl);
    var inner = document.createElement('div');
    inner.className = 'dt-settings-opacity-inner';
    var slider = document.createElement('input');
    slider.type = 'range';
    slider.min = 0;
    slider.max = 100;
    slider.step = 1;
    slider.value = Math.round(current * 100);
    slider.className = 'dt-width-slider';
    var val = document.createElement('span');
    val.className = 'dt-width-value';
    val.textContent = Math.round(current * 100) + '%';
    slider.addEventListener('input', function () {
      var v = parseInt(slider.value, 10);
      val.textContent = v + '%';
      onChange(v / 100);
    });
    inner.appendChild(slider);
    inner.appendChild(val);
    row.appendChild(inner);
    return row;
  }

  function _buildCloseBtn() {
    var btn = document.createElement('button');
    btn.className = 'dt-settings-close';
    btn.innerHTML = '<i data-lucide="X" style="width:14px;height:14px;stroke-width:2;"></i>';
    btn.addEventListener('click', _hideSettings);
    return btn;
  }

  function _positionPanel() {
    if (!_toolbarEl || !_settingsPanel) return;
    var tr = _toolbarEl.getBoundingClientRect();
    var left = tr.right + 10;
    var top = tr.top;
    var pr = _settingsPanel.getBoundingClientRect();
    if (left + pr.width > window.innerWidth - 10) left = tr.left - pr.width - 10;
    if (top + pr.height > window.innerHeight - 10) top = window.innerHeight - pr.height - 10;
    if (top < 10) top = 10;
    _settingsPanel.style.left = left + 'px';
    _settingsPanel.style.top = top + 'px';
  }

  return { init: init };
})();
