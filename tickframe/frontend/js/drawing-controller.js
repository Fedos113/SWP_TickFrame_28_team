var DrawingController = (function () {
  var _manager = null;
  var _symbol = '';
  var _saveTimer = null;
  var _chart = null;
  var _series = null;
  var _container = null;
  var _saveDebounceMs = 500;
  var _unsubs = [];
  var _pendingDrawing = null;
  var _pendingAnchors = [];
  var _redactMode = false;
  var _saveGeneration = 0;


  function _createDrawingFactory() {
    var registry = DrawingLib.getToolRegistry();
    return function (type, data) {
      return registry.createDrawing(type, data.id, data.anchors || [], data.style || {}, data.options || {});
    };
  }

  function _scheduleSave() {
    if (_saveTimer) clearTimeout(_saveTimer);
    _saveTimer = setTimeout(_save, _saveDebounceMs);
  }

  async function _save() {
    if (!_manager || !_symbol) return;
    var generation = ++_saveGeneration;
    var symbolAtSave = _symbol;
    try {
      var exported = _manager.exportDrawings();
      if (generation !== _saveGeneration || symbolAtSave !== _symbol) return;
      await fetch('/api/drawings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol: symbolAtSave, drawings_data: exported }),
      });
    } catch (e) { console.error('drawing save error', e); }
  }


  var _highlightOrigins = {};
  var _pendingSymbol = null;

  function _wireManagerEvents() {
    _unsubs.push(_manager.on('drawing:added', function () {
      DrawingState.setDrawingCount(_manager.getAllDrawings().length);
      _scheduleSave();
    }));
    _unsubs.push(_manager.on('drawing:removed', function (e) {
      DrawingState.setDrawingCount(_manager.getAllDrawings().length);
      delete _highlightOrigins[e.drawingId];
      _scheduleSave();
    }));
    _unsubs.push(_manager.on('drawing:updated', function () {
      _scheduleSave();
    }));
    _unsubs.push(_manager.on('drawing:cleared', function () {
      DrawingState.setDrawingCount(0);
      DrawingState.setSelected(null);
      _highlightOrigins = {};
      _scheduleSave();
    }));
    _unsubs.push(_manager.on('drawing:selected', function (event) {
      DrawingState.setSelected(event.drawing || null);
      var d = event.drawing;
      if (d && !d.options.locked) {
        _highlightOrigins[d.id] = {
          lineColor: d.style.lineColor,
          lineWidth: d.style.lineWidth,
          lineDash: d.style.lineDash,
        };
        d.updateStyle({ lineColor: '#64B5F6', lineWidth: d.style.lineWidth || 2, lineDash: [5, 5] });
      }
      if (_manager && _manager.getActiveTool() === null) {
        _setChartInteraction(false);
      }
    }));
    _unsubs.push(_manager.on('drawing:deselected', function (event) {
      DrawingState.setSelected(null);
      var id = event.drawingId;
      if (id && _highlightOrigins[id]) {
        var d = _manager.getDrawing(id);
        if (d) d.updateStyle(_highlightOrigins[id]);
        delete _highlightOrigins[id];
      }
      if (_manager && _manager.getActiveTool() === null) {
        _setChartInteraction(true);
      }
    }));
    _unsubs.push(_manager.on('tool:changed', function (event) {
      if (!event.toolType && _pendingDrawing) {
        _cancelPending();
      }
      DrawingEvents.emit('tool:changed', { toolId: event.toolType || 'cursor' });
    }));
  }

  function _initDrawingCreation() {
    if (!_chart) return;

    var crosshairHandler = function (param) {
      try {
        if (!_pendingDrawing || !param.point || !_manager) return;
        if (_pendingAnchors.length === 0) return;
        var time = _chart.timeScale().coordinateToTime(param.point.x);
        var price = _series.coordinateToPrice(param.point.y);
        if (time === null || price === null) return;
        _pendingDrawing.setAnchors(_pendingAnchors.concat([{ time: time, price: price }]));
      } catch (e) {}
    };

    _chart.subscribeCrosshairMove(crosshairHandler);
    _unsubs.push(function () {
      _chart.unsubscribeCrosshairMove(crosshairHandler);
    });

    _chart.subscribeClick(function (param) {
      if (!_manager || !param.point) return;
      var toolType = _manager.getActiveTool();
      if (!toolType) {
        _enterRedactMode();
        return;
      }

      var time = _chart.timeScale().coordinateToTime(param.point.x);
      var price = _series.coordinateToPrice(param.point.y);
      if (time === null || price === null) return;

      var anchor = { time: time, price: price };
      var registry = DrawingLib.getToolRegistry();
      var toolDef = registry.get(toolType);
      if (!toolDef) return;

      if (_pendingDrawing) {
        var newAnchors = _pendingAnchors.concat([anchor]);
        _pendingAnchors = newAnchors;
        _pendingDrawing.setAnchors(newAnchors);
        if (newAnchors.length >= toolDef.requiredAnchors) {
          _pendingDrawing = null;
          _pendingAnchors = [];
          _enterRedactMode();
          _manager.setActiveTool(null);
          if (_manager.getSelectedDrawing()) {
            _setChartInteraction(false);
          }
        }
      } else {
        var defaults = window.DrawingSettings && DrawingSettings.getDefaults(toolType);
        var style = defaults ? {} : {};
        if (defaults) {
          if (defaults.lineColor) style.lineColor = defaults.lineColor;
          if (defaults.lineWidth) style.lineWidth = defaults.lineWidth;
          if (defaults.lineDash) style.lineDash = defaults.lineDash;
          if (defaults.fillColor) style.fillColor = defaults.fillColor;
          if (defaults.fillOpacity != null) style.fillOpacity = defaults.fillOpacity;
        }
        var drawing = registry.createDrawing(toolType, toolType + '-' + Date.now(), [anchor], style, { visible: true });
        if (drawing) {
          var multiClick = toolDef.requiredAnchors > 1;
          _pendingDrawing = multiClick ? drawing : null;
          _pendingAnchors = multiClick ? [anchor] : [];
          _manager.addDrawing(drawing);
          _manager.selectDrawing(drawing.id);
          if (!multiClick) {
            _enterRedactMode();
            _manager.setActiveTool(null);
            if (_manager.getSelectedDrawing()) {
              _setChartInteraction(false);
            }
          }
        }
      }
    });
  }

  function _setChartInteraction(redact) {
    if (!_chart) return;
    _chart.applyOptions({
      handleScroll: redact
        ? { pressedMouseMove: true, mouseWheel: true, horzTouchDrag: true, vertTouchDrag: true }
        : { pressedMouseMove: false, mouseWheel: false, horzTouchDrag: false, vertTouchDrag: false },
      handleScale: redact,
    });
  }

  function _enterRedactMode() {
    if (_redactMode) return;
    _redactMode = true;
    _setChartInteraction(true);
  }

  function _exitRedactMode() {
    if (!_redactMode) return;
    _redactMode = false;
    _setChartInteraction(false);
  }

  function _cancelPending() {
    if (_pendingDrawing) {
      _manager.removeDrawing(_pendingDrawing.id);
      _pendingDrawing = null;
    }
    _pendingAnchors = [];
  }

  function _boostHitAreas() {
    DrawingLib && Object.values(DrawingLib).forEach(function (c) {
      try {
        if (typeof c === 'function' && c.HIT_THRESHOLD !== void 0) c.HIT_THRESHOLD = 12;
      } catch (e) {}
    });

    var proto = DrawingLib.Drawing && DrawingLib.Drawing.prototype;
    if (proto) proto.hitTestAnchor = function (pt, vp) {
      var pts = this.getControlPoints(vp);
      if (!pts) return null;
      for (var i = 0; i < pts.length; i++) {
        var dx = pt.x - pts[i].x, dy = pt.y - pts[i].y;
        if (Math.sqrt(dx * dx + dy * dy) <= 14) return pts[i].index;
      }
      return null;
    };
  }

  function init(chart, series, container) {
    if (!window.DrawingLib) { console.warn('DrawingLib not loaded'); return; }
    try {
      teardown();
      _chart = chart;
      _series = series;
      _container = container;
      _boostHitAreas();
      _manager = new DrawingLib.DrawingManager();
      console.log('DrawingController: manager created');
      _manager.attach(chart, series, container);
      console.log('DrawingController: manager attached');
      _setChartInteraction(true);
      _wireManagerEvents();
      _initDrawingCreation();
      DrawingState.setDrawingCount(0);
      DrawingEvents.emit('controller:init');
      console.log('DrawingController: init complete');
    } catch (e) {
      console.error('DrawingController.init error:', e);
      _manager = null;
    }
  }

  function teardown() {
    _pendingDrawing = null;
    _pendingAnchors = [];
    _unsubs.forEach(function (u) { u(); });
    _unsubs = [];
    if (_saveTimer) { clearTimeout(_saveTimer); _saveTimer = null; }
    if (_manager) { _manager.detach(); _manager = null; }
    _exitRedactMode();
    _chart = null;
    _series = null;
    _container = null;
    _symbol = '';
    _pendingSymbol = null;
    DrawingState.reset();
  }

  function activateTool(toolType) {
    if (!_manager) return;
    _cancelPending();
    if (toolType === null) {
      _enterRedactMode();
      _manager.setActiveTool(null);
      if (_manager.getSelectedDrawing()) {
        _setChartInteraction(false);
      }
    } else {
      _exitRedactMode();
      _manager.setActiveTool(toolType);
    }
  }

  function deleteSelection() {
    if (!_manager) return;
    if (_pendingDrawing) { _cancelPending(); return; }
    var sel = _manager.getSelectedDrawing();
    if (sel) {
      _manager.removeDrawing(sel.id);
    }
  }

  function clearAll() {
    if (!_manager) return;
    _pendingDrawing = null;
    _manager.clearAll();
  }

  function updateDrawingStyle(id, style) {
    if (!_manager) return;
    var d = _manager.getDrawing(id);
    if (d) d.updateStyle(style);
  }

  function updateDrawingOptions(id, options) {
    if (!_manager) return;
    var d = _manager.getDrawing(id);
    if (d) d.updateOptions(options);
  }

  function setSymbol(symbol) {
    if (_manager && _symbol && _symbol !== symbol) {
      var sym = symbol;
      _pendingSymbol = sym;
      _save().then(function () {
        if (_pendingSymbol !== sym) return;
        _symbol = sym;
        _pendingDrawing = null;
        _manager.clearAll();
        _load(sym);
      });
    } else {
      _symbol = symbol;
      if (_manager) {
        _load(symbol);
      }
    }
  }

  async function _load(symbol) {
    if (!_manager) return;
    try {
      var resp = await fetch('/api/drawings?symbol=' + encodeURIComponent(symbol));
      if (resp.ok) {
        var data = await resp.json();
        if (data.drawings_data && data.drawings_data.length) {
          _manager.importDrawings(data.drawings_data, _createDrawingFactory());
        } else if (data.drawings && data.drawings.length) {
          var registry = DrawingLib.getToolRegistry();
          data.drawings.forEach(function (d) {
            var drawing = registry.createDrawing(d.type, d.id || String(d.type + '-' + Date.now()), d.points || d.anchors || [], d.opts || d.style || {}, {});
            if (drawing) _manager.addDrawing(drawing);
          });
        }
        _restorePatternDateRangeOptions();
      }
      DrawingState.setDrawingCount(_manager.getAllDrawings().length);
      if (window.DrawingEvents) DrawingEvents.emit('drawings:loaded', { symbol: symbol });
    } catch (e) { console.error('drawing load error', e); }
  }

  function _restorePatternDateRangeOptions() {
    if (!_manager) return;
    var all = _manager.getAllDrawings();
    if (!all) return;
    for (var i = 0; i < all.length; i++) {
      var d = all[i];
      if (d.type === 'pattern-date-range' && d.options && d.options._patternLabel) {
        d.setDateRangeOptions({
          labelText: d.options._patternLabel,
          showBars: false,
          showDays: false,
          showDates: true,
          filled: false,
        });
      }
    }
  }

  function load(symbol) {
    _symbol = symbol;
    _load(symbol);
  }

  function redraw() {
    if (_chart) { try { _chart.requestUpdate(); } catch (e) {} }
  }

  function getManager() { return _manager; }
  function getSymbol() { return _symbol; }
  function cancelPending() { _cancelPending(); }

  return {
    init: init,
    teardown: teardown,
    activateTool: activateTool,
    deleteSelection: deleteSelection,
    clearAll: clearAll,
    updateDrawingStyle: updateDrawingStyle,
    updateDrawingOptions: updateDrawingOptions,
    setSymbol: setSymbol,
    load: load,
    redraw: redraw,
    getManager: getManager,
    getSymbol: getSymbol,
    cancelPending: cancelPending,
  };
})();
