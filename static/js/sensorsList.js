$(document).ready(function() {

    $("#available_sensors").on("change", function() {
        var sensorname = this.value

        var hostname = $(this).find(':selected').data('hostname');
        var monitorIP = $(this).find(':selected').data('monitor-ip');

        getMetrics(hostname, sensorname, monitorIP);
    });
});