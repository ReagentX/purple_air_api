import json
import requests
import requests_cache
from datetime import timedelta
from datetime import datetime
from api_data import API_ROOT
from geopy.geocoders import Nominatim


# Setup cache for requests
requests_cache.install_cache(expire_after=timedelta(hours=24))


class Sensor():
    """Class for a single PurpleAir sensor; set initialize=True to fetch data from the API"""
    def __init__(self, id, json=None, parse_location=False):
        self.id = id
        self.json = json
        self.data = self.get_data()
        self.parse_location = parse_location  # Disables some slow features
        self.setup()


    def get_data(self):
        # Fetch the JSON and exclude the child sensors
        if not self.json:
            response = requests.get(f'{API_ROOT}?show={self.id}')
            data = json.loads(response.content)
            return data['results'][0]
        else:
            return self.json


    def setup(self):
        """Initiailze metadata and real data for a sensor; for detailed info see docs"""
        # Meta
        self.lat = self.data['Lat']
        self.lon = self.data['Lon']
        self.parent = self.data['ParentID']
        self.name = self.data['Label']
        self.location_type = self.data['DEVICE_LOCATIONTYPE']
        # Parse the location (slow, so must be manually enabled)
        if not self.parse_location:
            self.get_location()

        # Data
        self.current_pm2_5 = self.data['PM2_5Value']
        try:
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
                self.last_modified = self.pm2_5stats['timeSinceModified'] # MS since last update to stats
            except KeyError:
                self.last_modified = None

        # Diagnostic
        self.last_seen = datetime.utcfromtimestamp(self.data['LastSeen'])
        self.model = self.data['Type']
        self.hidden = False if self.data['Hidden'] == 'false' else True
        self.flagged = True if self.data['Flag'] != 'null' else False
        self.downgraded = True if self.data['A_H'] != 'null' else False
        self.age = int(self.data['AGE']) # Number of minutes old the data is


    def get_location(self):
        """Set the location for a Sensor using geopy"""
        geolocator = Nominatim(user_agent="purple_air_api")
        location = geolocator.reverse(f'{self.lat}, {self.lon}')
        self.location = location
        return location


    def __repr__(self):
        try:
            return f"Sensor {self.id} at {self.location}"
        except AttributeError:
            return f"Sensor {self.id}"