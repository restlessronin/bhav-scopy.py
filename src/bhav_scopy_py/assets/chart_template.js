function render({ model, el }) {
  console.log("Render function called");
  const container = document.createElement("div");
  container.style.width = "100%";
  container.style.height = "100%";
  el.appendChild(container);

  console.log("Creating chart with config:", model.get("_config"));
  const chart = LightweightCharts.createChart(container, model.get("_config"));

  const seriesMap = new Map();

  function updateOrCreateSeries(seriesConfig) {
    let series = seriesMap.get(seriesConfig.id);

    if (!series) {
      switch (seriesConfig.type) {
        case 'candlestick':
          series = chart.addCandlestickSeries(seriesConfig.style);
          break;
        case 'line':
          series = chart.addLineSeries(seriesConfig.style);
          break;
        case 'histogram':
          series = chart.addHistogramSeries(seriesConfig.style);
          break;
        default:
          console.error('Unknown series type:', seriesConfig.type);
          return;
      }
      seriesMap.set(seriesConfig.id, series);
    }
    series.setData(seriesConfig.data);
  }

  const seriesConfigs = model.get("_series_configs");
  console.log("Initial series configs:", seriesConfigs);
  seriesConfigs.forEach(updateOrCreateSeries);

  model.on("change:_series_configs", () => {
    const configs = model.get("_series_configs");
    console.log("Series configs updated:", configs);
    configs.forEach(updateOrCreateSeries);
  });

  const resizeObserver = new ResizeObserver((entries) => {
    const { width, height } = entries[0].contentRect;
    chart.applyOptions({
      width,
      height,
    });
  });
  resizeObserver.observe(container);

  return () => {
    resizeObserver.disconnect();
    chart.remove();
  };
}

export default { render };