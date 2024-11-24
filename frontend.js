$(document).ready(function() {
    // Function to fetch and display reports
    function fetchReports() {
        $.ajax({
            url: '/fetch-reports', // URL to fetch reports from backend
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                // Clear existing reports
                $('#report-list').empty();
                // Add new reports to the list
                data.reports.forEach(function(report) {
                    $('#report-list').append('<li><a href="#">' + report[1] + '</a></li>');
                });
            },
            error: function(xhr, status, error) {
                console.error('Error fetching reports:', error);
            }
        });
    }

    // Call fetchReports function initially
    fetchReports();

    // Periodically fetch reports every 5 seconds (adjust as needed)
    setInterval(fetchReports, 5000);
});
