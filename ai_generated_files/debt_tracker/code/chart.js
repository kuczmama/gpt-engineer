// JavaScript file for chart.js

/**
 * Function to create a chart displaying the national debt
 * @param {HTMLCanvasElement} canvas - The canvas element to render the chart
 * @param {string} debt - The national debt
 */
function createDebtChart(canvas, debt) {
  var ctx = canvas.getContext('2d');
  var chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['United States Debt'],
      datasets: [
        {
          label: 'Debt in trillions of dollars',
          data: [debt],
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              return value.toLocaleString();
            },
          },
        },
      },
    },
  });
}