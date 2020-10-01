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

    def safe_float(self, key: str) -> Optional[float]:
        """
        Convert to float if the item exists, otherwise return none
        """
        result: Optional[float] = self.channel_data.get(key)
        if result is not None:
            try:
                result = float(result)
            except TypeError:
                return None
            except ValueError:
                return None
        return result

    def setup(self) -> None:
        """
        Initialize metadata and real data for a sensor; for detailed info see docs
        """
        # Meta
        self.lat: Optional[float] = self.safe_float('Lat')
        self.lon: Optional[float] = self.safe_float('Lon')
        self.identifier: Optional[int] = self.channel_data.get('ID')
        self.parent: Optional[int] = self.channel_data.get('ParentID')
        self.type: str = 'parent' if self.parent is None else 'child'
        self.name: Optional[str] = self.channel_data.get('Label')
        # pylint: disable=line-too-long
        self.location_type: Optional[str] = self.channel_data.get(
            'DEVICE_LOCATIONTYPE')

        # Data, possible TODO: abstract to class
        self.current_pm2_5: Optional[float] = self.safe_float('PM2_5Value')
        self.current_temp_f: Optional[float] = self.safe_float('temp_f')
        self.current_temp_c = (self.current_temp_f - 32) * (5 / 9) \
            if self.current_temp_f is not None else None
        self.current_humidity: Optional[float] = self.safe_float('humidity')
        self.current_pressure: Optional[float] = self.safe_float('pressure')
        self.current_p_0_3_um: Optional[float] = self.safe_float('p_0_3_um')
        self.current_p_0_5_um: Optional[float] = self.safe_float('p_0_5_um')
        self.current_p_1_0_um: Optional[float] = self.safe_float('p_1_0_um')
        self.current_p_2_5_um: Optional[float] = self.safe_float('p_2_5_um')
        self.current_p_5_0_um: Optional[float] = self.safe_float('p_5_0_um')
        self.current_p_10_0_um: Optional[float] = self.safe_float('p_10_0_um')
        self.current_pm1_0_cf_1: Optional[float] = self.safe_float(
            'pm1_0_cf_1')
        self.current_pm2_5_cf_1: Optional[float] = self.safe_float(
            'pm2_5_cf_1')
        self.current_pm10_0_cf_1: Optional[float] = self.safe_float(
            'pm10_0_cf_1')
        self.current_pm1_0_atm: Optional[float] = self.safe_float('pm1_0_atm')
        self.current_pm2_5_atm: Optional[float] = self.safe_float('pm2_5_atm')
        self.current_pm10_0_atm: Optional[float] = self.safe_float(
            'pm10_0_atm')

        # Statistics
        self.pm2_5stats: Optional[dict] = json.loads(self.channel_data['Stats']) \
            if 'Stats' in self.channel_data else None
        self.m10avg: Optional[float] = self.pm2_5stats.get(
            'v1') if self.pm2_5stats else None
        self.m30avg: Optional[float] = self.pm2_5stats.get(
            'v2') if self.pm2_5stats else None
        self.h1ravg: Optional[float] = self.pm2_5stats.get(
            'v3') if self.pm2_5stats else None
        self.h6ravg: Optional[float] = self.pm2_5stats.get(
            'v4') if self.pm2_5stats else None
        self.d1avg: Optional[float] = self.pm2_5stats.get(
            'v5') if self.pm2_5stats else None
        self.w1avg: Optional[float] = self.pm2_5stats.get(
            'v6') if self.pm2_5stats else None
        self.last_modified_stats: Optional[datetime] = None
        last_mod = self.pm2_5stats.get('lastModified') \
            if self.pm2_5stats is not None else None
        if last_mod is not None:
            self.last_modified_stats = datetime.utcfromtimestamp(
                int(last_mod) / 1000)
        self.last2_modified: Optional[int] = self.pm2_5stats.get(
            'timeSinceModified') if self.pm2_5stats is not None else None

        # ThingSpeak IDs, if these are missing do not crash, just set to None
        try:
            self.tp_primary_channel: Optional[str] = self.channel_data['THINGSPEAK_PRIMARY_ID']
            self.tp_primary_key: Optional[str] = self.channel_data['THINGSPEAK_PRIMARY_ID_READ_KEY']
            self.tp_secondary_channel: Optional[str] = self.channel_data['THINGSPEAK_SECONDARY_ID']
            self.tp_secondary_key: Optional[str] = self.channel_data['THINGSPEAK_SECONDARY_ID_READ_KEY']
            self.thingspeak_primary: Optional[thingspeak.Channel] = thingspeak.Channel(
                id=self.tp_primary_channel, api_key=self.tp_primary_key)
            self.thingspeak_secondary: Optional[thingspeak.Channel] = thingspeak.Channel(
                id=self.tp_secondary_channel, api_key=self.tp_secondary_key)
        except KeyError:
            # Doing this prevents a crash until we actually access ThingSpeak data
            #   which the user may not do
            self.tp_primary_channel = None
            self.tp_primary_key = None
            self.tp_secondary_channel = None
            self.tp_secondary_key = None
            self.thingspeak_primary = None
            self.thingspeak_secondary = None

        # Diagnostic
        last_seen = self.channel_data.get('LastSeen')
        if last_seen is not None:
            self.last_seen: Optional[datetime] = datetime.utcfromtimestamp(
                int(last_seen))
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
        self.brightness: Optional[str] = self.channel_data.get(
            'DEVICE_BRIGHTNESS')
        self.hardware: Optional[str] = self.channel_data.get(
            'DEVICE_HARDWAREDISCOVERED')
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

    def as_dict(self) -> dict:
        """
        Returns a dictionary representation of the channel data
        """
        out_d = {
            'meta': {
                'id': self.identifier,
                'parent': self.parent,
                'lat': self.lat,
                'lon': self.lon,
                'name': self.name,
                'location_type': self.location_type
            },
            'data': {
                'pm_2.5': self.current_pm2_5,
                'temp_f': self.current_temp_f,
                'temp_c': self.current_temp_c,
                'humidity': self.current_humidity,
                'pressure': self.current_pressure,
                'p_0_3_um': self.current_p_0_3_um,
                'p_0_5_um': self.current_p_0_5_um,
                'p_1_0_um': self.current_p_1_0_um,
                'p_2_5_um': self.current_p_2_5_um,
                'p_5_0_um': self.current_p_5_0_um,
                'p_10_0_um': self.current_p_10_0_um,
                'pm1_0_cf_1': self.current_pm1_0_cf_1,
                'pm2_5_cf_1': self.current_pm2_5_cf_1,
                'pm10_0_cf_1': self.current_pm10_0_cf_1,
                'pm1_0_atm': self.current_pm1_0_atm,
                'pm2_5_atm': self.current_pm2_5_atm,
                'pm10_0_atm': self.current_pm10_0_atm
            },
            'diagnostic': {
                'last_seen': self.last_seen,
                'model': self.model,
                'adc': self.adc,
                'rssi': self.rssi,
                'hidden': self.hidden,
                'flagged': self.flagged,
                'downgraded': self.downgraded,
                'age': self.age,
                'brightness': self.brightness,
                'hardware': self.hardware,
                'version': self.version,
                'last_update_check': self.last_update_check,
                'created': self.created,
                'uptime': self.uptime,
                'is_owner': self.is_owner
            },
            'statistics': {
                '10min_avg': self.m10avg,
                '30min_avg': self.m30avg,
                '1hour_avg': self.h1ravg,
                '6hour_avg': self.h6ravg,
                '1day_avg': self.d1avg,
                '1week_avg': self.w1avg
            }
        }

        return out_d

    def as_flat_dict(self) -> dict:
        """
        Returns a flat dictionary representation of channel data
        """
        out_d = {}
        nested = self.as_dict()
        for category in nested:
            for prop in nested[category]:
                out_d[prop] = nested[category][prop]
        return out_d

    def __repr__(self):
        """
        String representation of the class
        """
        child_string = f', child of {self.parent}' if self.parent is not None else ''
        return f"Sensor {self.identifier}{child_string}"
