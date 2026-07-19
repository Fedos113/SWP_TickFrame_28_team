import { beforeEach, afterEach, describe, expect, it, vi } from 'vitest';

function createDomStub() {
  const elements = {};

  const classList = {
    values: new Set(),
    add(...names) { names.forEach((name) => this.values.add(name)); },
    remove(...names) { names.forEach((name) => this.values.delete(name)); },
    toggle(name, force) {
      if (force === undefined) {
        if (this.values.has(name)) this.values.delete(name); else this.values.add(name);
        return this.values.has(name);
      }
      if (force) this.values.add(name); else this.values.delete(name);
      return force;
    },
    contains(name) { return this.values.has(name); },
  };

  const chartLoading = { classList };
  elements.chartLoading = chartLoading;

  return {
    elements,
    documentStub: {
      addEventListener: vi.fn(),
      getElementById(id) { return elements[id] || null; },
      querySelector() { return null; },
      querySelectorAll() { return []; },
    },
    chartLoading,
  };
}

describe('chart UI helpers', () => {
  let originalWindow;
  let originalDocument;
  let originalTradingView;

  beforeEach(() => {
    originalWindow = globalThis.window;
    originalDocument = globalThis.document;
    originalTradingView = globalThis.TradingView;
    vi.resetModules();
  });

  afterEach(() => {
    globalThis.window = originalWindow;
    globalThis.document = originalDocument;
    globalThis.TradingView = originalTradingView;
  });

  it('toggles the loading overlay through TFChart state helpers', async () => {
    const { documentStub, chartLoading } = createDomStub();
    globalThis.window = { document: documentStub, currentSymbol: 'BTCUSDT', _coinList: [] };
    globalThis.document = documentStub;
    globalThis.TradingView = undefined;

    await import('../charts.js');

    window.TFChart.setLoadingState(true);
    expect(chartLoading.classList.contains('visible')).toBe(true);

    window.TFChart.setLoadingState(false);
    expect(chartLoading.classList.contains('visible')).toBe(false);
  });
});
