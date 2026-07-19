/* ── Globals ──────────────────────────────────────────────── */
var chartInitMode = null;
var _patternFilter = {
  'Classic H&S': true, 'Inverse H&S': true,
  'Double Top': true, 'Double Bottom': true,
};
// Expose the filter on window so the pattern-filter checkboxes (app.js) and
// renderPatterns() share a single source of truth. Without this, the toolbar
// checkboxes wrote to a separate window._patternFilter object and the render
// filter (which reads window._patternFilter) never took effect.
window._patternFilter = _patternFilter;

var _allCoinPatterns = {};

/* ── Per-coin data store ─────────────────────────────────── */
var _coinData = {};      // symbol → { candles:[], ws:null, interval:'5m', visibleRange:null, patterns:[] }
var _activeSymbol = null;
var _activeInterval = '5m';
var _chart = null;       // single Lightweight Charts instance
var _candleSeries = null;
var _volumeSeries = null;
var _volumeSmaSeries = null;
var _lastCandles = [];   // alias for active coin's candles
var _patterns = [];
var _patternMarkers = [];
var _patternListenerRegistered = false;
var _volumeSmaBuffer = [];
var _volumeSmaSum = 0;
var _latestSeenTime = 0;
var _isSettingRange = false;
var _loadMoreTimer = null;
var _wsReconnect = false;
var _wsConnId = 0;

/* ── Utility functions ───────────────────────────────────── */

function _themeColors(dark) {
  var font = '"JetBrains Mono","Fira Code","SF Mono",Consolas,Menlo,monospace';
  if (dark) {
    return {
      bg: '#02050a', text: '#7fbf97', grid: 'rgba(0,255,136,0.06)', border: '#123322',
      up: '#00ff88', down: '#ff4d5e', volUp: 'rgba(0,255,136,0.45)', volDown: 'rgba(255,77,94,0.45)',
      sma: '#00c46a', pattern: '#00ff88', font: font,
    };
  }
  return {
    bg: '#ffffff', text: '#3d6552', grid: 'rgba(15,80,50,0.08)', border: '#dbe6df',
    up: '#0aa55f', down: '#e24d4d', volUp: 'rgba(10,165,95,0.4)', volDown: 'rgba(226,77,77,0.4)',
    sma: '#0c8a52', pattern: '#0aa55f', font: font,
  };
}

function _formatChartPrice(price) {
  if (price == null || isNaN(price)) return '--';
  var abs = Math.abs(price);
  var dec;
  if (abs >= 1000) dec = 2;
  else if (abs >= 100) dec = 3;
  else if (abs >= 10) dec = 4;
  else if (abs >= 1) dec = 5;
  else if (abs >= 0.01) dec = 6;
  else dec = 8;
  return price.toFixed(dec).replace(/\.?0+$/, '');
}

function calculateSMA(data, period) {
  var result = [];
  var sum = 0;
  for (var i = 0; i < data.length; i++) {
    sum += data[i].value;
    if (i >= period) sum -= data[i - period].value;
    if (i >= period - 1) result.push({ time: data[i].time, value: sum / period });
  }
  return result;
}

var _intervalToSeconds = (function () {
  var cache = {};
  return function (iv) {
    if (cache[iv] !== undefined) return cache[iv];
    var m = iv.match(/^(\d+)([smhd])$/);
    if (!m) { cache[iv] = 300; return 300; }
    var n = parseInt(m[1]), u = m[2];
    var s = u === 's' ? n : u === 'm' ? n * 60 : u === 'h' ? n * 3600 : n * 86400;
    cache[iv] = s;
    return s;
  };
})();

function showLoading(show) {
  var el = document.getElementById('chartLoading');
  if (el) el.classList.toggle('visible', show);
}

/* ── Candle fetching / loading ───────────────────────────── */

function fetchCandles(symbol, limit, before, interval) {
  var iv = interval || _activeInterval || '5m';
  var url = '/api/coins/' + symbol + '/candles?interval=' + iv + '&limit=' + (limit || 10000);
  if (before != null) url += '&before=' + before;
  return fetch(url).then(function (resp) {
    if (!resp.ok) throw new Error('fetchCandles failed');
    return resp.json();
  }).then(function (payload) {
    var data = Array.isArray(payload) ? payload : (payload.candles || []);
    return data.map(function (c) {
      return { time: c.time || c.t || 0, open: +c.open, high: +c.high, low: +c.low, close: +c.close, volume: +c.volume };
    });
  });
}

function loadCandles(symbol, limit, before, interval) {
  return fetchCandles(symbol, limit, before, interval).then(function (candles) {
    if (!_coinData[symbol]) _coinData[symbol] = { candles: [], ws: null, interval: _activeInterval, patterns: [] };
    _coinData[symbol].candles = candles;
    if (symbol === _activeSymbol) {
      _lastCandles = candles;
      _setData(candles);
    }
  });
}

