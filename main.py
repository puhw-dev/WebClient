#!/usr/bin/python
import os
import requests
import json
import math
import logging
from threading import Thread
from flask import Flask
from flask import render_template, Response, request
from random import random
from catalog_data_provider import CatalogDataProvider
from monitor_data_provider import MonitorDataProvider
from search_worker import generate_search_data_background_task

app = Flask(__name__, static_path="/static", static_url_path="/static")
app.config.from_pyfile("config.py")

catalog_data_provider = CatalogDataProvider(app.config.get("CATALOG_HOST"))

log = logging.getLogger()

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/catalog/monitors")
def monitors_list():
    """Returns monitors list in json from catalog"""

    monitors_data = json.loads(catalog_data_provider.get_monitors())

    # list needs to be a bit modified for jsTree
    monitor_names = [{"text": monitor["name"], "id": monitor["ip"], "children": True} for monitor in monitors_data]
    json_tree_data = json.dumps(monitor_names)

    return Response(json_tree_data, mimetype='application/json')


@app.route("/monitor/hosts")
def hosts_list():
    """Returns hosts list for specified monitor"""
    monitor_ip = request.args["ip"]
    monitor_data_provider = MonitorDataProvider(monitor_ip)

    try:
        hosts_list_data = json.loads(monitor_data_provider.get_hosts())
    except requests.Timeout:
        return Response("Timeout", 408)

    # list needs to be a bit modified for jsTree
    list_of_hosts = [{"text": host["hostname"]} for host in hosts_list_data["hosts"]]

    return Response(json.dumps(list_of_hosts), mimetype='application/json')


@app.route("/monitor/hosts/<hostname>/sensors/")
def sensors_list(hostname):
    """Returns sensors list for specified host"""
    monitor_ip = request.args["ip"]
    monitor_data_provider = MonitorDataProvider(monitor_ip)

    try:
        sensors_list_data = monitor_data_provider.get_sensors(hostname)
    except requests.Timeout:
        return Response("Timeout", 408)

    return Response(sensors_list_data, mimetype='application/json')


@app.route("/monitor/hosts/<hostname>/sensors/<sensorname>/metrics")
def metrics_list(hostname, sensorname):
    """Returns metrics list for specified host, sensor and monitor"""
    monitor_ip = request.args["ip"]
    monitor_data_provider = MonitorDataProvider(monitor_ip)

    try:
        metrics_list_data = monitor_data_provider.get_metrics(hostname, sensorname)
    except requests.Timeout:
        return Response("Timeout", 408)

    return Response(metrics_list_data, mimetype='application/json')


@app.route("/monitor/hosts/<host_name>/sensors/<sensor_name>/metrics/<metric_name>")
def metric_data(host_name, sensor_name, metric_name):
    """Returns metric data"""
    monitor_ip = request.args["ip"]
    number_of_datapoints = request.args["number_of_datapoints"]
    monitor_data_provider = MonitorDataProvider(monitor_ip)

    try:
        metric_data_json = monitor_data_provider.get_metric_data(host_name, sensor_name, metric_name, number_of_datapoints)
    except requests.Timeout:
        return Response("Timeout", 408)

    return Response(metric_data_json, mimetype='application/json')


@app.route("/search")
def search():
    """Method which filters search results from file"""
    search_data_file = open('search_data.json', 'r')
    search_data = json.load(search_data_file)

    # filtering
    search_phrase = request.args["s"]
    search_results = filter(lambda entity: search_phrase.lower() in entity["name"].lower(), search_data)

    return Response(json.dumps(search_results), mimetype='application/json')


@app.route("/create-compound-metric/<host_name>/<sensor_name>/<metric_name>", methods=['POST'])
def create_compound_metric(host_name, sensor_name, metric_name):
    name = request.form["name"]
    rpm = request.form["rpm"]
    average = request.form["average"]
    login = request.form["login"]
    password = request.form["password"]
    monitor_ip = request.form["monitor_ip"]

    request_data = {'compoundMetricName': name, 'rpm': rpm, 'average': average, 'login': login, 'password': password}

    response = requests.post("http://" + monitor_ip + "/hosts/" + host_name + "/sensors/" + sensor_name + "/metrics/" + metric_name, data=json.dumps(request_data))

    return Response(response.content, response.status_code)


@app.route("/delete-compound-metric/<host_name>/<sensor_name>/<metric_name>", methods=['POST'])
def delete_compound_metric(host_name, sensor_name, metric_name):
    login = request.form["login"]
    password = request.form["password"]
    monitor_ip = request.form["monitor_ip"]

    request_data = {'login': login, 'password': password}

    response = requests.delete("http://" + monitor_ip + "/hosts/" + host_name + "/sensors/" + sensor_name + "/metrics/" + metric_name, data=json.dumps(request_data))

    return Response(response.content, response.status_code)


if __name__ == "__main__":

    # background thread which generates search data
    generate_search_background_thread = Thread(target=generate_search_data_background_task,
                                               name="SearchGenThread")
    generate_search_background_thread.start()

    # main flask app
    port = int(os.getenv('PORT', 80))
    env = os.getenv('PUHW_ENV', 'DEV')
    if env == 'DEV':
        app.run(use_debugger=True, use_reloader=True, debug=True, port=port, threaded=True)
    else:
        app.run(host='0.0.0.0', use_debugger=False, use_reloader=False, debug=False, port=port, threaded=True)
