function render({ model, el }) {
  console.log("Render function called");
  const container = document.createElement('div');
  container.style.width = '100%';
  container.style.height = '100%';
  el.appendChild(container);

  const chart = LightweightCharts.createChart(container, model.get('_config'));
  const series = new Map();
  let processedCallCount = 0;
  function executeCall(call) {
    try {
      console.log("Executing:", call);
      (new Function('chart', 'series', call))(chart, series);
    } catch (error) {
      console.error('Error executing:', call, '\nError:', error);
    }
  }
  const initialCalls = model.get('_js_calls');
  initialCalls.forEach(executeCall);
  processedCallCount = initialCalls.length;
  model.on('change:_js_calls', () => {
    const currentCalls = model.get('_js_calls');
    while (processedCallCount < currentCalls.length) {
      executeCall(currentCalls[processedCallCount]);
      processedCallCount++;
    }
  });
  const resizeObserver = new ResizeObserver(entries => {
    const { width, height } = entries[0].contentRect;
    chart.applyOptions({ width, height });
  });
  resizeObserver.observe(container);
  return () => {
    resizeObserver.disconnect();
    chart.remove();
  };
}

export default { render };