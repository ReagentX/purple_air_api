# PurpleAir Documentation

There are two main components of this program: `SensorList` and `Sensor`. A `SensorList` instance represents the network or a subset of the network of PurpleAir sensors, while a `Sensor` represents a single sensor.

## SensorList

PurpleAir sensor network representation

### class `SensorList`(parse_location: bool)

`SensorList` parent class. Initialize with `SensorList()`.

To parse location of all sensors from coordinates to addresses, pass `SensorList(parse_location=True)`.

* Members
  * all_sensors
    * All sensors in the PurpleAir network
  * outside_sensors
    * Outdoor sensors in the PurpleAir network
  * useful_sensors
    * Sensors without faults in the PurpleAir network

#### get_all_data()

Automatically run on instantiation. Retrieves the current network data from the PurpleAir API.

#### to_dataframe(sensor_group: str)

Converts dictionary representation of a list of sensors to a Pandas DataFrame where `sensor_group` determines which group of sensors are used.

* useful
  * Sensors with no faults
* outside
  * Outdoor sensors only
* all
  * Do not filter sensors

If `sensor_group` is not in the above set, `to_dataframe()`  will raise a `ValueError`.

## Sensor

Representation of a single PurpleAir sensor

### class Sensor(identifier, json_data: dict, parse_location: bool)

Initialize a new sensor.

`identifier` is the sensor ID from the PurpleAir network.

`json_data` is an optional dict parameter of JSON data representing metadata about the sensor. If we are initializing a sensor without using `SensorList()`, we need this metadata to use the sensor. Since this metadata is returned by the PurpleAir API, sensors created through `SensorList()` do not need to make an additional API call to get sensor data.

`parse_location` is an optional boolean parameter to use `geopy` to parse the rough address of the location of the sensor based on the latitude and longitude from the sensor's metadata.

* Members
  * identifier
    * The sensor's ordinal identification number
  * json
    * metadata in JSON format about the sensor
  * data
    * metadata in Python dictionary format about the sensor
  * thingspeak_data
    * Dictionary of data returned by the ThingSpeak API
  * location
    * Location string if `parse_location` was true, otherwise empty string
  * lat
    * Sensor latitude
  * lon
    * Sensor longitude
  * name
    * Sensor name
  * location_type
    * Sensor location type {'outdoor', 'indoor', ''}
  * current_pm2_5
    * Current pm2.5 value
  * current_temp_f
    * Current temperature in Fahrenheit
  * current_temp_c
    * Current temperature in Celsius
  * current_humidity
    * Current humidity expressed as decimal (i.e., 0.1 = 10%)
  * current_pressure
    * Current atmospheric pressure
  * m10avg
    * Average pm2.5 value for the most recent 10 minutes
  * m30avg
    * Average pm2.5 value for the most recent 30 minutes
  * h1ravg
    * Average pm2.5 value for the most recent 1 hour
  * h6ravg
    * Average pm2.5 value for the most recent 6 hours
  * d1avg
    * Average pm2.5 value for the most recent day
  * w1avg
    * Average pm2.5 value for the most recent week
  * last_modified_stats
    * The date and time at which the stats were last updated
  * last2_modified
    * Milliseconds since last statistics update
  * tp_a
    * ThingSpeak primary identifier
  * tp_a_key
    * ThingSpeak primary read key
  * tp_b
    * ThingSpeak secondary identifier
  * tp_b_key
    * ThingSpeak secondary read key
  * channel_a
    * `thingspeak.Channel` for primary channel
  * channel_b
    * `thingspeak.Channel` for secondary channel
  * last_seen
    * The last time the sensor was online
  * model
    * The model number of the sensor
  * hidden
    * Whether a sensor is hidden from the network
  * flagged
    * Whether a sensor has been flagged for bad data
  * downgraded
    * Whether a sensor has previously been flagged for bad data
  * age
    * Number of minutes old the data returned by the sensor is

#### get_data()

If `json_data` is not provided to the constructor, it calls this method to get the metadata for the identified sensor.

#### setup()

This converts the JSON metadata to python class members, exposing data in a pythonic way.

#### get_location()

Set the location for a Sensor using geopy.

#### get_field('field': str)

Gets the ThingSpeak data from `field` for a sensor.

#### is_useful()

Used to determine if a sensor has useful data or not. Not all bad sensors are flagged or downgraded, so this performs additional checks. Useful sensors are guaranteed to have all of the following properties:

* lat
* lon
* hidden
* flagged
* downgraded
* current_pm2_5
* current_temp_f
* current_humidity
* current_pressure
* last_modified_stats
* last2_modified

#### as_dict()

Return a dictionary representation of a sensor. The data is shaped like this:

```python
{
    'meta': {
        'id': self.identifier,
        'lat': self.lat,
        'lon': self.lon,
        'name': self.name,
        'location_type': self.location_type
        'location': self.location
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
    },
    'statistics': {
        '10min_avg': self.m10avg,
        '30min_avg': self.m30avg,
        '1hour_avg': self.h1ravg,
        '6hour_avg': self.h6ravg,
        '1week_avg': self.w1avg
    }
}
```

#### as_flat_dict()

Returns a flat dictionary representation of the Sensor data. The data is shaped like this:

```python
{
    'id': 14633,
    'lat': 37.275561,
    'lon': -121.964134,
    'name': 'Hazelwood canary',
    'location_type': 'outside',
    'pm_2.5': 92.25,
    'temp_f': 73.0,
    'temp_c': 22.77777777777778,
    'humidity': 0.53,
    'pressure': '1007.15',
    'last_seen': datetime.datetime(2020, 9, 13, 15, 16, 52),
    'model': 'PMS5003+PMS5003+BME280',
    'hidden': False,
    'flagged': False,
    'downgraded': False,
    'age': 0,
    '10min_avg': 93.13,
    '30min_avg': 93.67,
    '1hour_avg': 93.93,
    '6hour_avg': 98.92,
    '1week_avg': 41.49
}
```

#### get_historical(weeks_to_get: int, sensor_channel: str)

Get data from the ThingSpeak API from channel `sensor_channel` one week at a time up to `weeks_to_get` weeks in the past.

`sensor_channel` is one of {'a', 'b'}.

* Channel `a` data
  * 'field1': 'PM1 CF=ATM ug/m3',
  * 'field2': 'PM25 CF=ATM ug/m3',
  * 'field3': 'PM10 CF=ATM ug/m3',
  * 'field4': 'Uptime (Minutes)',
  * 'field5': 'RSSI (WiFi Signal Strength)',
  * 'field6': 'Temperature (F)',
  * 'field7': 'Humidity %',
  * 'field8': 'PM25 CF=1 ug/m3'
* Channel `b` data
  * 'field1': 'PM1 CF=ATM ug/m3',
  * 'field2': 'PM25 CF=ATM ug/m3',
  * 'field3': 'PM10 CF=ATM ug/m3',
  * 'field4': 'Free HEAP memory',
  * 'field5': 'ADC0 Voltage',
  * 'field6': 'Sensor Firmware',
  * 'field7': 'Unused',
  * 'field8': 'PM25 CF=1 ug/m3'