/* ── Chart data rendering ────────────────────────────────── */

function _setData(candles) {
  if (!_candleSeries) return;
  _lastCandles = candles;
  if (_activeSymbol && _coinData[_activeSymbol]) {
    _coinData[_activeSymbol].candles = candles;
  }
  _candleSeries.setData(candles);
  _updatePriceFormat();
  _rebuildIndicators();
  if (typeof window._onCandlesUpdated === 'function') {
    window._onCandlesUpdated(_activeSymbol);
  }
}

function _updatePriceFormat() {
  if (!_candleSeries || !_lastCandles.length) return;
  var last = _lastCandles[_lastCandles.length - 1];
  var abs = Math.abs(last.close);
  var precision, minMove;
  if (abs >= 1000) { precision = 2; minMove = 0.01; }
  else if (abs >= 100) { precision = 3; minMove = 0.001; }
  else if (abs >= 10) { precision = 4; minMove = 0.0001; }
  else if (abs >= 1) { precision = 5; minMove = 0.00001; }
  else if (abs >= 0.01) { precision = 6; minMove = 0.000001; }
  else { precision = 8; minMove = 0.00000001; }
  _candleSeries.applyOptions({ priceFormat: { type: 'price', precision: precision, minMove: minMove } });
}

function _rebuildIndicators() {
  _updateVolumeIndicators();
}

function _updateVolumeIndicators() {
  if (!_volumeSeries || !_volumeSmaSeries) return;
  var candles = _lastCandles;
  if (!candles || candles.length < 20) return;
  var t = _themeColors(document.body.classList.contains('light') ? false : true);
  var volData = [];
  var volValues = [];
  for (var i = 0; i < candles.length; i++) {
    var c = candles[i];
    volData.push({ time: c.time, value: c.volume || 0, color: c.close >= c.open ? t.volUp : t.volDown });
    volValues.push({ time: c.time, value: c.volume || 0 });
  }
  _volumeSeries.setData(volData);
  _volumeSmaBuffer = volValues.slice(-20);
  _volumeSmaSum = 0;
  for (var j = 0; j < _volumeSmaBuffer.length; j++) {
    _volumeSmaSum += _volumeSmaBuffer[j].value;
  }
  _volumeSmaSeries.setData(calculateSMA(volValues, 20));
}

function updateRealtime(time, close, volume, open) {
  if (!_volumeSeries) return;
  var t = _themeColors(document.body.classList.contains('light') ? false : true);
  _volumeSeries.update({ time: time, value: volume || 0, color: close >= open ? t.volUp : t.volDown });
  if (!_lastCandles.length) return;
  var value = volume || 0;
  var buf = _volumeSmaBuffer;
  var lastBuf = buf.length ? buf[buf.length - 1] : null;
  if (lastBuf && lastBuf.time === time) {
    _volumeSmaSum += value - lastBuf.value;
    buf[buf.length - 1] = { time: time, value: value };
  } else {
    buf.push({ time: time, value: value });
    _volumeSmaSum += value;
    if (buf.length > 20) { _volumeSmaSum -= buf[0].value; buf.shift(); }
  }
  if (buf.length >= 20 && _volumeSmaSeries) {
    _volumeSmaSeries.update({ time: time, value: _volumeSmaSum / 20 });
  }
}

function updateLatestPrice(price) {
  if (typeof price !== 'number' || !isFinite(price)) return;
  if (!_lastCandles.length || !_candleSeries) return;
  var last = _lastCandles[_lastCandles.length - 1];
  if (!last) return;
  var updated = { time: last.time, open: last.open, high: last.high, low: last.low, close: price, volume: last.volume };
  if (!updated.time || !Number.isFinite(updated.open) || !Number.isFinite(updated.high) || !Number.isFinite(updated.low)) return;
  _lastCandles[_lastCandles.length - 1] = updated;
  if (_activeSymbol && _coinData[_activeSymbol]) {
    _coinData[_activeSymbol].candles = _lastCandles;
  }
  _candleSeries.update(updated);
}

/* ── Chart creation ──────────────────────────────────────── */

