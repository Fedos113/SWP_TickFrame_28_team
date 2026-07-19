/* ============================================================
   TickFrame — Topbar market header
   Populates coin identity (icon, ticker, name), live price,
   24h change, multi-timeframe change (5m / 1h / 4h / 24h)
   computed from chart bars, and market cap / circulating
   supply / 24h volume from CoinGecko's public markets API.
   ============================================================ */
(function () {
  // Map Bybit-style pairs to CoinGecko ids for the markets lookup.
  var CG_IDS = {
    BTCUSDT: 'bitcoin',
    ETHUSDT: 'ethereum',
    SOLUSDT: 'solana',
    XRPUSDT: 'ripple',
    DOGEUSDT: 'dogecoin',
    ADAUSDT: 'cardano',
    AVAXUSDT: 'avalanche-2',
    DOTUSDT: 'polkadot',
    LINKUSDT: 'chainlink',
    BNBUSDT: 'binancecoin',
  };

  var _marketsCache = null;
  var _marketsCacheAt = 0;
  var _currentSymbol = 'BTCUSDT';

  function coinName(symbol) {
    var list = window._coinList || [];
    for (var i = 0; i < list.length; i++) {
      if (list[i].symbol === symbol) return list[i].name;
    }
    return symbol.replace('USDT', '');
  }

  function fmtCompact(n) {
    if (n == null || isNaN(n)) return '--';
    var abs = Math.abs(n);
    if (abs >= 1e12) return '$' + (n / 1e12).toFixed(2) + 'T';
    if (abs >= 1e9) return '$' + (n / 1e9).toFixed(2) + 'B';
    if (abs >= 1e6) return '$' + (n / 1e6).toFixed(2) + 'M';
    if (abs >= 1e3) return '$' + (n / 1e3).toFixed(2) + 'K';
    return '$' + n.toFixed(2);
  }

  function fmtSupply(n, ticker) {
    if (n == null || isNaN(n)) return '--';
    var abs = Math.abs(n);
    var s;
    if (abs >= 1e9) s = (n / 1e9).toFixed(2) + 'B';
    else if (abs >= 1e6) s = (n / 1e6).toFixed(2) + 'M';
    else if (abs >= 1e3) s = (n / 1e3).toFixed(2) + 'K';
    else s = n.toFixed(0);
    return s + ' ' + ticker;
  }

  function fmtPrice(p) {
    if (p == null || isNaN(p)) return '--';
    var abs = Math.abs(p);
    var dec;
    if (abs >= 1000) dec = 2;
    else if (abs >= 1) dec = 4;
    else if (abs >= 0.01) dec = 6;
    else dec = 8;
    return '$' + p.toFixed(dec).replace(/(\.\d*?)0+$/, '$1').replace(/\.$/, '');
  }

  function setChangeCell(el, pct) {
    if (!el) return;
    if (pct == null || isNaN(pct)) {
      el.textContent = '--';
      el.classList.remove('tf-up', 'tf-down');
      return;
    }
    var sign = pct >= 0 ? '+' : '';
    el.textContent = sign + pct.toFixed(2) + '%';
    el.classList.toggle('tf-up', pct >= 0);
    el.classList.toggle('tf-down', pct < 0);
  }

  // Update the coin icon / ticker / name block.
  function refreshIdentity() {
    var symbol = window.currentSymbol || _currentSymbol;
    _currentSymbol = symbol;
    var ticker = symbol.replace('USDT', '');
    var iconEl = document.getElementById('marketIcon');
    var tickerEl = document.getElementById('marketTicker');
    var nameEl = document.getElementById('marketTitle');

    if (tickerEl) tickerEl.innerHTML = ticker + '<span class="market-quote">USDT</span>';
    if (nameEl) nameEl.textContent = coinName(symbol);
    if (iconEl) {
      var url = (window._coinIcons || {})[symbol];
      iconEl.innerHTML = url ? '<img src="' + url + '" alt="' + ticker + '" />' : ticker;
    }
  }

  // Compute % change over a number of seconds from the loaded chart bars.
  function changeOverSeconds(bars, seconds) {
    if (!bars || bars.length < 2) return null;
    var last = bars[bars.length - 1];
    var target = last.time - seconds;
    var ref = null;
    for (var i = bars.length - 1; i >= 0; i--) {
      if (bars[i].time <= target) { ref = bars[i]; break; }
    }
    if (!ref) ref = bars[0];
    if (!ref || !ref.close) return null;
    return ((last.close - ref.close) / ref.close) * 100;
  }

  function refreshChanges() {
    var bars = window.TFChart ? window.TFChart.getCurrentBars() : [];
    setChangeCell(document.getElementById('mc5m'), changeOverSeconds(bars, 5 * 60));
    setChangeCell(document.getElementById('mc1h'), changeOverSeconds(bars, 60 * 60));
    setChangeCell(document.getElementById('mc4h'), changeOverSeconds(bars, 4 * 60 * 60));
    setChangeCell(document.getElementById('mc24h'), changeOverSeconds(bars, 24 * 60 * 60));
  }

  // Live price + 24h change + 24h volume from the backend /api/coins feed.
  // Used only for initial REST load; real-time updates come via WebSocket.
  async function refreshLivePrice() {
    try {
      var res = await fetch('/api/coins');
      if (!res.ok) return;
      var list = await res.json();
      var info = null;
      for (var i = 0; i < list.length; i++) {
        if (list[i].pair === (window.currentSymbol || _currentSymbol)) { info = list[i]; break; }
      }
      if (!info) return;
      updateFromSnapshot(info.price, info.change_24h, info.volume_24h);
    } catch (e) { /* network hiccup — keep last values */ }
  }

  // Called directly from WebSocket market_snapshot (no REST fetch).
  function updateFromSnapshot(price, change24h, volume24h) {
    var priceEl = document.getElementById('marketPrice');
    var chEl = document.getElementById('marketPriceChange');
    var volEl = document.getElementById('mmVolume');
    if (priceEl && price != null) priceEl.textContent = fmtPrice(price);
    if (chEl && change24h != null) {
      var sign = change24h >= 0 ? '+' : '';
      chEl.textContent = sign + change24h.toFixed(2) + '% 24h';
      chEl.classList.toggle('tf-up', change24h >= 0);
      chEl.classList.toggle('tf-down', change24h < 0);
    }
    if (volEl && volume24h != null && price != null) {
      volEl.textContent = fmtCompact(volume24h * price);
    }
  }

  // Market cap + circulating supply from CoinGecko (cached ~5 min).
  async function refreshMarketMetrics() {
    var symbol = window.currentSymbol || _currentSymbol;
    var ticker = symbol.replace('USDT', '');
    var mcEl = document.getElementById('mmMarketCap');
    var supEl = document.getElementById('mmSupply');
    try {
      var now = Date.now();
      if (!_marketsCache || now - _marketsCacheAt > 300000) {
        var ids = Object.values(CG_IDS).join(',');
        var url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=' + ids;
        var res = await fetch(url);
        if (!res.ok) return;
        var arr = await res.json();
        _marketsCache = {};
        arr.forEach(function (m) { _marketsCache[m.id] = m; });
        _marketsCacheAt = now;
      }
      var m = _marketsCache[CG_IDS[symbol]];
      if (!m) return;
      if (mcEl) mcEl.textContent = fmtCompact(m.market_cap);
      if (supEl) supEl.textContent = fmtSupply(m.circulating_supply, ticker);
    } catch (e) { /* CoinGecko rate-limit / offline — leave as-is */ }
  }

  function refreshAll() {
    refreshIdentity();
    refreshChanges();
    refreshLivePrice();
    refreshMarketMetrics();
  }

  window.TFTopbar = {
    refreshIdentity: refreshIdentity,
    refreshChanges: refreshChanges,
    refreshLivePrice: refreshLivePrice,
    refreshMarketMetrics: refreshMarketMetrics,
    refreshAll: refreshAll,
    updateFromSnapshot: updateFromSnapshot,
    onSymbolChange: function (symbol) {
      _currentSymbol = symbol;
      refreshIdentity();
      refreshChanges();
      refreshLivePrice();
      refreshMarketMetrics();
    },
  };

  document.addEventListener('DOMContentLoaded', function () {
    refreshAll();
    // Changes read from chart bars (cheap, no REST). Market WS pushes price/change.
    setInterval(refreshChanges, 1000);
    // Market cap / supply change slowly; poll less often.
    setInterval(refreshMarketMetrics, 300000);
  });
})();
