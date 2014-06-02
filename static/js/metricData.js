function displayMetricData(monitorIP, hostname, sensorname, metricname) {
    $("#placeholder").hide();
    $("#metric_data").fadeIn();
    $.get(
        "/monitor/hosts/" + hostname + "/sensors/" + sensorname + "/metrics/" + metricname, 
        {
            "ip": monitorIP,
            "number_of_datapoints": $("#number_of_datapoints").val()
        },
        function(data) {
            var chartData = new google.visualization.DataTable();

            var options = {
                title: metricname
            }

            chartData.addColumn('datetime', 'Time');
            chartData.addColumn('number', metricname);

            data.metrics[2].data.forEach(function(row) {
                for (var time in row) {
                    var date = new Date(time*1000);
                    var value = parseInt(row[time]);
                    chartData.addRow([date, value]);
                }
            });

            var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
            chart.draw(chartData, options);
        }
    );
}

