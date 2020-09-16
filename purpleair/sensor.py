"""
PurpleAir Sensor Client
"""


import json
import os
from re import sub

import requests
from geopy.geocoders import Nominatim

from .api_data import API_ROOT
from .channel import Channel


class Sensor():
    """
    Representation of a single PurpleAir sensor
    """

    def __init__(self, identifier, json_data=None, parse_location=False):
        self.identifier = identifier
        self.data = json_data if json_data is not None else self.get_data()
        self.parent_data = self.data[0]
        self.child_data = self.data[1] if len(self.data) > 1 else None
        self.parse_location = parse_location
        self.thingspeak_data = {}
        self.parent = Channel(channel_data=self.parent_data,)
        self.child = Channel(
            channel_data=self.child_data) if self.child_data else None
        self.location_type = self.parent.location_type
        # Parse the location (slow, so must be manually enabled)
        self.location = ''
        if self.parse_location:
            self.get_location()

    def get_data(self) -> dict:
        """
        Get new data if no data is provided
        """
        # Fetch the JSON for parent and child sensors
        response = requests.get(f'{API_ROOT}?show={self.identifier}')
        data = json.loads(response.content)
        channel_data = data.get('results')

        # Handle various API problems
        if channel_data is None:
            raise ValueError(f'Results missing from data: {data}')
        if len(channel_data) == 1:
            print('Child sensor requested, acquiring parent instead.')
            try:
                parent_id = channel_data[0]["ParentID"]
            except IndexError:
                raise IndexError from IndexError(
                    f'Parent sensor for {self.identifier} does not exist!')
            response = requests.get(f'{API_ROOT}?show={parent_id}')
            data = json.loads(response.content)
            channel_data = data.get('results')
        elif len(channel_data) > 2:
            raise ValueError(
                f'More than 2 channels found for {self.identifier}')
        return channel_data

    def get_field(self, field) -> None:
        """
        Gets the thingspeak data for a sensor
        """
        self.thingspeak_data[field] = {'primary': {}, 'secondary': {}}

        # Primary
        self.thingspeak_data[field]['primary']['channel_a'] = json.loads(
            self.parent.thingspeak_primary.get_field(field=field))
        self.thingspeak_data[field]['primary']['channel_b'] = json.loads(
            self.child.thingspeak_primary.get_field(field=field))

        # Secondary
        self.thingspeak_data[field]['secondary']['channel_a'] = json.loads(
            self.parent.thingspeak_secondary.get_field(field=field))
        self.thingspeak_data[field]['secondary']['channel_b'] = json.loads(
            self.child.thingspeak_secondary.get_field(field=field))

    def is_useful(self) -> bool:
        """
        Function to dump broken sensors; expanded like this so we can collect metrics later
        """
        if self.parent.lat is None or self.parent.lon is None:
            return False
        if self.parent.hidden:
            return False
        if self.parent.flagged:
            return False
        if self.parent.downgraded:
            return False
        if self.parent.current_pm2_5 is None:
            return False
        if self.parent.current_temp_f is None:
            return False
        if self.parent.current_humidity is None:
            return False
        if self.parent.current_pressure is None:
            return False
        if not self.parent.channel_data.get('Stats', None):
            # Happens before stats because they will be missing if this is missing
            return False
        if self.parent.last_modified_stats is None:
            return False
        if self.parent.last2_modified is None:
            return False
        return True

    def get_location(self) -> None:
        """
        Set the location for a Sensor using geopy

        UA Rules: https://operations.osmfoundation.org/policies/nominatim/
        We do not want to have every user use the same UA, so we generate one per-user here
        """
        root_ua = 'pypi_purple_air_api_'
        try:
            user_agent = os.getcwd()
            user_agent = root_ua + sub(r'\/|\\| ', '', user_agent)
        except OSError:
            print(
                'Unable to read current direcory name to generate Nominatim user agent!')
            user_agent = f'{root_ua}anonymous_github_com_reagentx_purple_air_api'

        geolocator = Nominatim(user_agent=user_agent)
        location = geolocator.reverse(f'{self.parent.lat}, {self.parent.lon}')
        self.location = location

    def as_dict(self) -> dict:
        """
        Returns a dictionary representation of the sensor data
        """

        # Shorthand names for brevity here
        # pylint: disable=invalid-name
        a = self.parent
        # pylint: disable=invalid-name
        b = self.child
        out_d = {
            'parent': {
                'meta': {
                    'id': self.identifier,
                    'lat': a.lat,
                    'lon': a.lon,
                    'name': a.name,
                    'location_type': a.location_type
                },
                'data': {
                    'pm_2.5': a.current_pm2_5,
                    'temp_f': a.current_temp_f,
                    'temp_c': a.current_temp_c,
                    'humidity': a.current_humidity,
                    'pressure': a.current_pressure
                },
                'diagnostic': {
                    'last_seen': a.last_seen,
                    'model': a.model,
                    'hidden': a.hidden,
                    'flagged': a.flagged,
                    'downgraded': a.downgraded,
                    'age': a.age
                }
            },
            'child': {
                'meta': {
                    'id': self.identifier,
                    'lat': b.lat if b is not None else None,
                    'lon': b.lon if b is not None else None,
                    'name': b.name if b is not None else None,
                    'location_type': b.location_type if b is not None else None,
                },
                'data': {
                    'pm_2.5': b.current_pm2_5 if b is not None else None,
                    'temp_f': b.current_temp_f if b is not None else None,
                    'temp_c': b.current_temp_c if b is not None else None,
                    'humidity': b.current_humidity if b is not None else None,
                    'pressure': b.current_pressure if b is not None else None,
                },
                'diagnostic': {
                    'last_seen': b.last_seen if b is not None else None,
                    'model': b.model if b is not None else None,
                    'hidden': b.hidden if b is not None else None,
                    'flagged': b.flagged if b is not None else None,
                    'downgraded': b.downgraded if b is not None else None,
                    'age': b.age if b is not None else None
                }
            }
        }

        if 'Stats' in a.channel_data and a.channel_data['Stats']:
            out_d['parent']['statistics'] = {
                '10min_avg': a.m10avg,
                '30min_avg': a.m30avg,
                '1hour_avg': a.h1ravg,
                '6hour_avg': a.h6ravg,
                '1week_avg': a.w1avg
            }
        else:
            out_d['parent']['statistics'] = {
                '10min_avg': None,
                '30min_avg': None,
                '1hour_avg': None,
                '6hour_avg': None,
                '1week_avg': None
            }

        if b and 'Stats' in b.channel_data and b.channel_data['Stats']:
            out_d['child']['statistics'] = {
                '10min_avg': b.m10avg if b is not None else None,
                '30min_avg': b.m30avg if b is not None else None,
                '1hour_avg': b.h1ravg if b is not None else None,
                '6hour_avg': b.h6ravg if b is not None else None,
                '1week_avg': b.w1avg if b is not None else None
            }
        else:
            out_d['child']['statistics'] = {
                '10min_avg': None,
                '30min_avg': None,
                '1hour_avg': None,
                '6hour_avg': None,
                '1week_avg': None
            }

        return out_d

    def as_flat_dict(self, channel: str) -> dict:
        """
        Returns a flat dictionary representation of the Sensor data
        """
        channel_map = {'a': 'parent', 'b': 'child'}
        if channel not in channel_map:
            raise ValueError(f'Invalid sensor channel: {channel}')
        out_d = {}
        src = self.as_dict()
        for data_category in src[channel_map[channel]]:
            for data in src[channel_map[channel]][data_category]:
                out_d[data] = src[channel_map[channel]][data_category][data]
        return out_d

    def __repr__(self):
        """
        String representation of the class
        """
        if self.location:
            return f"Sensor {self.identifier} at {self.location}"
        return f"Sensor {self.identifier}"
