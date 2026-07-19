var DrawingSettings = (function () {
  var STORAGE_KEY = 'tickframe_drawing_settings';
  var _defaults = {};

  function _defaultForType(toolType) {
    var hasFill = ['rectangle', 'circle', 'triangle', 'parallel-channel', 'regression-trend',
      'fib-retracement', 'fib-extension', 'fib-channel', 'fib-time-zone',
      'gann-box', 'gann-fan'].indexOf(toolType) >= 0;
    var def = {
      lineColor: '#00ff88',
      lineWidth: 2,
      lineDash: [],
      fillOpacity: 0.12,
    };
    if (hasFill) def.fillColor = 'rgba(0, 255, 136, 0.12)';
    return def;

  }

  function load() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        _defaults = JSON.parse(raw);
      } else {
        _defaults = {};
      }
    } catch (e) {
      _defaults = {};
    }
  }

  function save() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(_defaults));
    } catch (e) {}
  }

  function getDefaults(toolType) {
    var base = _defaultForType(toolType);
    var saved = _defaults[toolType];
    if (saved) {
      if (saved.lineColor != null) base.lineColor = saved.lineColor;
      if (saved.lineWidth != null) base.lineWidth = saved.lineWidth;
      if (saved.lineDash != null) base.lineDash = saved.lineDash;
      if (saved.fillColor != null) base.fillColor = saved.fillColor;
      if (saved.fillOpacity != null) base.fillOpacity = saved.fillOpacity;
    }
    return base;
  }

  function setDefaults(toolType, settings) {
    _defaults[toolType] = settings;
    save();
  }

  function save(toolType, settings) {
    var existing = _defaults[toolType] || {};
    for (var key in settings) {
      if (settings.hasOwnProperty(key)) {
        existing[key] = settings[key];
      }
    }
    _defaults[toolType] = existing;
    save();
  }

  function getAll() {
    return _defaults;
  }

  load();
  return {
    getDefaults: getDefaults,
    setDefaults: setDefaults,
    save: save,
    getAll: getAll,
    load: load,
  };
})();
