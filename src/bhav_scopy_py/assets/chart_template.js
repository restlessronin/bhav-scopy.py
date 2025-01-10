if (typeof LightweightCharts === "undefined") {
  throw new Error("LightweightCharts library not loaded");
}

function render({ model, el }) {
  const container = document.createElement("div");
  container.style.width = "100%";
  container.style.height = "100%";
  el.appendChild(container);
  const chart = LightweightCharts.createChart(container, model.get("_config"));
  const candlestickSeries = chart.addCandlestickSeries({
    upColor: "#26a69a",
    downColor: "#ef5350",
    borderVisible: false,
    wickUpColor: "#26a69a",
    wickDownColor: "#ef5350",
  });
  model.on("change:_chart_data", () => {
    const data = model.get("_chart_data");
    candlestickSeries.setData(data);
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
