function getMetrics(hostname, sensorname, monitorIP) {
    $.get(
        "/monitor/hosts/" + hostname + "/sensors/" + sensorname + "/metrics", 
        {
            "ip": monitorIP
        },
        function(data) {
            var available_metrics = $("#available_metrics");
            available_metrics.html(""); // cleanup before append all the metrics
            data.metrics.forEach(function(metric) {
                available_metrics.append('<option value="' + metric.name + '" data-monitor-ip="' + monitorIP +'" data-host-name="' + hostname +'" data-sensor-name="' + sensorname + '">' + metric.name + '</option>');
            });

            if (data.metrics.length == 0) {
                available_metrics.append("<option>No metrics, sorry dude</option>");
            }
        }
    );
}

function displayMetricData(monitorIP, hostname, sensorname, metricname) {
    $.get(
        "/monitor/hosts/" + hostname + "/sensors/" + sensorname + "/metrics/" + metricname, 
        {
            "ip": monitorIP
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

$(document).ready(function() {
    $("#available_metrics").on("change", function() {
        var metricname = this.value

        var hostname = $(this).find(':selected').data('host-name');
        var sensorname = $(this).find(':selected').data('sensor-name');
        var monitorIP = $(this).find(':selected').data('monitor-ip');

        displayMetricData(monitorIP, hostname, sensorname, metricname)
    });

});