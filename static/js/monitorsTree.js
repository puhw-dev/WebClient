$(document).ready(function() {
	$('#jstree').jstree({
		'core' : {
            'data' : {
                'url' : function (node) {
                    return node.id === '#' ?
                        '/catalog/monitors' :
                        '/monitor/hosts';
                },
                'data' : function (node) {
                    return { 'ip': node.id };
                }
            }
        }
	});

	$('#jstree').on("select_node.jstree", function(node, selected, event) {
		if (selected.node.parent != '#') {
			loadSensorsForHost(selected.node.parent, selected.node.text); // it definitely shouldn't be based on node's text ;-)
		}
	});
});

function loadSensorsForHost(monitor_ip, hostname) {
	$.get(
	    "/monitor/hosts/" + hostname + "/sensors/",
	    {
            "ip": monitor_ip
	    },
	    function(data) {
            var available_sensors = $("#available_sensors");
            available_sensors.html(""); // clean the list

            data.sensors.forEach(function(sensor) {
                available_sensors.append('<option value="' + sensor.sensorname + '" data-monitor-ip="' + monitor_ip +'" data-hostname="' + hostname +'">' + sensor.sensorname + '</option>');
            });

            getMetrics(hostname, data.sensors[0].sensorname, monitor_ip);
	    }
	);
}
