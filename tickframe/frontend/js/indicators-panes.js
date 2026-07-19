/* ============================================================
   TFIndicatorPanes — native Lightweight Charts v5 pane manager.

   Instead of creating a separate chart per indicator (which produced
   independent grids, price axes, time axes and opaque backgrounds), this
   module allocates *panes* inside the single main chart. All panes share
   one grid, one time axis and one crosshair; the library draws a single
   thin separator line between them.
   ============================================================ */
var TFIndicatorPanes = (function () {
  // Map of logical paneId -> { paneIndex, series: [] }
  var panes = {};
  var mainChart = null;

  // Reserved pane indices:
  //   0 = main price pane (candles + overlays)
  //   1 = volume pane (created lazily by charts.js as '_volume')
  // Indicator panes are allocated at index >= 2.
  function init(chart) {
    mainChart = chart;
  }

  // Allocate the next free pane index. Lightweight Charts creates panes on
  // demand when a series requests a paneIndex that does not yet exist, so we
  // only need to hand out a monotonically-increasing index that is not in use.
  function nextPaneIndex() {
    var used = {};
    var ids = Object.keys(panes);
    for (var i = 0; i < ids.length; i++) {
      used[panes[ids[i]].paneIndex] = true;
    }
    // start at 2 so we never collide with price (0) or volume (1)
    var idx = 2;
    while (used[idx]) idx++;
    return idx;
  }

  // Return the pane record for a logical id, creating (reserving) one if
  // needed. The actual pane in the chart appears once a series is added to
  // the returned paneIndex.
  function getOrCreatePane(paneId) {
    if (panes[paneId]) return panes[paneId];
    var paneIndex = paneId === '_volume' ? 1 : nextPaneIndex();
    panes[paneId] = { paneIndex: paneIndex, series: [] };
    window._indicatorPanes = window._indicatorPanes || {};
    window._indicatorPanes[paneId] = panes[paneId];
    return panes[paneId];
  }

  // Backwards-compatible alias (older callers used createPane).
  function createPane(paneId) {
    return getOrCreatePane(paneId);
  }

  function registerSeries(paneId, series) {
    var p = panes[paneId];
    if (p && series) p.series.push(series);
  }

  function destroyPane(paneId) {
    if (paneId.charAt(0) === '_') return;
    var pane = panes[paneId];
    if (!pane) return;
    removePaneSeries(pane);
    // Remove the now-empty pane so remaining panes collapse upward and the
    // separators stay contiguous.
    try {
      if (mainChart && typeof mainChart.removePane === 'function') {
        mainChart.removePane(pane.paneIndex);
      }
    } catch (e) {}
    delete panes[paneId];
    if (window._indicatorPanes) delete window._indicatorPanes[paneId];
    reindexAfterRemoval(pane.paneIndex);
  }

  function removePaneSeries(pane) {
    if (!pane || !pane.series) return;
    for (var i = 0; i < pane.series.length; i++) {
      try {
        if (mainChart && typeof mainChart.removeSeries === 'function') {
          mainChart.removeSeries(pane.series[i]);
        }
      } catch (e) {}
    }
    pane.series = [];
  }

  // When a pane is removed the library shifts higher panes down by one, so we
  // decrement our stored indices to match.
  function reindexAfterRemoval(removedIndex) {
    var ids = Object.keys(panes);
    for (var i = 0; i < ids.length; i++) {
      var p = panes[ids[i]];
      if (p.paneIndex > removedIndex) p.paneIndex -= 1;
    }
  }

  function destroyAll() {
    var ids = Object.keys(panes);
    for (var i = 0; i < ids.length; i++) {
      if (ids[i].charAt(0) !== '_') destroyPane(ids[i]);
    }
  }

  // With a single chart the library handles resize/theme automatically; these
  // remain as no-ops so existing callers do not break.
  function resizeAll() {}
  function applyThemeToAll() {}

  return {
    init: init,
    createPane: createPane,
    getOrCreatePane: getOrCreatePane,
    registerSeries: registerSeries,
    destroyPane: destroyPane,
    destroyAll: destroyAll,
    resizeAll: resizeAll,
    applyThemeToAll: applyThemeToAll,
    panes: panes,
  };
})();

window.TFIndicatorPanes = TFIndicatorPanes;
