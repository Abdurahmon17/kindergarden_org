document.addEventListener('DOMContentLoaded', () => {
    console.log('WebSocket script loaded');
    // Placeholder: Implement WebSocket connection
    // Example: Update stock count and alerts
    document.getElementById('stock-count').textContent = '10 mahsulot';
    document.getElementById('report-status').textContent = '5 hisobot mavjud';
    const alerts = document.getElementById('stock-updates');
    alerts.textContent = 'Omborda kam qolgan mahsulotlar yo‘q';
    alerts.classList.remove('hidden');
});