function _createChart(container) {
  if (_chart) return;
  if (typeof LightweightCharts === 'undefined') {
    console.error('LightweightCharts library not loaded');
    return;
  }
  var rect = container.getBoundingClientRect();
  var t = _themeColors(document.body.classList.contains('light') ? false : true);

  var lwChart = LightweightCharts.createChart(container, {
    width: Math.max(300, rect.width),
    height: Math.max(200, rect.height),
    layout: {
      background: { type: 'solid', color: t.bg },
      textColor: t.text,
      fontFamily: t.font,
      panes: { separatorColor: t.border, separatorHoverColor: t.up, enableResize: true },
    },
    grid: { vertLines: { color: t.grid }, horzLines: { color: t.grid } },
    rightPriceScale: { borderColor: t.border },
    timeScale: { visible: true, timeVisible: true, secondsVisible: false, borderColor: t.border },
    crosshair: { mode: LightweightCharts.CrosshairMode.Normal },
    localization: { priceFormatter: _formatChartPrice },
  });

  var CSeries = window.LightweightCharts.CandlestickSeries || 'Candlestick';
  var candleSeries = lwChart.addSeries(CSeries, {
    upColor: t.up, downColor: t.down, borderVisible: false,
    wickUpColor: t.up, wickDownColor: t.down,
    priceFormat: { type: 'price', precision: 6, minMove: 0.000001 },
  });

  var volHS = window.LightweightCharts.HistogramSeries;
  var volLS = window.LightweightCharts.LineSeries;
  var volumeSeries = lwChart.addSeries(volHS, { priceFormat: { type: 'volume' }, lastValueVisible: false, priceLineVisible: false }, 1);
  var volumeSmaSeries = lwChart.addSeries(volLS, { color: '#FF9800', lineWidth: 2, lastValueVisible: false, priceLineVisible: false }, 1);

  try {
    var pricePane = lwChart.panes()[0];
    var volPane = lwChart.panes()[1];
    if (pricePane) pricePane.setStretchFactor(4);
    if (volPane) volPane.setStretchFactor(1);
  } catch (e) {}

  _chart = lwChart;
  window.chart = lwChart;
  window.candleSeries = candleSeries;
  _candleSeries = candleSeries;
  _volumeSeries = volumeSeries;
  _volumeSmaSeries = volumeSmaSeries;

  window.addEventListener('resize', function () {
    if (!_chart) return;
    var r = container.getBoundingClientRect();
    _chart.resize(Math.max(300, r.width), Math.max(200, r.height));
  });

  lwChart.timeScale().subscribeVisibleTimeRangeChange(function (range) {
    if (!range || !_lastCandles.length) return;
    if (_isSettingRange) return;
    if (range.from < _lastCandles[0].time) {
      if (_loadMoreTimer) clearTimeout(_loadMoreTimer);
      _loadMoreTimer = setTimeout(function () { _loadMoreBefore(_lastCandles[0].time); }, 400);
    }
    var maxTo = _maxFutureTime();
    if (range.to > maxTo) {
      _isSettingRange = true;
      _chart.timeScale().setVisibleRange({ from: range.from, to: maxTo });
      _isSettingRange = false;
    }
  });

  if (window.TFDraw) {
    try {
      if (!window.__tfd_initialized) {
        window.TFDraw.init(lwChart, candleSeries, container);
        window.__tfd_initialized = true;
      }
      window.TFDraw.setSymbol(_activeSymbol || 'BTCUSDT');
    } catch (e) {}
  }
}

function _maxFutureTime() {
  if (!_lastCandles.length) return 0;
  var base = _latestSeenTime || _lastCandles[_lastCandles.length - 1].time;
  return base + 500 * _intervalToSeconds(_activeInterval);
}

function _loadMoreBefore(before) {
  if (!_activeSymbol) return;
  fetchCandles(_activeSymbol, 5000, before).then(function (newCandles) {
    if (!newCandles.length) return;
    var merged = newCandles.concat(_lastCandles);
    var seen = {};
    var deduped = [];
    for (var i = 0; i < merged.length; i++) {
      var t = merged[i].time;
      if (!seen[t]) { seen[t] = true; deduped.push(merged[i]); }
    }
    if (deduped.length > 55000) deduped = deduped.slice(-55000);
    _lastCandles = deduped;
    if (_activeSymbol && _coinData[_activeSymbol]) _coinData[_activeSymbol].candles = deduped;
    if (_candleSeries) _candleSeries.setData(deduped);
    _rebuildIndicators();
  });
}

function resetChartScale() {
  if (!_chart) return;
  var ps = _chart.priceScale('right');
  ps.applyOptions({ autoScale: false });
  ps.applyOptions({ autoScale: true });
  if (_lastCandles && _lastCandles.length > 0) {
    var len = _lastCandles.length;
    var viewEnd = _lastCandles[len - 1].time;
    var startIdx = Math.max(0, len - 301);
    var viewFrom = _lastCandles[startIdx].time;
    _isSettingRange = true;
    _chart.timeScale().setVisibleRange({ from: viewFrom, to: viewEnd });
    _isSettingRange = false;
  } else {
    _chart.timeScale().fitContent();
  }
}

/* ── WebSocket ───────────────────────────────────────────── */

