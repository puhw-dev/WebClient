$(document).ready(function() {
    $("#add-compound-metric-button").click(function() {
        var available_metrics = $("#available_metrics");
        var metricname = available_metrics.val();
        var hostname = available_metrics.find(':selected').data('host-name');
        var sensorname = available_metrics.find(':selected').data('sensor-name');
        var monitorIP = available_metrics.find(':selected').data('monitor-ip');

        var comp_metric_name = $("#comp-metric-name").val();
        var comp_metric_average = $("#comp-metric-average").val();
        var comp_metric_rpm = $("#comp-metric-rpm").val();
        var login = $("#comp-metric-login").val();
        var password = $("#comp-metric-password").val();

        $.post("/create-compound-metric/" + hostname + "/" + sensorname + "/" + metricname,
            { name: comp_metric_name,
              average: comp_metric_average,
              rpm: comp_metric_rpm,
              login: login,
              password: password,
              monitor_ip: monitorIP}, function(data, textStatus, jqXHR) {
                var message = JSON.parse(data).message;
                alert(message);
                getMetrics(hostname, sensorname, monitorIP);
              }).error(function(data, textStatus, jqXHR) {
                var message = JSON.parse(data.responseText).message;
                alert(message + " (" + data.status + ")");
                });
    });
});