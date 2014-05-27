#!/usr/bin/python
import os
import requests
from flask import Flask
from flask import render_template, Response, request
from string import replace
from random import random
import json
import math

app = Flask(__name__, static_path="/static", static_url_path="/static")
if os.getenv('ENV', 'DEV') == "HEROKU":
    app.config.from_pyfile("config_heroku.py")
else:
    app.config.from_pyfile("config.py")

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/catalog/monitors")
def monitors_list():
    catalog_address = app.config.get("CATALOG_ADDRESS")
    monitors_list_request = requests.get(catalog_address + "/monitors")

    json_data = monitors_list_request.text

    monitors_data = json.loads(json_data)

    monitor_names = [{"text": monitor["name"], "id": monitor["name"], "children": True} for monitor in monitors_data]
    json_tree_data = json.dumps(monitor_names)

    return Response(json_tree_data, mimetype='application/json')

@app.route("/monitor/hosts")
def hosts_list():
    # mocked data
    # TODO: it should be request to {monitorURI}/hosts/ (GET)
    monitor_name = request.args["name"]
    list_of_hosts = ["host1", "host2", "host3"]
    return Response(json.dumps(list_of_hosts), mimetype='application/json')

@app.route("/monitor/hosts/<hostname>/sensors/")
def sensors_list(hostname):
    # mocked data again ;-)
    # TODO: it should be request to {monitorURI}/hosts/{hostname}/sensors/ (GET)
    dummy_data = '''{
        "hostname": "%(hostname)s", "ip" : "10.0.1.128", "href": "http://10.0.0.1/hosts/%(hostname)s",
        "sensors": [{
        "sensorname": "sensor1_for_%(hostname)s", "owner": "user1", "rpm": "10",
        "href": "http://10.0.0.1/hosts/%(hostname)s/sensors/sensor1"
        },{
        "sensorname": "sensor2_for_%(hostname)s", "owner": "user1", "rpm": "10",
        "href": "http://10.0.0.1/hosts/%(hostname)s/sensors/sensor2"
        },{
        "sensorname": "superduper_third_sensor_for_%(hostname)s_host", "owner": "user1", "rpm": "10",
        "href": "http://10.0.0.1/hosts/%(hostname)s/sensors/sensor2"
        }]
        }'''

    dummy_data = dummy_data % {"hostname": hostname}

    return Response(dummy_data, mimetype='application/json')

@app.route("/monitor/hosts/<hostname>/sensors/<sensorname>/metrics")
def metrics_list(hostname, sensorname):
    dummy_data = '''{
        "sensorname": "%(sensorname)s",
        "hostname": "%(hostname)s",
        "owner": "user1", "rpm": "10",
        "href": "http://10.0.0.1/hosts/box/sensors/sensor1",
        "metrics": [{
        "name": "metric1", "href": "http://10.0.0.1/hosts/box/sensors/sensor1/metrics/metric1"
        },{
        "name": "metric2", "href": "http://10.0.0.1/hosts/box/sensors/sensor1/metrics/metric1"
        }]
        }'''

    dummy_data = dummy_data % {"hostname": hostname, "sensorname": sensorname}

    return Response(dummy_data, mimetype='application/json')


@app.route("/json_sin")
def json_sin():
    values = [["x", "y"]]
    for x in range(0, 100):
        values.append([x/10., math.sin(x/10.) + random()])
    return Response(json.dumps(values), mimetype='application/json')

if __name__ == "__main__":
    port = int(os.getenv('PORT', 80))
    app.run(use_debugger=True, use_reloader=True, debug=True, port=port)
