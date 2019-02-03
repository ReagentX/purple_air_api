import json
import pandas as pd
import requests
import requests_cache
from datetime import timedelta
from .api_data import API_ROOT
from .sensor import Sensor


# Setup cache for requests
requests_cache.install_cache(expire_after=timedelta(hours=1))
requests_cache.core.remove_expired_responses()

class PurpleAir():
    def __init__(self, parse_location=False):
        self.data = self.get_all_data()
        self.all_sensors = [Sensor(s['ID'], json=s, parse_location=parse_location) for s in self.data]
        self.outside_sensors = [s for s in self.all_sensors if s.location_type == 'outside']
        self.useful_sensors = [s for s in self.all_sensors if s.is_useful()]

    def get_all_data(self) -> dict:
        '''Get all data from the API'''
        response = requests.get(f'{API_ROOT}')
        data = json.loads(response.content)
        print(f"Initialized {len(data['results'])} sensors!")
        return data['results']

    
    def to_dataframe(self, sensor_group: str) -> list:
        '''Converts dictionary representation of a list of sensors to a Pandas Dataframe
        where sensor_group determines which group of sensors are used'''
        if sensor_group not in {'useful', 'outside', 'all'}:
            raise ValueError(f'{sensor_group} is an invalid sensor group!')
        if sensor_group == 'all':
            df = pd.DataFrame([s.as_flat_dict() for s in self.all_sensors])
        elif sensor_group == 'outside':
            df = pd.DataFrame([s.as_flat_dict() for s in self.outside_sensors])
        elif sensor_group == 'useful':
            df = pd.DataFrame([s.as_flat_dict() for s in self.useful_sensors])
        df.index = df.pop('id')
        return df