function _connectWs(symbol, interval) {
  if (!symbol) return;
  var existing = _coinData[symbol];
  if (existing && existing.ws) {
    try { existing.ws.close(); } catch (e) {}
    existing.ws = null;
  }
  var connId = ++_wsConnId;
  _wsReconnect = true;
  var proto = (location.protocol === 'https:') ? 'wss' : 'ws';
  var url = proto + '://' + location.host + '/ws/candles/' + symbol + '?interval=' + (interval || _activeInterval || '5m');
  var ws = new WebSocket(url);
  if (!_coinData[symbol]) _coinData[symbol] = { candles: [], ws: null, interval: interval || _activeInterval, patterns: [] };
  _coinData[symbol].ws = ws;
  ws.onmessage = function (ev) {
    try {
      var msg = JSON.parse(ev.data);
      if (msg.type === 'snapshot' && msg.candles) { _applySnapshot(symbol, msg.candles); }
      else if (msg.type === 'update' && msg.candle) { _applyUpdate(symbol, msg.candle); }
    } catch (e) {}
  };
  ws.onclose = function () {
    if (connId === _wsConnId && _wsReconnect) {
      setTimeout(function () { _connectWs(symbol, interval); }, 2000);
    }
  };
}

function _disconnectWs(symbol) {
  var entry = _coinData[symbol];
  if (entry && entry.ws) {
    _wsConnId++;
    try { entry.ws.close(); } catch (e) {}
    entry.ws = null;
  }
}

function _getCoinCandles(symbol) {
  if (_coinData[symbol]) return _coinData[symbol].candles || [];
  return [];
}

function _setCoinCandles(symbol, candles) {
  if (!_coinData[symbol]) _coinData[symbol] = { candles: [], ws: null, interval: _activeInterval, patterns: [] };
  _coinData[symbol].candles = candles;
}

function _applySnapshot(symbol, newCandles) {
  var normalized = [];
  for (var i = 0; i < newCandles.length; i++) {
    var c = newCandles[i];
    normalized.push({ time: c.time, open: +c.open, high: +c.high, low: +c.low, close: +c.close, volume: +c.volume });
  }
  if (!normalized.length) return;
  var existing = _getCoinCandles(symbol);
  if (existing.length) {
    var seen = {};
    for (var j = 0; j < existing.length; j++) seen[existing[j].time] = existing[j];
    for (var k = 0; k < normalized.length; k++) seen[normalized[k].time] = normalized[k];
    var times = Object.keys(seen).map(Number).sort(function (a, b) { return a - b; });
    var merged = [];
    var maxc = 55000;
    var start = times.length > maxc ? times.length - maxc : 0;
    for (var m = start; m < times.length; m++) merged.push(seen[times[m]]);
    _setCoinCandles(symbol, merged);
    if (symbol === _activeSymbol) {
      _lastCandles = merged;
      if (_candleSeries) _candleSeries.setData(merged);
      _rebuildIndicators();
      if (typeof window._onCandlesUpdated === 'function') window._onCandlesUpdated(symbol);
    }
  } else {
    _setCoinCandles(symbol, normalized);
    if (symbol === _activeSymbol) {
      _lastCandles = normalized;
      if (_candleSeries) _candleSeries.setData(normalized);
      _rebuildIndicators();
      if (typeof window._onCandlesUpdated === 'function') window._onCandlesUpdated(symbol);
    }
  }
  _latestSeenTime = _getCoinCandles(symbol).length ? _getCoinCandles(symbol)[_getCoinCandles(symbol).length - 1].time : 0;
}

function _applyUpdate(symbol, candle) {
  if (!candle || !candle.time) return;
  var point = { time: candle.time, open: +candle.open, high: +candle.high, low: +candle.low, close: +candle.close, volume: +candle.volume };
  if (symbol === _activeSymbol && _candleSeries) _candleSeries.update(point);
  if (point.time > _latestSeenTime) _latestSeenTime = point.time;
  var candles = _getCoinCandles(symbol);
  if (candles.length) {
    var last = candles[candles.length - 1];
    if (last.time === point.time) { candles[candles.length - 1] = point; }
    else { candles.push(point); if (candles.length > 55000) candles = candles.slice(-55000); }
    _setCoinCandles(symbol, candles);
    if (symbol === _activeSymbol) {
      _lastCandles = candles;
      updateRealtime(point.time, point.close, point.volume, point.open);
    }
  }
}

/* ── Pattern rendering ───────────────────────────────────── */

function _patternColor(type, dark) {
  var map = {
    'Classic H&S': dark ? '#ff6b6b' : '#e03131',
    'Inverse H&S': dark ? '#ffd43b' : '#f08c00',
    'Double Top': dark ? '#748ffc' : '#4263eb',
    'Double Bottom': dark ? '#69db7c' : '#2f9e44',
  };
  return map[type] || (dark ? '#00ff88' : '#0aa55f');
}

function _formatPatternLabel(pat) {
  var pct = (pat.confidence * 100).toFixed(0);
  return pat.pattern_type + ' ' + pct + '%';
}

