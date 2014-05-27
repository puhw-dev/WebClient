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
			return { 'name' : node.id };
			}
		}
	}});

	$('#jstree').on("select_node.jstree", function(node, selected, event) {
		if (selected.node.parent != '#') {
			loadSensorsForHost(selected.node.text); // it definitely shouldn't be based on node's text ;-)
		}
	});
	});

	function loadSensorsForHost(hostname) {
	$.get("/monitor/hosts/" + hostname + "/sensors/", function(data) {

		var available_sensors = $("#available_sensors");
		available_sensors.html(""); // clean the list

        getMetrics(hostname, data.sensors[0].sensorname);

		data.sensors.forEach(function(sensor) {
			available_sensors.append('<option value="omg">' + sensor.sensorname + '</option>');
		});

		available_sensors.select2({width: "element"});
	});
}
