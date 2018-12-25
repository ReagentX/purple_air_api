import json
import requests
import requests_cache
from datetime import timedelta
from api_data import API_ROOT
from sensor import Sensor
from itertools import chain


# Setup cache for requests
requests_cache.install_cache(expire_after=timedelta(hours=24))

class PurpleAir():
    """"""
    def __init__(self, parse_location=False):
        self.data = self.get_all_data()
        self.all_sensors = [Sensor(s['ID'], json=s, parse_location=parse_location) for s in self.data]
        self.outside_sensors = [s for s in self.all_sensors if s.location_type == 'outside']
        # self.useful_sensors = 

    def get_all_data(self) -> dict:
        """Get all data from the API"""
        response = requests.get(f'{API_ROOT}')
        data = json.loads(response.content)
        print(f"Initialized {len(data['results'])} sensors!")
        return data['results']

