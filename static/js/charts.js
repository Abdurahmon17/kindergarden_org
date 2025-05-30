// static/js/charts.js
function initializeCharts(pieData, columnData) {
    const pieCtx = document.getElementById('pieChart').getContext('2d');
    new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: pieData.labels,
            datasets: [{
                data: pieData.data,
                backgroundColor: ['#2563eb', '#10b981'],
                borderColor: '#f9fafb',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' },
                title: { display: true, text: 'Oxirgi Oy Porsiyalari' }
            }
        }
    });

    const columnCtx = document.getElementById('columnChart').getContext('2d');
    new Chart(columnCtx, {
        type: 'bar',
        data: {
            labels: columnData.labels,
            datasets: [{
                label: 'Farq Foizi (%)',
                data: columnData.difference_percent,
                backgroundColor: '#2563eb',
                borderColor: '#1d4ed8',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: false, title: { display: true, text: 'Farq Foizi (%)' } },
                x: { title: { display: true, text: 'Oy' } }
            },
            plugins: {
                legend: { display: false },
                title: { display: true, text: 'Oylik Farq Foizi' }
            }
        }
    });
}