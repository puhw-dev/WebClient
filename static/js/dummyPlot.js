google.load("visualization", "1", {packages:["corechart"]});
// google.setOnLoadCallback(drawChart);

function drawChart(dataArray) {
    var data = google.visualization.arrayToDataTable(dataArray);

    var options = {
      title: 'Dummy sinus'
    };

    var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

function getDataAndPlot() {
    $.get("/json_sin", function(data) {
      drawChart(data);
    });
}

$(document).ready(function() {
    getDataAndPlot();

    $("#refresh_plot").click(function() {
      getDataAndPlot();
    });
});
