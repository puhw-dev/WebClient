import config
import time
import json
import requests
import logging
from catalog_data_provider import CatalogDataProvider
from monitor_data_provider import MonitorDataProvider

# logging
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
log = logging.getLogger()
log.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)

catalog_data_provider = CatalogDataProvider(config.CATALOG_HOST)


def generate_search_data_background_task():
    while True:
        generate_search_data()
        time.sleep(config.SEARCH_DATA_REFRESH_INTERVAL)


def generate_search_data():
    """Generates data for search functionality.
    It asks each monitors for hosts, host for sensors and sensors for metrics.
    Saves data in file (JSON format).
    It's really simple solution and I'm aware of the fact that it isn't the best regarding performance and scalability
    but as long as we've got only a few monitors, sensors and metrics it should be okay, otherwise it would be nice
    to have sth faster, probably based on db."""

    log.info("Generating search data")

    monitors_data = json.loads(catalog_data_provider.get_monitors())
    monitors = [{"type": "monitor", "name": monitor["name"], "ip": monitor["ip"]} for monitor in monitors_data]

    search_data = list(monitors)

    # for each monitor get list of hosts
    for monitor in monitors:
        try:
            monitor_data_provider = MonitorDataProvider(monitor["ip"], config.REQUEST_TIMEOUT)
            hosts_data = json.loads(monitor_data_provider.get_hosts())

            # for each host get list of sensors
            for host in hosts_data["hosts"]:
                search_data.append({"type": "host", "monitor": monitor["name"], "name": host["hostname"]})

                sensors_data = json.loads(monitor_data_provider.get_sensors(host["hostname"]))

                # for each sensor get list of metrics
                for sensor in sensors_data["sensors"]:
                    search_data.append({"type": "sensor", "monitor": monitor["name"], "host": host["hostname"], "name": sensor["sensorname"]})

                    metrics_data = json.loads(monitor_data_provider.get_metrics(host["hostname"], sensor["sensorname"]))

                    for metric in metrics_data["metrics"]:
                        search_data.append({"type": "metric", "monitor": monitor["name"], "host": host["hostname"], "sensor": sensor["sensorname"], "name": metric["name"]})

        except requests.Timeout:
            pass  # Just ignore timeouts, if any of endpoints is down we can't do anything about that.
            # It's also quite good protection from invalid data about monitors (during development).

    search_data_file = open('search_data.json', 'w')
    search_data_file.write(json.dumps(search_data))

    log.info("Search data generated")


if __name__ == "__main__":
    generate_search_data_background_task()