function renderPatterns(patterns) {
  if (!_patternListenerRegistered && window.DrawingEvents) {
    _patternListenerRegistered = true;
    DrawingEvents.on('drawings:loaded', function (event) {
      var sym = event && event.symbol;
      if (sym && sym === _activeSymbol) {
        var cached = _allCoinPatterns[sym] || [];
        if (cached.length) renderPatterns(cached);
      }
    });
  }
  _clearPatterns();
  if (!_chart || !patterns || !patterns.length) return;
  var filtered = [];
  for (var i = 0; i < patterns.length; i++) {
    var p = patterns[i];
    if (window._patternFilter && window._patternFilter[p.pattern_type] !== false) filtered.push(p);
  }
  if (!filtered.length) return;
  var data = _lastCandles || [];
  var segments = [];
  for (var j = 0; j < filtered.length; j++) {
    var p2 = filtered[j];
    var startT, endT;
    if (p2.startTime !== undefined && p2.endTime !== undefined) {
      startT = p2.startTime;
      endT = p2.endTime;
    } else {
      var ts = p2.timestamp;
      var idx = -1;
      for (var d = 0; d < data.length; d++) { if (data[d].time === ts) { idx = d; break; } }
      if (idx === -1) { startT = ts; endT = ts; }
      else {
        var startIdx = Math.max(0, idx - 49);
        startT = data[startIdx].time;
        endT = ts;
      }
    }
    segments.push({ start: startT, end: endT, patterns: [p2] });
  }
  segments.sort(function (a, b) { return a.start - b.start; });
  var merged = [];
  for (var s = 0; s < segments.length; s++) {
    var seg = segments[s];
    if (merged.length === 0) { merged.push(seg); continue; }
    var last = merged[merged.length - 1];
    if (seg.start <= last.end) { last.end = Math.max(last.end, seg.end); last.patterns = last.patterns.concat(seg.patterns); }
    else { merged.push(seg); }
  }
  var dark = !document.body.classList.contains('light');
  var markers = [];
  for (var m = 0; m < merged.length; m++) {
    var seg2 = merged[m];
    var segMaxPrice = -Infinity;
    var segMinPrice = Infinity;
    for (var di = 0; di < data.length; di++) {
      if (data[di].time >= seg2.start && data[di].time <= seg2.end) {
        segMaxPrice = Math.max(segMaxPrice, data[di].high);
        segMinPrice = Math.min(segMinPrice, data[di].low);
      }
    }
    if (!isFinite(segMaxPrice)) continue;
    var topPattern = null;
    for (var pm = 0; pm < seg2.patterns.length; pm++) {
      if (!topPattern || seg2.patterns[pm].confidence > topPattern.confidence) topPattern = seg2.patterns[pm];
    }
    if (!topPattern) continue;
    var pad = (segMaxPrice - segMinPrice) * 0.15;
    var linePrice = segMaxPrice + pad;
    try {
      if (window.DrawingLib && window.DrawingController) {
        var registry = DrawingLib.getToolRegistry();
        var drawingId = 'pattern-' + Date.now() + '-' + m;
        var drawing = registry.createDrawing(
          'pattern-date-range',
          drawingId,
          [
            { time: seg2.start, price: linePrice },
            { time: seg2.end, price: linePrice },
          ],
          {
            lineColor: '#00ff88',
            lineWidth: 1,
            fillColor: 'rgba(0,255,136,0.1)',
          },
          { visible: true, locked: false, _patternLabel: _formatPatternLabel(topPattern) }
        );

        if (drawing) {
          drawing.setDateRangeOptions({
            labelText: _formatPatternLabel(topPattern),

            showBars: false,
            showDays: false,
            showDates: true,
            filled: false,
          });
          var manager = DrawingController.getManager();
          if (manager) manager.addDrawing(drawing);
        }
      }
    } catch (e) {}
    var markersForSeg = [];
    for (var pn = 0; pn < seg2.patterns.length; pn++) {
      var pp = seg2.patterns[pn];
      var pColor = _patternColor(pp.pattern_type, dark);
      var pLabel = _formatPatternLabel(pp);
      markersForSeg.push({ time: seg2.start, position: 'aboveBar', color: pColor, shape: 'arrowDown', text: pLabel });
    }
    Array.prototype.push.apply(markers, markersForSeg);
  }
  if (_candleSeries && typeof _candleSeries.setMarkers === 'function') {
    _candleSeries.setMarkers(markers);
    _patternMarkers = markers;
  }
  _patterns = patterns;
}

