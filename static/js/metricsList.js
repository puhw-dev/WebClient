var refreshCurrentMetricFunction = null;
var metricRefreshInterval = null;

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

$(document).ready(function() {
    $("#available_metrics").on("change", function() {
        var metricname = this.value
        var hostname = $(this).find(':selected').data('host-name');
        var sensorname = $(this).find(':selected').data('sensor-name');
        var monitorIP = $(this).find(':selected').data('monitor-ip');

        refreshCurrentMetricFunction = function() { displayMetricData(monitorIP, hostname, sensorname, metricname); }
        refreshCurrentMetricFunction();

    });

});