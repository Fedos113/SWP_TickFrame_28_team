var TFIndicatorPanel = (function () {
  var panelEl = null;
  var searchEl = null;
  var listEl = null;
  var unsub = null;

  function init() {
    panelEl = document.getElementById('indicatorsPanel');
    if (!panelEl) return;
    searchEl = document.getElementById('indicatorsSearch');
    listEl = document.getElementById('indicatorsList');

    if (searchEl) {
      searchEl.addEventListener('input', function (e) {
        TFIndicatorState.setSearchQuery(e.target.value);
      });
    }

    unsub = TFIndicatorState.subscribe(render);
    render();
  }

  function pinnedRSIRow() {
    var st = TFIndicatorState.getState();
    var rsiApplied = false;
    for (var i = 0; i < st.applied.length; i++) {
      if (st.applied[i].indicatorId === 'rsi') { rsiApplied = true; break; }
    }
    var row = document.createElement('div');
    row.className = 'indicator-row indicator-row-pinned' + (rsiApplied ? ' indicator-applied' : '');
    row.innerHTML = '<span class="indicator-pin-icon">&#9733;</span> RSI (14)' + (rsiApplied ? ' \u2713' : '');
    row.onclick = function () {
      TFIndicatorController.applyIndicator('rsi');
    };
    return row;
  }

  function volumeToggleRow() {
    var st = TFIndicatorState.getState();
    var row = document.createElement('div');
    row.className = 'indicator-row indicator-row-toggle';
    row.innerHTML =
      '<span class="indicator-toggle-icon">' +
      '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>' +
      '</span> Volume + SMA' +
      '<span class="indicator-toggle-check' + (st.volumeEnabled ? ' checked' : '') + '">' +
      '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>' +
      '</span>';
    row.onclick = function () {
      TFIndicatorState.toggleVolume();
    };
    return row;
  }

  function applyVolumeVisibility(visible) {
    var active = window.TFChart && typeof window.TFChart.mainChart === 'function' ? window.TFChart.mainChart() : null;
    var targetSeries = null;
    if (active && active._tickframeVolumeSeries) {
      targetSeries = active._tickframeVolumeSeries;
    } else if (window._volumeSeries) {
      targetSeries = window._volumeSeries;
    }
    if (targetSeries && typeof targetSeries.applyOptions === 'function') {
      targetSeries.applyOptions({ visible: visible });
    }
    if (active && active._tickframeVolumeSmaSeries) {
      active._tickframeVolumeSmaSeries.applyOptions({ visible: visible });
    } else if (window._volumeSmaSeries && typeof window._volumeSmaSeries.applyOptions === 'function') {
      window._volumeSmaSeries.applyOptions({ visible: visible });
    }

    // Hiding the histogram series alone leaves the volume pane (and its empty
    // price axis / gutter) visible. Collapse the volume pane's stretch factor to
    // 0 when hidden so the whole indicator bar disappears, and restore it when
    // shown. This relies on the volume pane being pane index 1.
    if (active && typeof active.panes === 'function') {
      try {
        var panes = active.panes();
        var pricePane = panes[0];
        var volPane = panes[1];
        if (volPane && typeof volPane.setStretchFactor === 'function') {
          volPane.setStretchFactor(visible ? 1 : 0.0001);
        }
        if (pricePane && typeof pricePane.setStretchFactor === 'function') {
          pricePane.setStretchFactor(visible ? 4 : 1);
        }
      } catch (e) { /* older lib versions may not support panes() */ }
    }
  }


  function render() {
    if (!listEl) return;
    var st = TFIndicatorState.getState();

    var grouped = st.searchQuery
      ? flattenSearch(st.searchQuery)
      : TFIndicators.byGroup();

    listEl.innerHTML = '';

    if (st.searchQuery) {
      grouped.forEach(function (ind) {
        listEl.appendChild(indicatorRow(ind));
      });
      return;
    }

    // pinned top-level entries
    listEl.appendChild(pinnedRSIRow());
    listEl.appendChild(volumeToggleRow());

    // separator
    var sep = document.createElement('div');
    sep.className = 'indicator-pinned-separator';
    listEl.appendChild(sep);

    // extract RSI from standard group so it doesn't appear twice
    var standardItems = [];
    for (var i = 0; i < (grouped.standard || []).length; i++) {
      if (grouped.standard[i].id !== 'rsi') {
        standardItems.push(grouped.standard[i]);
      }
    }

    var groups = [
      { key: 'standard', label: 'Standard', items: standardItems },
      { key: 'candlestickPatterns', label: 'Candlestick Patterns', items: grouped.candlestickPatterns },
      { key: 'community', label: 'Community', items: grouped.community },
    ];

    for (var g = 0; g < groups.length; g++) {
      var group = groups[g];
      if (!group.items || !group.items.length) continue;
      var section = document.createElement('div');
      section.className = 'indicator-group';

      var header = document.createElement('button');
      header.className = 'indicator-group-header';
      var expanded = st.expandedGroups[group.key];
      header.innerHTML =
        '<span class="indicator-chevron' + (expanded ? ' expanded' : '') + '">' +
        '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>' +
        '</span>' +
        '<span class="indicator-group-label">' + group.label + '</span>' +
        '<span class="indicator-group-count">' + group.items.length + '</span>';
      header.onclick = function (key) { return function () { TFIndicatorState.toggleGroup(key); }; }(group.key);
      section.appendChild(header);

      if (expanded) {
        var body = document.createElement('div');
        body.className = 'indicator-group-body';
        for (var j = 0; j < group.items.length; j++) {
          body.appendChild(indicatorRow(group.items[j]));
        }
        section.appendChild(body);
      }

      listEl.appendChild(section);
    }

    // sync volume pane visibility
    applyVolumeVisibility(st.volumeEnabled);
  }

  function flattenSearch(query) {
    return TFIndicators.search(query);
  }

  function indicatorRow(ind) {
    var row = document.createElement('div');
    var applied = TFIndicatorState.getApplied();
    var isApplied = false;
    for (var i = 0; i < applied.length; i++) {
      if (applied[i].indicatorId === ind.id) { isApplied = true; break; }
    }
    row.className = 'indicator-row' + (isApplied ? ' indicator-applied' : '');
    row.textContent = ind.name + (isApplied ? ' \u2713' : '');
    row.onclick = function () {
      TFIndicatorController.applyIndicator(ind.id);
    };
    return row;
  }

  function destroy() {
    if (unsub) { unsub(); unsub = null; }
  }

  return { init: init, destroy: destroy };
})();

window.TFIndicatorPanel = TFIndicatorPanel;