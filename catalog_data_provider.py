import requests


class CatalogDataProvider:

    catalog_host = ""

    def __init__(self, catalog_host):
        self.catalog_host = catalog_host

    def get_monitors(self):
        monitors_list_request = requests.get(self.catalog_host + "/monitors")
        return monitors_list_request.text
