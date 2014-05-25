$(document).ready(function() {
    $('#jstree').jstree({
      'core' : {
        'data' : {
          'url' : function (node) {
            return node.id === '#' ?
              '/monitors_list' :
              '/monitor';
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
    $.get("/monitor/" + hostname + "/sensors/", function(data) {

        var available_sensors_container = $("#available_sensors_container");
        available_sensors_container.html(""); // clean the list

        data.sensors.forEach(function(sensor) {
            available_sensors_container.append("<li>" + sensor.sensorname + "</li>");
        });

    });
}
