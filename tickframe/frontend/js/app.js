function saveSetting(key, value) {
  fetch('/api/settings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ settings: { [key]: value } }),
  }).catch(function () {});
}

async function loadSettings() {
  try {
    var r = await fetch('/api/settings');
    var data = await r.json();
    var s = data.settings || {};
    if (s.theme === 'light') {
      document.body.classList.add('light');
      if (window.TFChart && window.TFChart.applyChartTheme) {
        window.TFChart.applyChartTheme(false);
      }
    }
  } catch (e) {}
}

var _initialLoadDone = false;
var _rsiAppliedForSymbol = '';

function initIndicatorSubsystem() {
  if (window.TFIndicatorController && window.TFIndicatorState && window.TFIndicatorPanel && window.TFIndicatorChips && window.TFIndicatorPanes) {
    TFIndicatorController.init({
      getCurrentBarsFn: function () { return window.TFChart ? window.TFChart.getCurrentBars() : []; },
    });
    var mainChart = window.TFChart ? window.TFChart.mainChart() : null;
    if (mainChart) {
      TFIndicatorPanes.init(mainChart);
    }
    TFIndicatorPanel.init();
    TFIndicatorChips.init();
  }

  window._onCandlesUpdated = function (symbol) {
    if (window.TFTopbar && typeof window.TFTopbar.refreshChanges === 'function') {
      window.TFTopbar.refreshChanges();
    }
    // Lazy-init indicator panes with the active chart (created on first coin switch)
    if (window.TFIndicatorPanes && !window.TFIndicatorPanes.mainChart) {
      var chart = window.TFChart ? window.TFChart.mainChart() : null;
      if (chart) TFIndicatorPanes.init(chart);
    }
    if (!window.TFIndicatorController) return;
    var saved = TFIndicatorState.getApplied().slice();
    TFIndicatorController.destroyAll();
    for (var i = 0; i < saved.length; i++) {
      TFIndicatorController.applyIndicator(saved[i].indicatorId, saved[i].inputs);
    }
    if (_rsiAppliedForSymbol !== symbol) {
      _rsiAppliedForSymbol = symbol;
      var hasRsi = false;
      for (var j = 0; j < saved.length; j++) {
        if (saved[j].indicatorId === 'rsi') { hasRsi = true; break; }
      }
      if (!hasRsi) {
        TFIndicatorController.applyIndicator('rsi');
      }
    }
  };
}

document.addEventListener('DOMContentLoaded', function () {
  loadSettings();
  initIndicatorSubsystem();
  const defaultSymbol = 'BTCUSDT';
  const symbolNames = {
    BTCUSDT: 'Bitcoin', ETHUSDT: 'Ethereum', SOLUSDT: 'Solana',
    XRPUSDT: 'Ripple', DOGEUSDT: 'Dogecoin', ADAUSDT: 'Cardano',
    AVAXUSDT: 'Avalanche', DOTUSDT: 'Polkadot', LINKUSDT: 'Chainlink', BNBUSDT: 'BNB',
  };

  const updateTitle = function (symbol) {
    document.title = (symbolNames[symbol] || symbol) + ' \u00B7 TickFrame';
    if (window.TFTopbar && typeof window.TFTopbar.onSymbolChange === 'function') {
      window.TFTopbar.onSymbolChange(symbol);
    }
  };

  var origSetActive = window.TFChart?.setActiveSymbol;
  if (window.TFChart) {
    window.TFChart.setActiveSymbol = function (symbol) {
      window.currentSymbol = symbol;
      updateTitle(symbol);
      _initialLoadDone = true;
      if (typeof origSetActive === 'function') origSetActive(symbol);
      if (window.TFIndicatorController && typeof TFIndicatorController.loadForSymbol === 'function') {
        TFIndicatorController.loadForSymbol(symbol);
      }
    };
  }

  // timeframe buttons — use the manager's switchInterval
  document.querySelectorAll('.timeframes button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.timeframes button').forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      var tf = btn.dataset.tf;
      if (window.TFChart) {
        if (window.currentSymbol && window.TFChart.saveCoinState) {
          window.TFChart.saveCoinState(window.currentSymbol, tf);
        }
        window.TFChart.switchInterval(tf);
      }
    });
  });

  // theme toggle
  var themeBtn = document.getElementById('themeBtn');
  themeBtn?.addEventListener('click', function () {
    var body = document.body;
    body.classList.toggle('light');
    var dark = !body.classList.contains('light');
    window.TFChart?.applyChartTheme?.(dark);
    saveSetting('theme', dark ? 'dark' : 'light');
    if (typeof startFearAndGreedPolling === 'function') startFearAndGreedPolling();
    if (window.TFDraw && window.TFDraw.redraw) {
      window.TFDraw.redraw();
    }
    if (window.TFIndicatorPanes && typeof TFIndicatorPanes.applyThemeToAll === 'function') {
      TFIndicatorPanes.applyThemeToAll(dark);
    }
  });

  // analyze / clear patterns button
  var analyzeBtn = document.querySelector('.analyze-btn');
  analyzeBtn?.addEventListener('click', function () {
    var label = analyzeBtn.querySelector('.analyze-btn-label');
    if (label && label.textContent === 'CLEAR PATTERNS') {
      window.TFChart?.clearPatternsFrontend?.();
    } else {
      window.TFChart?.analyzePatterns?.();
    }
  });

  // pattern filter button
  var filterBtn = document.querySelector('.filter-patterns-btn');
  filterBtn?.addEventListener('click', function () {
    window.TFChart?.togglePatternFilter?.();
  });

  function updateFilterBadge() {
    var badge = document.getElementById('filterCountBadge');
    if (!badge) return;
    var checked = document.querySelectorAll('.pattern-filter-cb:checked').length;
    var total = document.querySelectorAll('.pattern-filter-cb').length;
    badge.textContent = checked;
    if (filterBtn) filterBtn.classList.toggle('filtered', checked < total);
  }

  document.querySelectorAll('.pattern-filter-cb').forEach(function (cb) {
    cb.addEventListener('change', function () {
      var pattern = this.dataset.pattern;
      if (window._patternFilter) {
        window._patternFilter[pattern] = this.checked;
      }
      updateFilterBadge();
      window.TFChart?.onPatternFilterChange?.();
    });
  });

  function setAllPatterns(state) {
    document.querySelectorAll('.pattern-filter-cb').forEach(function (cb) {
      cb.checked = state;
      if (window._patternFilter) {
        window._patternFilter[cb.dataset.pattern] = state;
      }
    });
    updateFilterBadge();
    window.TFChart?.onPatternFilterChange?.();
  }
  document.getElementById('patternFilterSelectAll')?.addEventListener('click', function () { setAllPatterns(true); });
  document.getElementById('patternFilterClearAll')?.addEventListener('click', function () { setAllPatterns(false); });

  var filterClose = document.getElementById('patternFilterClose');
  if (filterClose) {
    filterClose.addEventListener('click', function () {
      window.TFChart?.togglePatternFilter?.();
    });
  }

  updateFilterBadge();
  updateTitle(defaultSymbol);

  // Auto-select first coin when chart is ready
  setTimeout(function () {
    if (_initialLoadDone) return;
    var first = document.querySelector('.watchlist .coin');
    if (first) first.click();
  }, 300);
});
