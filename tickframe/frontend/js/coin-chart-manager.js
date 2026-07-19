/* global CoinChartInstance */

function CoinChartManager() {
  this._instances = {};
  this._activeSymbol = null;
  this._activeInterval = '5m';
  this._stackContainer = null;
  this._coinState = {};
  this._isDarkTheme = true;
  this._initialized = false;
}

/* ── Initialisation ──────────────────────────────────────── */

CoinChartManager.prototype.init = function (containerId, symbols, interval) {
  this._stackContainer = document.getElementById(containerId);
  if (!this._stackContainer) return;
  this._activeInterval = interval || '5m';

  for (var i = 0; i < symbols.length; i++) {
    var symbol = symbols[i];
    var div = document.createElement('div');
    div.id = 'cl-' + symbol;
    div.className = 'chart-layer';
    this._stackContainer.appendChild(div);
    this._instances[symbol] = new CoinChartInstance(symbol, div);
  }

  this._initialized = true;
};

CoinChartManager.prototype.getSymbols = function () {
  var keys = [];
  for (var k in this._instances) {
    if (this._instances.hasOwnProperty(k)) keys.push(k);
  }
  return keys;
};

/* ── Background preload ──────────────────────────────────── */

CoinChartManager.prototype.preloadDefault = function () {
  var self = this;
  var symbols = this.getSymbols();
  if (!symbols.length) return null;
  var defaultSymbol = symbols[0];
  this.switchCoin(defaultSymbol, this._activeInterval);
  var instance = this._instances[defaultSymbol];
  if (!instance) return null;
  return instance.loadCandles(10000).then(function () {
    if (instance.lastCandles && instance.lastCandles.length > 0) {
      instance.connectWs(self._activeInterval);
    }
  }).catch(function () {});
};

/* ── Coin switching ──────────────────────────────────────── */

CoinChartManager.prototype.switchCoin = function (symbol, interval) {
  var self = this;
  var current = this._activeSymbol ? this._instances[this._activeSymbol] : null;
  if (current) {
    var range = null;
    try {
      if (current.chart) {
        range = current.chart.timeScale().getVisibleRange();
      }
    } catch (e) {}
    if (range) {
      this._saveState(this._activeSymbol, { visibleRange: range });
    }
    current.makeInactive();
  }

  this._activeSymbol = symbol;
  this._activeInterval = interval || this._activeInterval || '5m';

  var next = this._instances[symbol];
  if (!next) return;

  var needsLoad = false;
  if (!next.chart) {
    next.createChart(this._activeInterval);
    if (next.lastCandles.length) {
      next.setData(next.lastCandles);
    } else {
      needsLoad = true;
    }
  } else {
    next._interval = this._activeInterval;
  }

  next.makeActive();

  if (needsLoad) {
    typeof showLoading === 'function' && showLoading(true);
    var sym = symbol;
    next.loadCandles(10000).then(function () {
      var inst = self._instances[sym];
      if (inst && inst.lastCandles && inst.lastCandles.length > 0) {
        inst.resetChartScale();
        inst.connectWs(self._activeInterval);
      }
      typeof showLoading === 'function' && showLoading(false);
    }).catch(function () {
      typeof showLoading === 'function' && showLoading(false);
    });
  }

  var t = document.body.classList.contains('light') ? false : true;
  next.applyTheme(t);

  var saved = this._getState(symbol);
  if (saved && saved.visibleRange && next.chart) {
    try {
      next._isSettingRange = true;
      next.chart.timeScale().setVisibleRange(saved.visibleRange);
      next._isSettingRange = false;
    } catch (e) {
      next.resetChartScale();
    }
  } else {
    next.resetChartScale();
  }

  if (window.TFDraw) {
    try {
      window.TFDraw.init(next.chart, next.candleSeries, next.container);
      window.TFDraw.setSymbol(symbol);
    } catch (e) {}
  }
};

CoinChartManager.prototype.switchInterval = function (interval) {
  if (!this._activeSymbol) return;
  this._activeInterval = interval;
  var instance = this._instances[this._activeSymbol];
  if (!instance) return;
  instance.disconnectWs();
  typeof showLoading === 'function' && showLoading(true);
  instance.loadCandles(10000, null, interval).then(function () {
    instance.resetChartScale();
    instance.connectWs(interval);
    typeof showLoading === 'function' && showLoading(false);
  });
  this._saveState(this._activeSymbol, { interval: interval });
};

/* ── Theme ───────────────────────────────────────────────── */

CoinChartManager.prototype.applyTheme = function (dark) {
  this._isDarkTheme = dark;
  for (var k in this._instances) {
    if (this._instances.hasOwnProperty(k)) {
      this._instances[k].applyTheme(dark);
    }
  }
};

/* ── Per-coin state persistence ──────────────────────────── */

CoinChartManager.prototype._saveState = function (symbol, patch) {
  if (!this._coinState[symbol]) this._coinState[symbol] = {};
  for (var k in patch) {
    if (patch.hasOwnProperty(k)) {
      this._coinState[symbol][k] = patch[k];
    }
  }
};

CoinChartManager.prototype._getState = function (symbol) {
  return this._coinState[symbol] || null;
};

CoinChartManager.prototype.saveCoinState = function (symbol, interval) {
  var instance = this._instances[symbol];
  var range = null;
  if (instance && instance.chart) {
    try { range = instance.chart.timeScale().getVisibleRange(); } catch (e) {}
  }
  this._saveState(symbol, {
    interval: interval,
    visibleRange: range ? { from: range.from, to: range.to } : null,
  });
};

CoinChartManager.prototype.getCoinState = function (symbol) {
  return this._getState(symbol);
};

CoinChartManager.prototype.restoreCoinState = function (symbol, interval) {
  var state = this._getState(symbol);
  if (!state) return;
  if (state.interval === interval) {
    var instance = this._instances[symbol];
    if (instance) {
      instance.renderPatterns(instance.patterns);
    }
  }
};

/* ── Active instance accessors ───────────────────────────── */

CoinChartManager.prototype.getActiveInstance = function () {
  return this._activeSymbol ? (this._instances[this._activeSymbol] || null) : null;
};

CoinChartManager.prototype.getInstance = function (symbol) {
  return this._instances[symbol] || null;
};

CoinChartManager.prototype.getActiveSymbol = function () {
  return this._activeSymbol;
};

CoinChartManager.prototype.getActiveInterval = function () {
  return this._activeInterval;
};
