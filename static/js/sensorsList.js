$(document).ready(function() {
    $("#available_sensors").select2({width: "element"});

    $("#available_sensors").on("select2-selecting", function() {
        var hostname = "dummy";
        var sensorname = $(this).val();

        getMetrics(hostname, sensorname);

    });

});