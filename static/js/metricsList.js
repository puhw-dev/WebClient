function getMetrics(hostname, sensorname, monitorIP) {
    $.get(
        "/monitor/hosts/" + hostname + "/sensors/" + sensorname + "/metrics", 
        {
            "ip": monitorIP
        },
        function(data) {
            $("#available_metrics").html(""); // cleanup before append all the metrics
            data.metrics.forEach(function(metric) {
                $("#available_metrics").append("<li>" + metric.name + "</li>");
        });
    });
}