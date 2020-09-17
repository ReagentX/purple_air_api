"""
Representation of sensor channel data
"""

import json
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
import thingspeak

from .api_data import (CHANNEL_A_PRIMARY_COLS, CHANNEL_A_SECONDARY_COLS,
                       CHANNEL_B_PRIMARY_COLS, CHANNEL_B_SECONDARY_COLS)


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
        self.lat = self.channel_data.get('Lat', None)
        self.lon = self.channel_data.get('Lon', None)
        self.identifier = self.channel_data.get('ID', None)
        self.parent = self.channel_data.get('ParentID', None)
        self.channel = 'a' if self.parent is None else 'b'
        self.name = self.channel_data.get('Label', None)
        # pylint: disable=line-too-long
        self.location_type = self.channel_data['DEVICE_LOCATIONTYPE'] if 'DEVICE_LOCATIONTYPE' in self.channel_data else ''

        # Data
        if 'PM2_5Value' in self.channel_data:
            if self.channel_data['PM2_5Value'] is not None:
                self.current_pm2_5: Optional[float] = float(
                    self.channel_data['PM2_5Value'])
            else:
                self.current_pm2_5 = self.channel_data['PM2_5Value']
        else:
            self.current_pm2_5 = None
        try:
            f_temp = float(self.channel_data['temp_f'])
            if f_temp > 150 or f_temp < -100:
                self.current_temp_f = None
                self.current_temp_c = None
            else:
                self.current_temp_f = float(self.channel_data['temp_f'])
                self.current_temp_c = (self.current_temp_f - 32) * (5 / 9)
        except TypeError:
            self.current_temp_f = None
            self.current_temp_c = None
        except ValueError:
            self.current_temp_f = None
            self.current_temp_c = None
        except KeyError:
            self.current_temp_f = None
            self.current_temp_c = None

        try:
            self.current_humidity: Optional[float] = int(
                self.channel_data['humidity']) / 100
        except TypeError:
            self.current_humidity = None
        except ValueError:
            self.current_humidity = None
        except KeyError:
            self.current_humidity = None

        try:
            self.current_pressure: Optional[float] = self.channel_data['pressure']
        except TypeError:
            self.current_pressure = None
        except ValueError:
            self.current_pressure = None
        except KeyError:
            self.current_pressure = None

        # Statistics
        stats = self.channel_data.get('Stats', None)
        if stats:
            self.pm2_5stats = json.loads(self.channel_data['Stats'])
            self.m10avg = self.pm2_5stats['v1']
            self.m30avg = self.pm2_5stats['v2']
            self.h1ravg = self.pm2_5stats['v3']
            self.h6ravg = self.pm2_5stats['v4']
            self.d1avg = self.pm2_5stats['v5']
            self.w1avg = self.pm2_5stats['v6']
            try:
                self.last_modified_stats: Optional[datetime] = datetime.utcfromtimestamp(
                    int(self.pm2_5stats['lastModified']) / 1000)
            except TypeError:
                self.last_modified_stats = None
            except ValueError:
                self.last_modified_stats = None
            except KeyError:
                self.last_modified_stats = None

            try:
                # MS since last update to stats
                self.last2_modified = self.pm2_5stats['timeSinceModified']
            except KeyError:
                self.last2_modified = None

        # Thingspeak IDs
        self.tp_primary_channel = self.channel_data['THINGSPEAK_PRIMARY_ID']
        self.tp_primary_key = self.channel_data['THINGSPEAK_PRIMARY_ID_READ_KEY']
        self.tp_secondary_channel = self.channel_data['THINGSPEAK_SECONDARY_ID']
        self.tp_secondary_key = self.channel_data['THINGSPEAK_SECONDARY_ID_READ_KEY']
        self.thingspeak_primary = thingspeak.Channel(
            id=self.tp_primary_channel, api_key=self.tp_primary_key)
        self.thingspeak_secondary = thingspeak.Channel(
            id=self.tp_secondary_channel, api_key=self.tp_secondary_key)

        # Diagnostic
        self.last_seen = datetime.utcfromtimestamp(
            self.channel_data['LastSeen'])
        self.model = self.channel_data['Type'] if 'Type' in self.channel_data else ''
        # pylint: disable=simplifiable-if-expression
        self.hidden = False if self.channel_data['Hidden'] == 'false' else True
        # pylint: disable=simplifiable-if-expression
        self.flagged = True if 'Flag' in self.channel_data and self.channel_data[
            'Flag'] == 1 else False
        # pylint: disable=simplifiable-if-expression
        self.downgraded = True if 'A_H' in self.channel_data and self.channel_data[
            'A_H'] == 'true' else False
        # Number of minutes old the data is
        self.age = int(self.channel_data['AGE'])

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
        channel = self.tp_primary_channel if thingspeak_field == 'primary' else self.tp_secondary_channel
        key = self.tp_primary_key if thingspeak_field == 'primary' else self.tp_secondary_key

        # Determine column columns
        # pylint: disable=line-too-long
        columns_a = CHANNEL_A_PRIMARY_COLS if thingspeak_field == 'primary' else CHANNEL_A_SECONDARY_COLS
        # pylint: disable=line-too-long
        columns_b = CHANNEL_B_PRIMARY_COLS if thingspeak_field == 'primary' else CHANNEL_B_SECONDARY_COLS

        columns = columns_a if self.channel == 'a' else columns_b
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
