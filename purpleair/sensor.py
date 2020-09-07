"""
PurpleAir Sensor Client
"""


import json
from typing import Optional
from datetime import datetime, timedelta

import pandas as pd
import requests
import requests_cache
import thingspeak
from geopy.geocoders import Nominatim
from geopy.location import Location

from .api_data import API_ROOT

# Setup cache for requests
requests_cache.install_cache(expire_after=timedelta(hours=1))
requests_cache.core.remove_expired_responses()


class Sensor():
    """
    Class for a single PurpleAir sensor; set initialize=True to fetch data from the API
    """

    def __init__(self, identifier, json_data=None, parse_location=False):
        self.identifier = identifier
        self.json = json_data
        self.data = self.get_data()
        self.parse_location = parse_location
        self.thingspeak_data = {}
        self.location = ''
        self.setup()

    def get_data(self) -> dict:
        """
        Get new data if no data is provided
        """
        # Fetch the JSON and exclude the child sensors
        if not self.json:
            response = requests.get(f'{API_ROOT}?show={self.identifier}')
            data = json.loads(response.content)
            return data['results'][0]
        return self.json

    def setup(self) -> None:
        """
        Initiailze metadata and real data for a sensor; for detailed info see docs
        """
        # Meta
        self.lat = self.data.get('Lat', None)
        self.lon = self.data.get('Lon', None)
        self.identifier = self.data.get('ID', None)
        self.name = self.data.get('Label', None)
        # pylint: disable=line-too-long
        self.location_type = self.data['DEVICE_LOCATIONTYPE'] if 'DEVICE_LOCATIONTYPE' in self.data else ''
        # Parse the location (slow, so must be manually enabled)
        if self.parse_location:
            self.get_location()

        # Data
        if 'PM2_5Value' in self.data:
            if self.data['PM2_5Value'] is not None:
                self.current_pm2_5: Optional[float] = float(self.data['PM2_5Value'])
            else:
                self.current_pm2_5 = self.data['PM2_5Value']
        else:
            self.current_pm2_5 = None
        try:
            f_temp = float(self.data['temp_f'])
            if f_temp > 150 or f_temp < -100:
                self.current_temp_f = None
                self.current_temp_c = None
            else:
                self.current_temp_f = float(self.data['temp_f'])
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
            self.current_humidity: Optional[float]  = int(self.data['humidity']) / 100
        except TypeError:
            self.current_humidity = None
        except ValueError:
            self.current_humidity = None
        except KeyError:
            self.current_humidity = None

        try:
            self.current_pressure: Optional[float] = self.data['pressure']
        except TypeError:
            self.current_pressure = None
        except ValueError:
            self.current_pressure = None
        except KeyError:
            self.current_pressure = None

        # Statistics
        stats = self.data.get('Stats', None)
        if stats:
            self.pm2_5stats = json.loads(self.data['Stats'])
            self.m10avg = self.pm2_5stats['v1']
            self.m30avg = self.pm2_5stats['v2']
            self.h1ravg = self.pm2_5stats['v3']
            self.h6ravg = self.pm2_5stats['v4']
            self.d1avg = self.pm2_5stats['v5']
            self.w1avg = self.pm2_5stats['v6']
            try:
                self.last_modified_stats: Optional[datetime]  = datetime.utcfromtimestamp(
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
        self.tp_a = self.data['THINGSPEAK_PRIMARY_ID']
        self.tp_a_key = self.data['THINGSPEAK_PRIMARY_ID_READ_KEY']
        self.tp_b = self.data['THINGSPEAK_SECONDARY_ID']
        self.tp_b_key = self.data['THINGSPEAK_SECONDARY_ID_READ_KEY']
        self.channel_a = thingspeak.Channel(
            id=self.tp_a, api_key=self.tp_a_key)
        self.channel_b = thingspeak.Channel(
            id=self.tp_b, api_key=self.tp_b_key)

        # Diagnostic
        self.last_seen = datetime.utcfromtimestamp(self.data['LastSeen'])
        self.model = self.data['Type'] if 'Type' in self.data else ''
        # pylint: disable=simplifiable-if-expression
        self.hidden = False if self.data['Hidden'] == 'false' else True
        # pylint: disable=simplifiable-if-expression
        self.flagged = True if 'Flag' in self.data and self.data['Flag'] == 1 else False
        # pylint: disable=simplifiable-if-expression
        self.downgraded = True if 'A_H' in self.data and self.data['A_H'] == 'true' else False
        self.age = int(self.data['AGE'])  # Number of minutes old the data is

    def get_location(self) -> None:
        """
        Set the location for a Sensor using geopy
        """
        geolocator = Nominatim(user_agent="purple_air_api")
        location = geolocator.reverse(f'{self.lat}, {self.lon}')
        self.location = location

    def get_field(self, field) -> None:
        """
        Gets the thingspeak data for a sensor
        """
        self.thingspeak_data[field] = {}
        self.thingspeak_data[field]['channel_a'] = json.loads(
            self.channel_a.get_field(field=field))
        self.thingspeak_data[field]['channel_b'] = json.loads(
            self.channel_b.get_field(field=field))

    def is_useful(self) -> bool:
        """
        Function to dump broken sensors; expanded like this so we can collect metrics later
        """
        if self.lat is None or self.lon is None:
            return False
        if self.hidden:
            return False
        if self.flagged:
            return False
        if self.downgraded:
            return False
        if self.current_pm2_5 is None:
            return False
        if self.current_temp_f is None:
            return False
        if self.current_humidity is None:
            return False
        if self.current_pressure is None:
            return False
        if not self.data.get('Stats', None):
            # Happens before stats because they will be missing if this is missing
            return False
        if self.last_modified_stats is None:
            return False
        if self.last2_modified is None:
            return False
        return True

    def as_dict(self) -> dict:
        """
        Returns a dictionary representation of the sensor data
        """
        out_d = {
            'meta': {
                'id': self.identifier,
                'lat': self.lat,
                'lon': self.lon,
                'name': self.name,
                'locaction_type': self.location_type
            },
            'data': {
                'pm_2.5': self.current_pm2_5,
                'temp_f': self.current_temp_f,
                'temp_c': self.current_temp_c,
                'humidity': self.current_humidity,
                'pressure': self.current_pressure
            },
            'diagnostic': {
                'last_seen': self.last_seen,
                'model': self.model,
                'hidden': self.hidden,
                'flagged': self.flagged,
                'downgraded': self.downgraded,
                'age': self.age
            }
        }

        if 'Stats' in self.data and self.data['Stats']:
            out_d['statistics'] = {
                '10min_avg': self.m10avg,
                '30min_avg': self.m30avg,
                '1hour_avg': self.h1ravg,
                '6hour_avg': self.h6ravg,
                '1week_avg': self.w1avg
            }
        else:
            out_d['statistics'] = {
                '10min_avg': None,
                '30min_avg': None,
                '1hour_avg': None,
                '6hour_avg': None,
                '1week_avg': None
            }

        if self.parse_location:
            out_d['meta']['location'] = self.location

        return out_d

    def as_flat_dict(self) -> dict:
        """
        Returns a flat dictionart representation of the Sensor data
        """
        out_d = {}
        src = self.as_dict()
        for data_category in src:
            for data in src[data_category]:
                out_d[data] = src[data_category][data]
        return out_d

    def get_historical(self, weeks_to_get: int, sensor_channel: str) -> pd.DataFrame:
        """
        Get data from the ThingSpeak API one week at a time up to weeks_to_get weeks in the past
        """
        if sensor_channel not in {'a', 'b'}:
            raise ValueError(f'Invalid sensor channel: {sensor_channel}')
        channel = self.tp_a if sensor_channel == 'a' else self.tp_b
        key = self.tp_a_key if sensor_channel == 'a' else self.tp_b_key
        columns_a = {
            'field1': 'PM1 CF=ATM ug/m3',
            'field2': 'PM25 CF=ATM ug/m3',
            'field3': 'PM10 CF=ATM ug/m3',
            'field4': 'Uptime (Minutes)',
            'field5': 'RSSI (WiFi Signal Strength)',
            'field6': 'Temperature (F)',
            'field7': 'Humidity %',
            'field8': 'PM25 CF=1 ug/m3'
        }
        columns_b = {
            'field1': 'PM1 CF=ATM ug/m3',
            'field2': 'PM25 CF=ATM ug/m3',
            'field3': 'PM10 CF=ATM ug/m3',
            'field4': 'Free HEAP memory',
            'field5': 'ADC0 Voltage',
            'field6': 'Sensor Firmware',
            'field7': 'Unused',
            'field8': 'PM25 CF=1 ug/m3'
        }
        columns = columns_a if sensor_channel == 'a' else columns_b
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
        if self.parse_location:
            return f"Sensor {self.identifier} at {self.location}"
        return f"Sensor {self.identifier}"
