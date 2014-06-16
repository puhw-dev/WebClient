google.load("visualization", "1", {packages:["corechart"]});

function displayMetricData(monitorIP, hostname, sensorname, sensortype, metricname) {
    $("#placeholder").hide();
    $("#metric_data").fadeIn();
    $.get(
        "/monitor/hosts/" + hostname + "/sensors/" + sensorname + "/metrics/" + metricname, 
        {
            "ip": monitorIP,
            "number_of_datapoints": $("#number_of_datapoints").val()
        },
        function(data) {
            $("#metric_name").html(metricname);

            // It shouldn't be based on sensor name but it's hardcoded like this cause we don't provide info about type of metric in Catalog's API
            if (sensortype.toLowerCase().indexOf("system info") > -1) {
                $("#chart_div").hide();
                $("#text_data").fadeIn();

                var metricValue = 'No value';
                var singleMetricValue = data.metrics[2].data[0];
                for (var val in singleMetricValue) {
                    metricValue = singleMetricValue[val];
                }

                $("#metric_value").html(metricValue);

            } else {
                $("#text_data").hide();
                $("#chart_div").fadeIn();
                var chartData = new google.visualization.DataTable();

                var options = {
                    title: metricname
                }

                chartData.addColumn('datetime', 'Time');
                chartData.addColumn('number', metricname);

                var metricData = data.metrics[2].data;

                metricData.forEach(function(row) {
                    for (var time in row) {
                        var date = new Date(time*1000);
                        var value = parseInt(row[time]);
                        chartData.addRow([date, value]);
                    }
                });

                var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
                chart.draw(chartData, options);
            } 
        }
    );
}

