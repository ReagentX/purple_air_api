"""
Representation of sensor channel data
"""

import json
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
import thingspeak

from .api_data import (PARENT_PRIMARY_COLS, PARENT_SECONDARY_COLS,
                       CHILD_PRIMARY_COLS, CHILD_SECONDARY_COLS)


class Channel():
    """
    Representation of sensor channel data
    """

    def __init__(self, channel_data: dict):
        self.channel_data = channel_data
        self.setup()

    def setup(self) -> None:
        """
        Initialize metadata and real data for a sensor; for detailed info see docs
        """
        # Meta
        self.lat: Optional[float] = self.channel_data.get('Lat')
        self.lon: Optional[float] = self.channel_data.get('Lon')
        self.identifier: Optional[int] = self.channel_data.get('ID')
        self.parent: Optional[int] = self.channel_data.get('ParentID')
        self.type: str = 'parent' if self.parent is None else 'child'
        self.name: Optional[str] = self.channel_data.get('Label')
        # pylint: disable=line-too-long
        self.location_type: Optional[str] = self.channel_data.get(
            'DEVICE_LOCATIONTYPE')

        # Data
        # Current pm2.5
        self.current_pm2_5: Optional[float] = self.channel_data.get('PM2_5Value')
        if self.current_pm2_5 is not None:
            self.current_pm2_5 = float(self.current_pm2_5)

        # Current temperature
        self.current_temp_f: Optional[float] = self.channel_data.get('temp_f')
        self.current_temp_c: Optional[float] = self.current_temp_f
        if self.current_temp_f is not None:
            self.current_temp_f = float(self.current_temp_f)
            self.current_temp_c = (self.current_temp_f - 32) * (5 / 9)

        # Humidity
        self.current_humidity: Optional[float] = self.channel_data.get('humidity')
        if self.current_humidity is not None:
            self.current_humidity = float(self.current_humidity)

        # Pressure
        self.current_pressure: Optional[float] = self.channel_data.get('pressure')
        if self.current_pressure is not None:
            self.current_pressure = float(self.current_pressure)

        # Statistics
        stats = self.channel_data.get('Stats', None)
        if stats:
            self.pm2_5stats: dict = json.loads(self.channel_data['Stats'])
            self.m10avg: Optional[float] = self.pm2_5stats.get('v1')
            self.m30avg: Optional[float] = self.pm2_5stats.get('v2')
            self.h1ravg: Optional[float] = self.pm2_5stats.get('v3')
            self.h6ravg: Optional[float] = self.pm2_5stats.get('v4')
            self.d1avg: Optional[float] = self.pm2_5stats.get('v5')
            self.w1avg: Optional[float] = self.pm2_5stats.get('v6')
            last_mod = self.pm2_5stats.get('lastModified')
            if last_mod is not None:
                self.last_modified_stats: Optional[datetime] = datetime.utcfromtimestamp(
                    int(last_mod) / 1000)
            self.last2_modified: Optional[int] = self.pm2_5stats.get(
                'timeSinceModified')

        # Thingspeak IDs
        self.tp_primary_channel: str = self.channel_data['THINGSPEAK_PRIMARY_ID']
        self.tp_primary_key: str = self.channel_data['THINGSPEAK_PRIMARY_ID_READ_KEY']
        self.tp_secondary_channel: str = self.channel_data['THINGSPEAK_SECONDARY_ID']
        self.tp_secondary_key: str = self.channel_data['THINGSPEAK_SECONDARY_ID_READ_KEY']
        self.thingspeak_primary: thingspeak.Channel = thingspeak.Channel(
            id=self.tp_primary_channel, api_key=self.tp_primary_key)
        self.thingspeak_secondary: thingspeak.Channel = thingspeak.Channel(
            id=self.tp_secondary_channel, api_key=self.tp_secondary_key)

        # Diagnostic
        last_seen = self.channel_data.get('LastSeen')
        if last_seen is not None:
            self.last_seen: Optional[datetime] = datetime.utcfromtimestamp(
                int(last_seen) / 1000)
        else:
            self.last_seen = last_seen
        self.model: Optional[str] = self.channel_data.get('Type')
        self.adc: Optional[str] = self.channel_data.get('Adc')
        self.rssi: Optional[str] = self.channel_data.get('RSSI')
        # pylint: disable=simplifiable-if-expression
        self.hidden = False if self.channel_data.get(
            'Hidden') == 'false' else True
        # pylint: disable=simplifiable-if-expression
        self.flagged = True if self.channel_data.get('Flag') == 1 else False
        # pylint: disable=simplifiable-if-expression
        self.downgraded = True if self.channel_data.get(
            'A_H') == 'true' else False
        # Number of minutes old the data is
        self.age: Optional[int] = self.channel_data.get('AGE')
        self.brightness: Optional[str] = self.channel_data.get('DEVICE_BRIGHTNESS')
        self.hardware: Optional[str] = self.channel_data.get('DEVICE_HARDWAREDISCOVERED')
        self.version: Optional[str] = self.channel_data.get('Version')
        self.last_update_check: Optional[int] = self.channel_data.get(
            'LastUpdateCheck')
        self.created: Optional[int] = self.channel_data.get('Created')
        self.uptime: Optional[int] = self.channel_data.get('Uptime')
        self.is_owner: Optional[bool] = bool(self.channel_data.get('isOwner'))

    def get_historical(self,
                       weeks_to_get: int,
                       thingspeak_field: str) -> pd.DataFrame:
        """
        Get data from the ThingSpeak API one week at a time up to weeks_to_get weeks in the past
        """
        if thingspeak_field not in {'primary', 'secondary'}:
            # pylint: disable=line-too-long
            raise ValueError(
                f'Invalid ThingSpeak key: {thingspeak_field}. Must be in {{"primary", "secondary"}}')

        # Determine channel and key
        # pylint: disable=line-too-long
        channel = self.tp_primary_channel if thingspeak_field == 'primary' else self.tp_secondary_channel
        key = self.tp_primary_key if thingspeak_field == 'primary' else self.tp_secondary_key

        # Determine column columns
        # pylint: disable=line-too-long
        parent_cols = PARENT_PRIMARY_COLS if thingspeak_field == 'primary' else PARENT_SECONDARY_COLS
        # pylint: disable=line-too-long
        child_cols = CHILD_PRIMARY_COLS if thingspeak_field == 'primary' else CHILD_SECONDARY_COLS

        columns = parent_cols if self.type == 'parent' else child_cols
        from_week = datetime.now()
        to_week = from_week - timedelta(weeks=1)
        # pylint: disable=line-too-long
        url = f'https://thingspeak.com/channels/{channel}/feed.csv?api_key={key}&offset=0&average=&round=2&start={to_week.strftime("%Y-%m-%d")}%2000:00:00&end={from_week.strftime("%Y-%m-%d")}%2000:00:00'
        weekly_data = pd.read_csv(url)
        if weeks_to_get > 1:
            for _ in range(weeks_to_get):
                from_week = to_week  # DateTimes are immutable so this reference is not a problem
                to_week = to_week - timedelta(weeks=1)
                # pylint: disable=line-too-long
                url = f'https://thingspeak.com/channels/{channel}/feed.csv?api_key={key}&offset=0&average=&round=2&start={to_week.strftime("%Y-%m-%d")}%2000:00:00&end={from_week.strftime("%Y-%m-%d")}%2000:00:00'
                weekly_data = pd.concat([weekly_data, pd.read_csv(url)])

        # Handle formatting the DataFrame
        weekly_data.rename(columns=columns, inplace=True)
        weekly_data['created_at'] = pd.to_datetime(
            weekly_data['created_at'], format='%Y-%m-%d %H:%M:%S %Z')
        weekly_data.index = weekly_data.pop('entry_id')
        return weekly_data

    def __repr__(self):
        """
        String representation of the class
        """
        child_string = f', child of {self.parent}' if self.parent is not None else ''
        return f"Sensor {self.identifier}{child_string}"
