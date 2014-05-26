#!/usr/bin/python
import os
from flask import Flask
from flask import render_template, jsonify, Response, request
from string import replace
from random import random
import json
import math

app = Flask(__name__, static_path="/static", static_url_path="/static")

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/monitors_list")
def monitors_list():
    # mocked dummy data
    # TODO: replace with data from catalog when it'll be ready
    # This json data is based on API documentation
    json_data = '''[{
        "name": "monitor1", "ip": "10.0.0.1", "href": "{catalog-uri}/monitors/monitor1"
        },{
        "name": "monitor2", "ip": "10.0.0.2", "href": "{catalog-uri}/monitors/monitor2"
        }]'''
    catalog_url = request.url_root  # now it's just webgui URL
    json_data = replace(json_data, "{catalog-uri}", catalog_url)

    monitors_data = json.loads(json_data)

    monitor_names = [{"text": monitor["name"], "id": monitor["name"], "children": True} for monitor in monitors_data]
    json_tree_data = json.dumps(monitor_names)

    return Response(json_tree_data, mimetype='application/json')

@app.route("/monitor")
def hosts_list():
    # mocked data
    # TODO: it should be request to {monitorURI}/hosts/ (GET)
    monitor_name = request.args["name"]
    list_of_hosts = ("Sample list of hosts loaded with AJAX call for " + monitor_name).split(" ")
    return Response(json.dumps(list_of_hosts), mimetype='application/json')

@app.route("/monitor/<hostname>/sensors/")
def sensors_list(hostname):
    # mocked data again ;-)
    # TODO: it should be request to {monitorURI}/hosts/{hostname}/sensors/ (GET)
    dummy_data = '''{
        "hostname": "%(hostname)s", "ip" : "10.0.1.128", "href": "http://10.0.0.1/hosts/%(hostname)s",
        "sensors": [{
        "sensorname": "sensor1 for '%(hostname)s' host", "owner": "user1", "rpm": "10",
        "href": "http://10.0.0.1/hosts/%(hostname)s/sensors/sensor1"
        },{
        "sensorname": "sensor2 for '%(hostname)s' host", "owner": "user1", "rpm": "10",
        "href": "http://10.0.0.1/hosts/%(hostname)s/sensors/sensor2"
        },{
        "sensorname": "superduper third sensor for '%(hostname)s' host", "owner": "user1", "rpm": "10",
        "href": "http://10.0.0.1/hosts/%(hostname)s/sensors/sensor2"
        }]
        }'''

    dummy_data = dummy_data % {"hostname": hostname}

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
