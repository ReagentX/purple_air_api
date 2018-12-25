import json
import requests
import requests_cache
from datetime import timedelta
from api_data import API_ROOT
from geopy.geocoders import Nominatim


# Setup cache for requests
requests_cache.install_cache(expire_after=timedelta(hours=24))


class Sensor():
    """Class for a single PurpleAir sensor; set initialize=True to fetch data from the API"""
    def __init__(self, id, json=None, parse_location=False):
        self.id = id
        self.json = json
        self.data = self.get_data()
        self.parse_location = parse_location  # Disables some slow features
        self.setup()


    def get_data(self):
        # Fetch the JSON and exclude the child sensors
        if not self.json:
            response = requests.get(f'{API_ROOT}?show={self.id}')
            data = json.loads(response.content)
            return data['results'][0]
        else:
            return self.json


    def setup(self):
        if not self.parse_location:
            self.location = self.get_location()


    def get_location(self):
        lat = self.data['Lat']
        lon = self.data['Lon']
        geolocator = Nominatim(user_agent="purple_air_api")
        location = geolocator.reverse(f'{lat}, {lon}')
        print(location.raw['display_name'])
        return location


    def __repr__(self):
        if not self.parse_location:
            return f"Sensor {self.id} at {self.location.raw['city']}"
        else:
            return f"Sensor {self.id}"