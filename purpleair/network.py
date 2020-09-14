"""
PurpleAir API Client Class
"""


import json
import time
from json.decoder import JSONDecodeError
from typing import List

import pandas as pd
import requests

from .api_data import API_ROOT
from .sensor import Sensor


class SensorList():
    """
    PurpleAir Sensor Network Representation
    """

    def __init__(self, parse_location=False):
        self.parse_location = parse_location

        self.data = {}
        self.get_all_data()  # Populate `data`

        self.all_sensors: List[Sensor] = []
        self.generate_sensor_list()  # Populate `all_sensors`

        # Commonly requested/used filters
        self.outside_sensors: List[Sensor] = [
            s for s in self.all_sensors if s.location_type == 'outside']
        self.useful_sensors: List[Sensor] = [
            s for s in self.all_sensors if s.is_useful()]

    def get_all_data(self) -> None:
        """
        Get all data from the API
        """
        response = requests.get(f'{API_ROOT}')
        try:
            data = json.loads(response.content)
        except JSONDecodeError as err:
            raise ValueError(
                'Invalid JSON data returned from network!') from err

        # Handle rate limit or other error message
        if 'results' not in data:
            message = data.get('message')
            error_message = message if message is not None else data
            raise ValueError(
                f'No sensor data returned from PurpleAir: {error_message}')

        print(f"Initialized {len(data['results']):,} sensors!")
        self.data = data['results']

    def generate_sensor_list(self) -> None:
        """
        Generator for Sensor objects, delated if `parse_location` is true per Nominatim policy
        """
        if self.parse_location:
            # pylint: disable=line-too-long
            print('Warning: location parsing enabled! This reduces sensor parsing speed to less than 1 per second.')
        for sensor in self.data:
            if self.parse_location:
                # Required by https://operations.osmfoundation.org/policies/nominatim/
                time.sleep(1)
            self.all_sensors.append(Sensor(sensor['ID'],
                                           json_data=sensor,
                                           parse_location=self.parse_location))

    def to_dataframe(self, sensor_group: str) -> pd.DataFrame:
        """
        Converts dictionary representation of a list of sensors to a Pandas DataFrame
        where sensor_group determines which group of sensors are used
        """
        if sensor_group not in {'useful', 'outside', 'all'}:
            raise ValueError(f'{sensor_group} is an invalid sensor group!')
        if sensor_group == 'all':
            sensor_data = pd.DataFrame([s.as_flat_dict()
                                        for s in self.all_sensors])
        elif sensor_group == 'outside':
            sensor_data = pd.DataFrame([s.as_flat_dict()
                                        for s in self.outside_sensors])
        elif sensor_group == 'useful':
            sensor_data = pd.DataFrame([s.as_flat_dict()
                                        for s in self.useful_sensors])
        sensor_data.index = sensor_data.pop('id')
        return sensor_data
