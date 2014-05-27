function getMetrics(hostname, sensorname) {
    $.get("/monitor/hosts/" + hostname + "/sensors/" + sensorname + "/metrics", function(data) {
        $("#available_metrics").html(""); // cleanup before append all the metrics
        data.metrics.forEach(function(metric) {
            $("#available_metrics").append("<li>" + metric.name + "</li>");
        });
    });
}