function _clearPatterns() {
  if (window.DrawingController) {
    var manager = DrawingController.getManager();
    if (manager) {
      var all = manager.getAllDrawings();
      if (all) {
        for (var i = 0; i < all.length; i++) {
          if (all[i].type === 'pattern-date-range' && all[i].id && all[i].id.indexOf('pattern-') === 0) {
            try { manager.removeDrawing(all[i].id); } catch (e) {}
          }
        }
      }
    }
  }
  if (_candleSeries && typeof _candleSeries.setMarkers === 'function') _candleSeries.setMarkers([]);
  _patternMarkers = [];
  _patterns = [];
}

/* ── Theme ────────────────────────────────────────────────── */

function applyChartTheme(dark) {
  if (!_chart) return;
  var t = _themeColors(dark);
  _chart.applyOptions({
    layout: { background: { type: 'solid', color: t.bg }, textColor: t.text, fontFamily: t.font },
    grid: { vertLines: { color: t.grid }, horzLines: { color: t.grid } },
    rightPriceScale: { borderColor: t.border },
    timeScale: { borderColor: t.border },
    localization: { priceFormatter: _formatChartPrice },
  });
  if (_candleSeries) { _candleSeries.applyOptions({ upColor: t.up, downColor: t.down, wickUpColor: t.up, wickDownColor: t.down }); }
  if (_volumeSmaSeries) _volumeSmaSeries.applyOptions({ color: t.sma });
  if (_lastCandles && _lastCandles.length) _rebuildIndicators();
}

/* ── Chart lifecycle ─────────────────────────────────────── */

function isChartingLibAvailable() {
  return typeof TradingView !== 'undefined';
}

function createChart() {
  var container = document.getElementById('chart');
  if (!container) return;

  if (isChartingLibAvailable()) {
    chartInitMode = 'advanced';
    createAdvancedChart(container);
  } else {
    chartInitMode = 'lightweight';
    createLightweightCharts(container);
  }
}

function createLightweightCharts(container) {
  _createChart(container);
  if (!_chart) return;

  var symbols = window._coinList || [];
  for (var i = 0; i < symbols.length; i++) {
    var sym = symbols[i].symbol || symbols[i];
    if (!_coinData[sym]) _coinData[sym] = { candles: [], ws: null, interval: _activeInterval, patterns: [] };
  }

  preloadDefault();
}

function preloadDefault() {
  var symbols = window._coinList || [];
  if (!symbols.length) return;
  var defaultSymbol = symbols[0].symbol || symbols[0];
  switchCoin(defaultSymbol, _activeInterval);
  loadCandles(defaultSymbol, 10000).then(function () {
    var candles = _coinData[defaultSymbol] ? _coinData[defaultSymbol].candles : [];
    if (candles.length > 0) _connectWs(defaultSymbol, _activeInterval);
  }).catch(function () {});
}

function switchCoin(symbol, interval) {
  if (!symbol) return;
  if (symbol === _activeSymbol && interval === _activeInterval) return;

  var prevSymbol = _activeSymbol;
  if (prevSymbol && _chart) {
    try { _coinData[prevSymbol].visibleRange = _chart.timeScale().getVisibleRange(); } catch (e) {}
  }

  _activeSymbol = symbol;
  _activeInterval = interval || _activeInterval || '5m';
  window._currentInterval = _activeInterval;

  if (!_coinData[symbol]) _coinData[symbol] = { candles: [], ws: null, interval: _activeInterval, patterns: [] };
  _lastCandles = _coinData[symbol].candles || [];

  if (_lastCandles.length && _candleSeries) {
    _setData(_lastCandles);
  } else if (_candleSeries) {
    _candleSeries.setData([]);
  }

  if (window.TFDraw) {
    try { window.TFDraw.setSymbol(symbol); } catch (e) {}
  }

  var saved = _coinData[symbol];
  if (saved && saved.visibleRange && _chart) {
    try { _isSettingRange = true; _chart.timeScale().setVisibleRange(saved.visibleRange); _isSettingRange = false; }
    catch (e) { resetChartScale(); }
  } else { resetChartScale(); }

  if (_lastCandles.length === 0) {
    showLoading(true);
    loadCandles(symbol, 10000).then(function () {
      var candles = _coinData[symbol] ? _coinData[symbol].candles : [];
      if (candles.length > 0) _connectWs(symbol, _activeInterval);
    }).catch(function () {}).then(function () {
      showLoading(false);
    });
  } else if (!_coinData[symbol].ws || _coinData[symbol].ws.readyState !== 1) {
    _connectWs(symbol, _activeInterval);
  }
}

function switchInterval(interval) {
  if (!_activeSymbol) return;
  showLoading(true);
  _disconnectWs(_activeSymbol);
  _activeInterval = interval;
  window._currentInterval = interval;
  loadCandles(_activeSymbol, 10000, null, interval).then(function () {
    resetChartScale();
    _connectWs(_activeSymbol, interval);
  }).catch(function () {}).then(function () {
    showLoading(false);
  });
}

