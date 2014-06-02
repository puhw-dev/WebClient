$(document).ready(function() {
    $("#autorefresh").on("change", function() {
        var refreshEvery = this.value

        if (refreshEvery == "disabled") {
            clearInterval(metricRefreshInterval);
        } else {
            metricRefreshInterval = setInterval(function() { refreshCurrentMetricFunction(); }, parseInt(refreshEvery) * 1000);
        }
    });

    $("#apply_plot_parameters").click(function() {
        refreshCurrentMetricFunction();
    });
});