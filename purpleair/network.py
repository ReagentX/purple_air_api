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

        parsed_data = self.parse_raw_result(data['results'])

        print(f"Initialized {len(parsed_data):,} sensors!")
        self.data = parsed_data

    def parse_raw_result(self, flat_sensor_data: dict) -> List[List[dict]]:
        """
        O(2n) algorithm to build the network map
        """
        out_l: List[List[dict]] = []

        # First pass: build map of parent and child sensor data
        parent_map = {}
        child_map = {}
        for sensor in flat_sensor_data:
            if 'ParentID' in sensor:
                child_map[sensor['ID']] = sensor
            else:
                parent_map[sensor['ID']] = sensor

        # Second pass: build list of complete sensors
        for child_sensor_id in child_map:
            parent_sensor_id = child_map[child_sensor_id]['ParentID']
            if parent_sensor_id not in parent_map:
                # pylint: disable=line-too-long
                raise ValueError(f'Child {child_sensor_id} lists parent {parent_sensor_id}, but parent does not exist!')
            channels =[
                parent_map[parent_sensor_id],
                child_map[child_sensor_id]
            ]
            del parent_map[parent_sensor_id]  # Any unused parents will be left over
            out_l.append(channels)

        # Handle remaining parent sensors
        for remaining_parent in parent_map:
            channels = [
                parent_map[remaining_parent],
            ]
            out_l.append(channels)

        return out_l

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
            # sensor[0] is always the parent sensor
            self.all_sensors.append(Sensor(sensor[0]['ID'],
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
