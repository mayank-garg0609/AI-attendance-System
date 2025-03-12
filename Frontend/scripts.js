const ctx = document.getElementById('attendanceChart').getContext('2d');
function updateTime() {
    const now = new Date();

    // Format time
    const timeOptions = { hour: '2-digit', minute: '2-digit', second: '2-digit' };
    const currentTime = now.toLocaleTimeString('en-US', timeOptions);

    // Format date
    const dateOptions = { day: 'numeric', month: 'long', year: 'numeric' };
    const currentDate = now.toLocaleDateString('en-GB', dateOptions);

    // Update elements
    document.getElementById('current-time').textContent = currentTime;
    document.getElementById('current-date').textContent = currentDate;

    // Refresh every second
    setTimeout(updateTime, 1000);
}

// Initialize time on page load
window.onload = updateTime;

document.getElementById('sort-options').addEventListener('change', function() {
    const sortBy = this.value;
    const table = document.getElementById('attendance-table').getElementsByTagName('tbody')[0];
    const rows = Array.from(table.getElementsByTagName('tr'));

    const sortedRows = rows.sort((a, b) => {
        const attendanceA = parseInt(a.cells[4].textContent.replace('%', ''));
        const attendanceB = parseInt(b.cells[4].textContent.replace('%', ''));
        const idA = parseInt(a.cells[0].textContent);
        const idB = parseInt(b.cells[0].textContent);
        const nameA = a.cells[1].textContent.toLowerCase();
        const nameB = b.cells[1].textContent.toLowerCase();

        switch (sortBy) {
            case 'id':
                return idA - idB;
            case 'name':
                return nameA.localeCompare(nameB);
            case 'attendance-asc':
                return attendanceA - attendanceB;
            case 'attendance-desc':
                return attendanceB - attendanceA;
            case 'less-than-75':
                return attendanceA < 75 ? -1 : 1;
            default:
                return 0;
        }
    });

    // Clear and re-append sorted rows
    table.innerHTML = '';
    sortedRows.forEach(row => table.appendChild(row));
});



new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['02 Mar', '03 Mar', '04 Mar', '05 Mar', '06 Mar', '07 Mar', '08 Mar'],
        datasets: [{
            label: 'Attendance Rate',
            data: [70, 60, 80, 91, 70, 60, 75],
            borderColor: '#4A90E2',
            backgroundColor: 'rgba(74, 144, 226, 0.1)',
            fill: true
        }]
    },
    options: {
        scales: {
            y: { beginAtZero: true }
        }
    }
});
