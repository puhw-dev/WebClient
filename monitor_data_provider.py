import requests


class MonitorDataProvider:

    request_timeout = 0
    monitor_ip = ""

    def __init__(self, monitor_ip, request_timeout=30):
        self.monitor_ip = monitor_ip
        self.request_timeout = request_timeout

    def get_hosts(self):
        return self.monitor_get_request(self.monitor_ip, "/hosts")

    def get_sensors(self, hostname):
        return self.monitor_get_request(self.monitor_ip, "/hosts/" + hostname + "/sensors")

    def get_metrics(self, hostname, sensorname):
        return self.monitor_get_request(self.monitor_ip, "/hosts/" + hostname + "/sensors/" + sensorname + "/metrics")

    def monitor_get_request(self, monitor_ip, url):
        """Performs GET request to monitor based on provided ip and path"""
        full_url = "http://" + monitor_ip + url
        get_request = requests.get(full_url, timeout=self.request_timeout)
        return get_request.text
