$(document).ready(function() {
    $("#available_sensors").select2({width: "element"});

    $("#available_sensors").on("select2-selecting", function(eventObject) {
        var sensorname = $(this).val();

        var hostname = eventObject.object.element[0].attributes["data-hostname"].value;
        var monitorIP = eventObject.object.element[0].attributes["data-monitor-ip"].value;
        // plz kill me for this chains... 

        getMetrics(hostname, sensorname, monitorIP);
    });
});