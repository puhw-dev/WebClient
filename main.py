#!/usr/bin/python
import os
import requests
import json
import math
import time
from threading import Thread
from flask import Flask
from flask import render_template, Response, request
from random import random
import logging

# logging
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
log = logging.getLogger()
log.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)

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


@app.route("/search")
def search():
    search_data_file = open('search_data.json', 'r')
    search_data = json.load(search_data_file)

    # filtering
    search_phrase = request.args["s"]
    search_results = filter(lambda entity: search_phrase.lower() in entity["name"].lower(), search_data)

    return Response(json.dumps(search_results), mimetype='application/json')


@app.route("/json_sin")
def json_sin():
    """Method which returns sinus with random noise as json - for charts testing purposes"""
    values = [["x", "y"]]
    for x in range(0, 100):
        values.append([x/10., math.sin(x/10.) + random()])
    return Response(json.dumps(values), mimetype='application/json')


def generate_search_data():
    log.info("Generating search data")

    catalog_address = app.config.get("CATALOG_HOST")
    monitors_list_request = requests.get(catalog_address + "/monitors")
    monitors_data = json.loads(monitors_list_request.text)

    monitors = [{"type": "monitor", "name": monitor["name"], "ip": monitor["ip"]} for monitor in monitors_data]

    search_data = list(monitors)

    # for each monitor get list of hosts
    for monitor in monitors:
        try:
            hosts_data = monitor_get_request(monitor["ip"], "/hosts")
            hosts_data_list = json.loads(hosts_data)

            # for each host get list of sensors
            for host in hosts_data_list["hosts"]:
                search_data.append({"type": "host", "monitor": monitor["name"], "name": host["hostname"]})

                sensors_data = monitor_get_request(monitor["ip"], "/hosts/" + host["hostname"] + "/sensors")
                sensors_data_list = json.loads(sensors_data)

                # for each sensor get list of metrics
                for sensor in sensors_data_list["sensors"]:
                    search_data.append({"type": "sensor", "monitor": monitor["name"], "host": host["hostname"], "name": sensor["sensorname"]})

                    metrics_data = monitor_get_request(monitor["ip"], "/hosts/" + host["hostname"] + "/sensors/" + sensor["sensorname"] + "/metrics")
                    metrics_data_list = json.loads(metrics_data)

                    for metric in metrics_data_list["metrics"]:
                        search_data.append({"type": "metric", "monitor": monitor["name"], "host": host["hostname"], "sensorname": sensor["sensorname"], "name": metric["name"]})

        except requests.Timeout:
            pass  # Just ignore timeouts, if any of endpoints is down we can't do anything about that.
            # It's also quite good protection from invalid data about monitors (during development).

    search_data_file = open('search_data.json', 'w')
    search_data_file.write(json.dumps(search_data))

    log.info("Search data generated")


def generate_search_data_background_task():
    while True:
        generate_search_data()
        time.sleep(60)


if __name__ == "__main__":

    # background thread which generates search data
    generate_search_background_thread = Thread(target=generate_search_data_background_task,
                                               name="SearchGenThread")
    generate_search_background_thread.start()

    # main flask app
    port = int(os.getenv('PORT', 80))
    env = os.getenv('PUHW_ENV', 'DEV')
    if env == 'DEV':
        app.run(use_debugger=True, use_reloader=False, debug=True, port=port)
    else:
        app.run(use_debugger=False, use_reloader=False, debug=False, port=port)
