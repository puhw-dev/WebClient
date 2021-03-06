import requests


class MonitorDataProvider:

    request_timeout = 0
    monitor_ip = ""

    def __init__(self, monitor_ip, request_timeout=30):
        self.monitor_ip = monitor_ip
        self.request_timeout = request_timeout

    def get_hosts(self):
        return self.monitor_request("/hosts")

    def get_sensors(self, hostname):
        return self.monitor_request("/hosts/" + hostname + "/sensors")

    def get_metrics(self, hostname, sensor):
        return self.monitor_request("/hosts/" + hostname + "/sensors/" + sensor + "/metrics")

    def get_metric_data(self, hostname, sensor, metric, number_of_datapoints=50):
        return self.monitor_request("/hosts/" + hostname + "/sensors/" + sensor + "/metrics/" + metric + "/data?n=" + number_of_datapoints)

    def monitor_request(self, url):
        """Performs GET request to monitor based on path"""
        full_url = "http://" + self.monitor_ip + url
        get_request = requests.get(full_url, timeout=self.request_timeout)
        return get_request.text