/* ── Advanced chart mode ─────────────────────────────────── */

function createAdvancedChart(container) {
  var datafeed = new TickFrameDatafeed(window.currentSymbol || 'BTCUSDT', '5m');
  window._datafeed = datafeed;
  var widgetOptions = {
    symbol: window.currentSymbol || 'BTCUSDT',
    interval: '5m',
    container: container,
    datafeed: datafeed,
    library_path: '/lib/charting_library/',
    theme: 'Dark',
    time_frames: [
      { text: '1y', resolution: '1d', description: '1 Year' },
      { text: '6m', resolution: '4h', description: '6 Months' },
      { text: '3m', resolution: '1h', description: '3 Months' },
      { text: '1m', resolution: '15m', description: '1 Month' },
      { text: '7d', resolution: '5m', description: '7 Days' },
      { text: '3d', resolution: '5m', description: '3 Days' },
      { text: '1d', resolution: '5m', description: '1 Day' },
    ],
    fullscreen: false, autosize: true,
    overrides: {
      'paneProperties.background': '#000000',
      'paneProperties.vertGridProperties.color': '#1f2937',
      'paneProperties.horzGridProperties.color': '#1f2937',
      'scalesProperties.textColor': '#d1d4dc',
    },
    disabled_features: ['header_widget', 'header_symbol_search', 'header_compare', 'header_chart_type', 'header_settings', 'header_indicators', 'timeframes_toolbar'],
    enabled_features: ['show_drawing_toolbar'],
    custom_css_url: '/css/tradingview-custom.css',
  };
  var tvWidget = new TradingView.widget(widgetOptions);
  tvWidget.onChartReady(function () {
    window.chart = tvWidget;
    tvWidget.chart().dataReady(function () {
      window.TFChart.loadCandles(window.currentSymbol || 'BTCUSDT', '5m');
    });
  });
}

/* ── TFChart API ─────────────────────────────────────────── */

window.TFChart = {
  createChart: createChart,

  setLoadingState: function (visible) {
    showLoading(visible);
  },

  loadCandles: function (symbol, interval) {
    if (chartInitMode === 'advanced') {
      window.currentSymbol = symbol;
      showLoading(true);
      if (window._datafeed) { window._datafeed.symbol = symbol; window._datafeed.interval = interval; window._datafeed.reconnectWs(); }
      if (window.chart && typeof window.chart.setSymbol === 'function') window.chart.setSymbol(symbol, interval);
      setTimeout(function () { showLoading(false); }, 5000);
      return Promise.resolve();
    }
    switchCoin(symbol, interval);
    return Promise.resolve();
  },

  startCandleWs: function (symbol, interval) {
    if (chartInitMode === 'advanced') return;
    _connectWs(symbol || _activeSymbol, interval || _activeInterval);
  },

  stopCandleWs: function () {
    if (chartInitMode === 'advanced') return;
    _disconnectWs(_activeSymbol);
  },

  switchCoin: function (symbol, interval) { switchCoin(symbol, interval); },
  switchInterval: function (interval) { switchInterval(interval); },

  applyChartTheme: function (dark) {
    if (chartInitMode === 'advanced') {
      if (window.chart && typeof window.chart.changeTheme === 'function') window.chart.changeTheme(dark ? 'Dark' : 'Light');
      return;
    }
    applyChartTheme(dark);
  },

  setActiveSymbol: function (symbol) { window.currentSymbol = symbol; },

  getCurrentBars: function () { return _lastCandles; },
  mainChart: function () { return _chart; },

  updateIndicators: function () { _rebuildIndicators(); },
  updateRealtime: function (time, close, volume, open) { updateRealtime(time, close, volume, open); },
  updateLatestPrice: function (price) { updateLatestPrice(price); },
  resetChartScale: function () { resetChartScale(); },

  renderPatterns: function (patterns) {
    if (_activeSymbol) _allCoinPatterns[_activeSymbol] = patterns || [];
    renderPatterns(patterns || []);
  },

  clearPatternsFrontend: function () {
    if (_activeSymbol) _allCoinPatterns[_activeSymbol] = [];
    _clearPatterns();
    var btn = document.querySelector('.analyze-btn');
    if (btn) {
      var label = btn.querySelector('.analyze-btn-label');
      if (label) label.textContent = 'ANALYZE';
      btn.disabled = false;
      btn.classList.remove('analyzing');
    }
  },

  getFilteredPatterns: function () {
    if (!_patterns) return [];
    var filtered = [];
    for (var i = 0; i < _patterns.length; i++) {
      if (_patternFilter[_patterns[i].pattern_type] === true) filtered.push(_patterns[i]);
    }
    return filtered;
  },

  togglePatternFilter: function () {
    var el = document.getElementById('patternFilterModal');
    if (el) el.classList.toggle('hidden');
  },

  onPatternFilterChange: function () {
    var patterns = _activeSymbol ? (_allCoinPatterns[_activeSymbol] || []) : [];
    renderPatterns(patterns);
  },

  saveCoinState: function (symbol, interval) {
    if (!symbol) return;
    if (!_coinData[symbol]) _coinData[symbol] = { candles: [], ws: null, interval: _activeInterval, patterns: [] };
    _coinData[symbol].interval = interval;
    if (_chart) {
      try { _coinData[symbol].visibleRange = _chart.timeScale().getVisibleRange(); } catch (e) {}
    }
  },

  getCoinState: function (symbol) {
    return _coinData[symbol] || null;
  },

  restoreCoinState: function (symbol, interval) {
    var saved = _coinData[symbol];
    if (!saved) return;
    if (saved.interval === interval) {
      var cached = _allCoinPatterns[symbol] || [];
      renderPatterns(cached);
      var btn = document.querySelector('.analyze-btn');
      if (btn) {
        var label = btn.querySelector('.analyze-btn-label');
        if (label) label.textContent = cached.length > 0 ? 'CLEAR PATTERNS' : 'ANALYZE';
        btn.disabled = false;
        btn.classList.remove('analyzing');
      }
      var resultEl = document.querySelector('.result-text');
      if (resultEl) {
        resultEl.innerText = cached.length > 0 ? cached.length + ' pattern(s) loaded.' : 'Click to analyze chart for patterns.';
      }
    }
  },

  loadPatternsFromDB: function () { return Promise.resolve(); },
  analyzePatterns: function () { analyzePatterns(); },
};

