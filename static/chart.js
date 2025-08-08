document.addEventListener('DOMContentLoaded', function () {
  const labels = JSON.parse(document.getElementById('chart-data').dataset.labels);
  const amounts = JSON.parse(document.getElementById('chart-data').dataset.amounts);

  const ctx = document.getElementById('expenseChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Expenses',
        data: amounts,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function(value) {
              return '₦' + value.toLocaleString();
            }
          }
        }
      }
    }
  });
});
