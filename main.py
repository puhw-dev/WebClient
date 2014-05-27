#!/usr/bin/python
import os
import requests
from flask import Flask
from flask import render_template, Response, request
from random import random
import json
import math

app = Flask(__name__, static_path="/static", static_url_path="/static")
app.config.from_pyfile("config.py")

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/catalog/monitors")
def monitors_list():
    """Returns monitors list in json from catalog"""
    catalog_address = app.config.get("CATALOG_HOST")
    monitors_list_request = requests.get(catalog_address + "/monitors")

    monitors_data = json.loads(monitors_list_request.text)

    # list needs to be a bit modified for jsTree
    monitor_names = [{"text": monitor["name"], "id": monitor["ip"], "children": True} for monitor in monitors_data]
    json_tree_data = json.dumps(monitor_names)

    return Response(json_tree_data, mimetype='application/json')


@app.route("/monitor/hosts")
def hosts_list():
    """Returns hosts list for specified monitor"""
    monitor_ip = request.args["ip"]

    try:
        hosts_list_data = json.loads(monitor_get_request(monitor_ip, "/hosts"))
    except requests.Timeout:
        return Response("Timeout", 408)

    # list needs to be a bit modified for jsTree
    list_of_hosts = [{"text": host["hostname"]} for host in hosts_list_data["hosts"]]

    return Response(json.dumps(list_of_hosts), mimetype='application/json')


@app.route("/monitor/hosts/<hostname>/sensors/")
def sensors_list(hostname):
    """Returns sensors list for specified host"""
    monitor_ip = request.args["ip"]

    try:
        sensors_list_data = monitor_get_request(monitor_ip, "/hosts/" + hostname + "/sensors")
    except requests.Timeout:
        return Response("Timeout", 408)

    return Response(sensors_list_data, mimetype='application/json')


@app.route("/monitor/hosts/<hostname>/sensors/<sensorname>/metrics")
def metrics_list(hostname, sensorname):
    """Returns metrics list for specified host, sensor and monitor"""
    monitor_ip = request.args["ip"]

    try:
        metrics_list_data = monitor_get_request(monitor_ip, "/hosts/" + hostname + "/sensors/" + sensorname + "/metrics")
    except requests.Timeout:
        return Response("Timeout", 408)

    return Response(metrics_list_data, mimetype='application/json')


def monitor_get_request(monitor_ip, url):
    """Performs GET request to monitor based on provided ip and path"""
    full_url = "http://" + monitor_ip + url
    get_request = requests.get(full_url, timeout=app.config.get('REQUEST_TIMEOUT'))
    return get_request.text


@app.route("/json_sin")
def json_sin():
    """Method which returns sinus with random noise as json - for charts testing purposes"""
    values = [["x", "y"]]
    for x in range(0, 100):
        values.append([x/10., math.sin(x/10.) + random()])
    return Response(json.dumps(values), mimetype='application/json')

if __name__ == "__main__":
    port = int(os.getenv('PORT', 80))
    app.run(use_debugger=True, use_reloader=True, debug=True, port=port)
