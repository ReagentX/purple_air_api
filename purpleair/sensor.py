"""
PurpleAir Sensor Client
"""


import json
import os
from re import sub
from typing import Optional, List

import requests
from geopy.geocoders import Nominatim

from .api_data import API_ROOT
from .channel import Channel


class Sensor():
    """
    Representation of a single PurpleAir sensor
    """

    def __init__(self, identifier: int, json_data: list = None, parse_location=False):
        self.identifier = identifier
        self.data: Optional[list] = json_data \
            if json_data is not None else self.get_data()

        # Validate the data we received
        if not self.data:
            raise ValueError(
                f'Invalid sensor: no configuration found for {identifier}')
        if not isinstance(self.data, list):
            raise ValueError(
                f'Sensor {identifier} created without valid data')

        self.parent_data: dict = self.data[0]
        self.child_data: Optional[dict] = self.data[1] if len(
            self.data) > 1 else None
        self.parse_location: bool = parse_location
        self.thingspeak_data: dict = {}
        self.parent: Channel = Channel(channel_data=self.parent_data,)
        self.child: Optional[Channel] = Channel(
            channel_data=self.child_data) if self.child_data else None
        self.location_type: Optional[str] = self.parent.location_type
        # Parse the location (slow, so must be manually enabled)
        self.location: str = ''
        if self.parse_location:
            self.get_location()

    def get_data(self) -> Optional[list]:
        """
        Get new data if no data is provided
        """
        # Sanitize ID
        if not isinstance(self.identifier, int):
            raise ValueError(f'Invalid sensor ID: {self.identifier}')

        # Fetch the JSON for parent and child sensors
        response = requests.get(f'{API_ROOT}?show={self.identifier}')
        data = json.loads(response.content)
        channel_data: Optional[list] = data.get('results')

        # Handle various API problems
        if channel_data and len(channel_data) == 1:
            print('Child sensor requested, acquiring parent instead.')
            try:
                parent_id = channel_data[0]["ParentID"]
            except IndexError:
                raise IndexError from IndexError(
                    f'Parent sensor for {self.identifier} does not exist!')
            response = requests.get(f'{API_ROOT}?show={parent_id}')
            data = json.loads(response.content)
            channel_data = data.get('results')
        elif channel_data and len(channel_data) > 2:
            print(json.dumps(data, indent=4))
            raise ValueError(
                f'More than 2 channels found for {self.identifier}')
        return channel_data

    def get_field(self, field) -> None:
        """
        Gets the thingspeak data for a sensor, setting None if the data is missing
        """
        self.thingspeak_data[field] = {'primary': {}, 'secondary': {}}

        # Primary
        self.thingspeak_data[field]['primary']['channel_a'] = json.loads(
            self.parent.thingspeak_primary.get_field(field=field)) \
            if self.parent.thingspeak_primary else None
        self.thingspeak_data[field]['primary']['channel_b'] = json.loads(
            self.child.thingspeak_primary.get_field(field=field)) \
            if self.child and self.child.thingspeak_primary else None

        # Secondary
        self.thingspeak_data[field]['secondary']['channel_a'] = json.loads(
            self.parent.thingspeak_secondary.get_field(field=field)) \
            if self.parent.thingspeak_secondary else None
        self.thingspeak_data[field]['secondary']['channel_b'] = json.loads(
            self.child.thingspeak_secondary.get_field(field=field)) \
            if self.child and self.child.thingspeak_secondary else None

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
                'Unable to read current directory name to generate Nominatim user agent!')
            user_agent = f'{root_ua}anonymous_github_com_reagentx_purple_air_api'

        geolocator = Nominatim(user_agent=user_agent)
        location = geolocator.reverse(f'{self.parent.lat}, {self.parent.lon}')
        self.location = str(location)

    def as_dict(self) -> dict:
        """
        Returns a dictionary representation of the sensor data
        """
        return {
            'parent': self.parent.as_dict(),
            'child': self.child.as_dict() if self.child else None,
        }

    def as_list(self) -> List[Optional[dict]]:
        """
        Returns a list representation of the sensor data
        """
        return [
            self.parent.as_dict(),
            self.child.as_dict() if self.child else None
        ]

    def resolve_sensor_channel(self, channel: str) -> Optional[Channel]:
        """
        Resolves a sensor channel string to the respective Channel object
        """
        if channel not in {'parent', 'child'}:
            raise ValueError(
                f'Invalid sensor channel: {channel}. Must be in {{"parent", "child"}}')
        choice: Optional[Channel] = self.parent if channel == 'parent' else self.child
        return choice

    def as_flat_dict(self, channel: str) -> dict:
        """
        Returns a flat dictionary representation of the Sensor data
        """
        choice = self.resolve_sensor_channel(channel)
        if choice is None:
            # There is no data for the specified sensor, so fill with `None`s
            return {key: None for key in self.parent.as_flat_dict()}
        return choice.as_flat_dict()

    def __repr__(self):
        """
        String representation of the class
        """
        if self.location:
            return f"Sensor {self.identifier} at {self.location}"
        return f"Sensor {self.identifier}"
