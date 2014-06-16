$(document).ready(function() {
    $("#delete-compound-metric-button").click(function() {
        var available_metrics = $("#available_metrics");
        var metricname = available_metrics.val();
        var hostname = available_metrics.find(':selected').data('host-name');
        var sensorname = available_metrics.find(':selected').data('sensor-name');
        var monitorIP = available_metrics.find(':selected').data('monitor-ip');

        var login = $("#comp-metric-login-delete").val();
        var password = $("#comp-metric-password-delete").val();

        $.post("/delete-compound-metric/" + hostname + "/" + sensorname + "/" + metricname,
            {
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