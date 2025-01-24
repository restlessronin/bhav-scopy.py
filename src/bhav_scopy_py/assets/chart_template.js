function render({ model, el }) {
  console.log("Render function called");
  const container = document.createElement('div');
  container.style.width = '100%';
  container.style.height = '100%';
  el.appendChild(container);

  // Create global variables
  const chart = LightweightCharts.createChart(container, model.get('_config'));
  const series = new Map();

  // Execute each JS call in sequence
  function executeCall(call) {
    try {
      console.log("Executing:", call);
      // Make chart and series available directly
      (new Function('chart', 'series', call))(chart, series);
    } catch (error) {
      console.error('Error executing:', call, '\nError:', error);
    }
  }

  model.get('_js_calls').forEach(executeCall);

  // Handle new calls
  model.on('change:_js_calls', () => {
    const newCalls = model.get('_js_calls');
    if (newCalls.length > 0) {
      executeCall(newCalls[newCalls.length - 1]);
    }
  });

  // Handle resizing
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