/* ── Pattern analysis ────────────────────────────────────── */

function analyzePatterns() {
  var btn = document.querySelector('.analyze-btn');
  var resultEl = document.querySelector('.result-text');
  if (!btn || !resultEl) return;
  var label = btn.querySelector('.analyze-btn-label');
  if (label) label.textContent = 'LOADING...';
  btn.disabled = true;
  btn.classList.add('analyzing');
  resultEl.innerText = 'Loading existing patterns...';
  loadExistingPatterns(btn, resultEl);
}

function loadExistingPatterns(btn, resultEl) {
  var symbol = window.currentSymbol || 'BTCUSDT';
  var label = btn.querySelector('.analyze-btn-label');
  if (label) label.textContent = 'LOADING...';
  fetch('/api/patterns/' + encodeURIComponent(symbol) + '?interval=5m').then(function (resp) {
    if (!resp.ok) return [];
    return resp.json().then(function (data) { return data.patterns || []; });
  }).then(function (existing) {
    var msg = '5m timeframe. ';
    resultEl.innerText = existing.length ? msg + existing.length + ' existing pattern(s) loaded. Checking for new ones...' : msg + 'No existing patterns. Scanning...';
    return mlScan(symbol, btn, resultEl);
  }).catch(function (err) {
    resultEl.innerText = 'Analysis failed: ' + err.message;
    btn.disabled = false;
    btn.classList.remove('analyzing');
    if (label) label.textContent = 'ANALYZE';
  });
}

function mlScan(symbol, btn, resultEl) {
  var label = btn.querySelector('.analyze-btn-label');
  if (label) label.textContent = 'SCANNING...';
  var currentTf = window._currentInterval || '5m';
  var mlInterval = '5m';
  if (currentTf !== mlInterval) {
    resultEl.innerText = 'Note: ML analysis uses 5m data regardless of selected timeframe.';
  }
  var threshold = parseFloat(window._analysisThreshold || '0.60');
  fetch('/api/analyze/' + encodeURIComponent(symbol) + '?interval=' + mlInterval + '&confidence_threshold=' + threshold, { method: 'POST' })
    .then(function (resp) {
      return resp.text().then(function (text) {
        var data;
        try { data = text ? JSON.parse(text) : {}; }
        catch (e) { data = { detail: text || ('HTTP ' + resp.status) }; }
        if (!resp.ok) throw new Error(data.detail || ('Analysis failed (HTTP ' + resp.status + ')'));
        return data;
      });
    }).then(function (mlData) {

      var patterns = mlData.patterns || [];
      resultEl.innerText = patterns.length ? 'Found ' + patterns.length + ' pattern(s) on 5m.' : 'No patterns detected on 5m.';
      window.TFChart.renderPatterns(patterns);
      btn.disabled = false;
      btn.classList.remove('analyzing');
      if (label) label.textContent = patterns.length > 0 ? 'CLEAR PATTERNS' : 'ANALYZE';
    }).catch(function (err) {
      resultEl.innerText = 'Analysis failed: ' + err.message;
      btn.disabled = false;
      btn.classList.remove('analyzing');
      if (label) label.textContent = 'ANALYZE';
    });
}

document.addEventListener('DOMContentLoaded', createChart);
