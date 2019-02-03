import json
import thingspeak
import requests
import requests_cache
from datetime import timedelta
from datetime import datetime
from .api_data import API_ROOT
from geopy.geocoders import Nominatim
from geopy.location import Location

# Setup cache for requests
requests_cache.install_cache(expire_after=timedelta(hours=24))


class Sensor():
    '''Class for a single PurpleAir sensor; set initialize=True to fetch data from the API'''
    def __init__(self, id, json=None, parse_location=False):
        self.id = id
        self.json = json
        self.data = self.get_data()
        self.parse_location = parse_location
        self.thingspeak_data = {}
        self.setup()


    def get_data(self) -> dict:
        '''Get new data if no data is provided'''
        # Fetch the JSON and exclude the child sensors
        if not self.json:
            response = requests.get(f'{API_ROOT}?show={self.id}')
            data = json.loads(response.content)
            return data['results'][0]
        else:
            return self.json


    def setup(self) -> None:
        '''Initiailze metadata and real data for a sensor; for detailed info see docs'''
        # Meta
        self.lat = self.data['Lat']
        self.lon = self.data['Lon']
        self.parent = self.data['ParentID']
        self.name = self.data['Label']
        self.location_type = self.data['DEVICE_LOCATIONTYPE']
        # Parse the location (slow, so must be manually enabled)
        if self.parse_location:
            self.get_location()

        # Data
        self.current_pm2_5 = self.data['PM2_5Value']
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

        try: 
            self.current_humidity = int(self.data['humidity']) / 100
        except TypeError:
            self.current_humidity = None
        except ValueError:
            self.current_humidity = None

        try:
            self.current_pressure = self.data['pressure']
        except TypeError:
            self.current_pressure = None
        except ValueError:
            self.current_pressure = None

        # Statistics
        stats = self.data['Stats']
        if stats:
            self.pm2_5stats = json.loads(self.data['Stats'])
            self.m10avg = self.pm2_5stats['v1']
            self.m30avg = self.pm2_5stats['v2']
            self.h1ravg = self.pm2_5stats['v3']
            self.h6ravg = self.pm2_5stats['v4']
            self.d1avg = self.pm2_5stats['v5']
            self.w1avg = self.pm2_5stats['v6']
            try:
                self.last_modified_stats = datetime.utcfromtimestamp(int(self.pm2_5stats['lastModified']) / 1000)
            except TypeError:
                self.last_modified_stats = None
            except ValueError:
                self.last_modified_stats = None
            except KeyError:
                self.last_modified_stats = None

            try:
                self.last2_modified = self.pm2_5stats['timeSinceModified'] # MS since last update to stats
            except KeyError:
                self.last2_modified = None

        # Thingspeak IDs
        self.tp_a = self.data['THINGSPEAK_PRIMARY_ID']
        self.tp_a_key = self.data['THINGSPEAK_PRIMARY_ID_READ_KEY']
        self.tp_b = self.data['THINGSPEAK_SECONDARY_ID']
        self.tp_b_key = self.data['THINGSPEAK_SECONDARY_ID_READ_KEY']
        self.channel_a = thingspeak.Channel(id=self.tp_a, api_key=self.tp_a_key)
        self.channel_b =thingspeak.Channel(id=self.tp_b, api_key=self.tp_b_key)

        # Diagnostic
        self.last_seen = datetime.utcfromtimestamp(self.data['LastSeen'])
        self.model = self.data['Type']
        self.hidden = False if self.data['Hidden'] == 'false' else True
        self.flagged = True if self.data['Flag'] == 1 else False
        self.downgraded = True if self.data['A_H'] == 'true' else False
        self.age = int(self.data['AGE']) # Number of minutes old the data is


    def get_location(self) -> Location:
        '''Set the location for a Sensor using geopy'''
        geolocator = Nominatim(user_agent="purple_air_api")
        location = geolocator.reverse(f'{self.lat}, {self.lon}')
        self.location = location
        return location


    def get_field(self, field) -> None:
        '''Gets the thingspeak data for a sensor'''
        self.thingspeak_data[field] = {}
        self.thingspeak_data[field]['channel_a'] = json.loads(self.channel_a.get_field(field=field))
        self.thingspeak_data[field]['channel_b'] = json.loads(self.channel_b.get_field(field=field))


    def is_useful(self) -> bool:
        '''Function to dump broken sensors; expanded like this so we can collect metrics later'''
        if self.hidden:
            return False
        elif self.flagged:
            return False
        elif self.downgraded:
            return False
        elif self.current_temp_f == None:
            return False
        elif self.current_humidity == None:
            return False
        elif self.current_pressure == None:
            return False
        elif not self.data['Stats']:
            # Happens before stats because they will be missing if this is missing
            return False
        elif self.last_modified_stats == None:
            return False
        elif self.last2_modified == None:
            return False
        return True


    def as_dict(self) -> dict:
        '''Returns a dictionary representation of the sensor data'''
        d = {
            'meta': {
                'id': self.id,
                'lat': self.lat,
                'lon': self.lon,
                'parent': self.parent,
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
            'statistics': {
                '10min_avg': self.m10avg,
                '30min_avg': self.m30avg,
                '1hour_avg': self.h1ravg,
                '6hour_avg': self.h6ravg,
                '1week_avg': self.w1avg
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

        if self.parse_location:
            d['meta']['location'] = self.location

        return d


    def as_flat_dict(self) -> dict:
        '''Returns a flat dictionart representation of the Sensor data'''
        d = {}
        src = self.as_dict()
        for data_category in src:
            for data in src[data_category]:
                d[data] = src[data_category][data]
        return d


    def __repr__(self):
        '''String representation of the class'''
        try:
            return f"Sensor {self.id} at {self.location}"
        except AttributeError:
            return f"Sensor {self.id}"
