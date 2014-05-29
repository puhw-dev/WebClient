function getMetrics(hostname, sensorname, monitorIP) {
    $.get(
        "/monitor/hosts/" + hostname + "/sensors/" + sensorname + "/metrics", 
        {
            "ip": monitorIP
        },
        function(data) {
            $("#available_metrics").html(""); // cleanup before append all the metrics
            data.metrics.forEach(function(metric) {
                $("#available_metrics").append("<option>" + metric.name + "</option>");
            });

            if (data.metrics.length == 0) {
                $("#available_metrics").append("<option>No metrics, sorry dude</option>");
            }
        }
    );
}