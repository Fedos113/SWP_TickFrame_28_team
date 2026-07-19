var TFIndicatorController = (function () {
  var getCurrentBarsFn = null;
  var DEFAULT_COLORS = ['#2962FF', '#FF6D00', '#7E57C2', '#26A69A', '#EF5350', '#FF9800', '#E91E63', '#9C27B0'];
  var patternMarkerColor = '#FF9800';

  function init(opts) {
    if (opts && opts.getCurrentBarsFn) getCurrentBarsFn = opts.getCurrentBarsFn;
  }

  function uid() {
    return 'ind_' + Date.now() + '_' + Math.random().toString(36).slice(2, 7);
  }

  function getBars() {
    if (typeof getCurrentBarsFn === 'function') return getCurrentBarsFn();
    return [];
  }

  function applyIndicator(indicatorId, inputs) {
    var def = TFIndicators.get(indicatorId);
    if (!def) { console.warn('Indicator not found:', indicatorId); return; }
    var applied = TFIndicatorState.getApplied();
    for (var i = 0; i < applied.length; i++) {
      if (applied[i].indicatorId === indicatorId) {
        console.log('Indicator already applied:', indicatorId);
        return;
      }
    }
    var bars = getBars();
    if (!bars || !bars.length) { console.warn('No candle data available'); return; }

    var mergedInputs = Object.assign({}, def.defaultInputs || {}, inputs || {});
    var result;
    try {
      result = def.calculate(bars, mergedInputs);
    } catch (e) {
      console.error('Indicator calculation error:', indicatorId, e);
      return;
    }
    if (!result || !result.plots) return;

    var meta = result.metadata || {};
    var entry = {
      uid: uid(),
      indicatorId: indicatorId,
      inputs: mergedInputs,
      title: meta.shortTitle || meta.shorttitle || meta.title || def.shortName || def.id,
      overlay: def.overlay,
      series: [],
      markerSeries: null,
    };

    if (def.group === 'candlestickPatterns') {
      renderCandlestickPatterns(entry, result);
    } else if (def.overlay) {
      renderOverlay(entry, result);
    } else {
      renderInPane(entry, result);
    }

    TFIndicatorState.addIndicator(entry);
    persist();
  }

  function cleanPlotData(data) {
    if (!data || !data.length) return data;
    return data.filter(function (d) {
      return d != null && d.time != null && d.value != null && isFinite(d.value);
    });
  }

  function renderOverlay(entry, result) {
    var plotKeys = Object.keys(result.plots);
    for (var i = 0; i < plotKeys.length; i++) {
      var raw = result.plots[plotKeys[i]];
      var data = cleanPlotData(raw);
      if (!data || !data.length) continue;
      var color = DEFAULT_COLORS[i % DEFAULT_COLORS.length];
      try {
        var lineSeries = window.chart.addSeries(LightweightCharts.LineSeries, {
          color: color,
          lineWidth: 1,
          lastValueVisible: true,
          priceLineVisible: false,
        });
        lineSeries.setData(data);
        entry.series.push(lineSeries);
      } catch (e) {
        console.warn('Failed to create overlay series', e);
      }
    }
  }

  function renderInPane(entry, result) {
    var colorIdx = 0;
    var paneId = entry.uid;

    // Reserve a native chart pane index for this indicator. The pane itself is
    // materialised by the library once we add the first series to it.
    var pane = TFIndicatorPanes.getOrCreatePane(paneId);
    if (!pane) return;
    entry.paneId = paneId;

    var plotKeys = Object.keys(result.plots);
    for (var i = 0; i < plotKeys.length; i++) {
      var raw = result.plots[plotKeys[i]];
      var data = cleanPlotData(raw);
      if (!data || !data.length) continue;
      var color = DEFAULT_COLORS[colorIdx % DEFAULT_COLORS.length];
      colorIdx++;
      try {
        // Third argument = paneIndex → series is placed in the shared chart's pane.
        var lineSeries = window.chart.addSeries(LightweightCharts.LineSeries, {
          color: color,
          lineWidth: 1,
          lastValueVisible: true,
          priceLineVisible: false,
          title: entry.title,
        }, pane.paneIndex);
        lineSeries.setData(data);
        entry.series.push(lineSeries);
        TFIndicatorPanes.registerSeries(paneId, lineSeries);
      } catch (e) {
        console.warn('Failed to create pane series', e);
      }
    }
  }


  function renderCandlestickPatterns(entry, result) {
    var plotData = result.plots && result.plots.plot0;
    if (!plotData || !plotData.length) return;
    var markers = plotData.map(function (p) {
      return {
        time: p.time,
        position: 'aboveBar',
        color: patternMarkerColor,
        shape: 'arrowDown',
        text: entry.title,
      };
    });
    if (window.candleSeries && typeof window.candleSeries.setMarkers === 'function') {
      window.candleSeries.setMarkers(markers);
      entry.markerSeries = markers;
    }
  }

  function removeIndicator(uidToRemove) {
    var entry = null;
    var applied = TFIndicatorState.getApplied();
    for (var i = 0; i < applied.length; i++) {
      if (applied[i].uid === uidToRemove) { entry = applied[i]; break; }
    }
    if (!entry) return;

    cleanupEntry(entry);
    TFIndicatorState.removeIndicator(uidToRemove);
    persist();
  }

  function cleanupEntry(entry) {
    if (entry.series) {
      for (var i = 0; i < entry.series.length; i++) {
        try {
          if (window.chart && typeof window.chart.removeSeries === 'function') {
            window.chart.removeSeries(entry.series[i]);
          }
        } catch (e) {}
      }
    }
    if (entry.paneId) {
      TFIndicatorPanes.destroyPane(entry.paneId);
    }
    if (entry.markerSeries && window.candleSeries && typeof window.candleSeries.setMarkers === 'function') {
      window.candleSeries.setMarkers([]);
    }
  }

  function recomputeAll() {
    var bars = getBars();
    if (!bars || !bars.length) return;
    var applied = TFIndicatorState.getApplied();
    for (var i = 0; i < applied.length; i++) {
      var entry = applied[i];
      var def = TFIndicators.get(entry.indicatorId);
      if (!def) continue;
      try {
        var result = def.calculate(bars, entry.inputs);
        if (!result || !result.plots) continue;
        if (def.group === 'candlestickPatterns') {
          var plotData = result.plots.plot0;
          if (plotData && plotData.length) {
            var markers = plotData.map(function (p) {
              return { time: p.time, position: 'aboveBar', color: patternMarkerColor, shape: 'arrowDown', text: entry.title };
            });
            if (window.candleSeries && typeof window.candleSeries.setMarkers === 'function') {
              window.candleSeries.setMarkers(markers);
            }
          }
        } else {
          var plotKeys = Object.keys(result.plots);
          var branch = def.overlay ? 'overlay' : 'pane';
          for (var j = 0; j < plotKeys.length && j < entry.series.length; j++) {
            var raw = result.plots[plotKeys[j]];
            var data = cleanPlotData(raw);
            if (data && data.length) entry.series[j].setData(data);
          }
        }
      } catch (e) {
        console.warn('Recompute error', entry.indicatorId, e);
      }
    }
  }

  async function persist() {
    var symbol = window.currentSymbol || 'BTCUSDT';
    var payload = [];
    var applied = TFIndicatorState.getApplied();
    for (var i = 0; i < applied.length; i++) {
      var a = applied[i];
      payload.push({ uid: a.uid, indicatorId: a.indicatorId, inputs: a.inputs, overlay: a.overlay });
    }
    try {
      await fetch('/api/indicators', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol: symbol, indicators: payload }),
      });
    } catch (e) {
      console.warn('Failed to persist indicators', e);
    }
  }

  async function loadForSymbol(symbol) {
    destroyAll();
    try {
      var resp = await fetch('/api/indicators?symbol=' + encodeURIComponent(symbol));
      if (!resp.ok) return;
      var data = await resp.json();
      var indicators = data.indicators || [];
      for (var i = 0; i < indicators.length; i++) {
        applyIndicator(indicators[i].indicatorId, indicators[i].inputs);
      }
    } catch (e) {
      console.warn('Failed to load indicators for', symbol, e);
    }
  }

  function destroyAll() {
    var applied = TFIndicatorState.getApplied().slice();
    for (var i = 0; i < applied.length; i++) {
      cleanupEntry(applied[i]);
    }
    TFIndicatorPanes.destroyAll();
    TFIndicatorState.setApplied([]);
  }

  return {
    init: init,
    applyIndicator: applyIndicator,
    removeIndicator: removeIndicator,
    recomputeAll: recomputeAll,
    persist: persist,
    loadForSymbol: loadForSymbol,
    destroyAll: destroyAll,
  };
})();

window.TFIndicatorController = TFIndicatorController;