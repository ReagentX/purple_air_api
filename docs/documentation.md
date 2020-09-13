# PurpleAir API Documentation

There are two main components of this program: `SensorList` and `Sensor`. A `SensorList` instance represents the network or a subset of the network of PurpleAir sensors, while a `Sensor` represents a single sensor.

## SensorList

PurpleAir sensor network representation

### `class SensorList(parse_location: bool)`

`SensorList` parent class. Initialize with `SensorList()`.

To parse location of all sensors from coordinates to addresses, pass `SensorList(parse_location=True)`.

* Members
  * `all_sensors`
    * All sensors in the PurpleAir network
  * `outside_sensors`
    * Outdoor sensors in the PurpleAir network
  * `useful_sensors`
    * Sensors without faults in the PurpleAir network

See [api/sensorlist_methods.md](api/sensorlist_methods.md) for method documentation.

## Sensor

Representation of a single PurpleAir sensor

### `class Sensor(identifier, json_data: dict, parse_location: bool)`

Initialize a new sensor.

`identifier` is the sensor ID from the PurpleAir network.

`json_data` is an optional dict parameter of JSON data representing metadata about the sensor. If we are initializing a sensor without using `SensorList()`, we need this metadata to use the sensor. Since this metadata is returned by the PurpleAir API, sensors created through `SensorList()` do not need to make an additional API call to get sensor data.

`parse_location` is an optional boolean parameter to use `geopy` to parse the rough address of the location of the sensor based on the latitude and longitude from the sensor's metadata.

* Members
  * `identifier`
    * The sensor's ordinal identification number
  * `json`
    * metadata in JSON format about the sensor
  * `data`
    * metadata in Python dictionary format about the sensor
  * `thingspeak_data`
    * Dictionary of data returned by the ThingSpeak API
  * `location`
    * Location string if `parse_location` was true, otherwise empty string
  * `lat`
    * Sensor latitude
  * `lon`
    * Sensor longitude
  * `name`
    * Sensor name
  * `location_type`
    * Sensor location type {'outdoor', 'indoor', ''}
  * `current_pm2_5`
    * Current pm2.5 value
  * `current_temp_f`
    * Current temperature in Fahrenheit
  * `current_temp_c`
    * Current temperature in Celsius
  * `current_humidity`
    * Current humidity expressed as decimal (i.e., 0.1 = 10%)
  * `current_pressure`
    * Current atmospheric pressure
  * `m10avg`
    * Average pm2.5 value for the most recent 10 minutes
  * `m30avg`
    * Average pm2.5 value for the most recent 30 minutes
  * `h1ravg`
    * Average pm2.5 value for the most recent 1 hour
  * `h6ravg`
    * Average pm2.5 value for the most recent 6 hours
  * `d1avg`
    * Average pm2.5 value for the most recent day
  * `w1avg`
    * Average pm2.5 value for the most recent week
  * `last_modified_stats`
    * The date and time at which the stats were last updated
  * `last2_modified`
    * Milliseconds since last statistics update
  * `tp_a`
    * ThingSpeak primary identifier
  * `tp_a_key`
    * ThingSpeak primary read key
  * `tp_b`
    * ThingSpeak secondary identifier
  * `tp_b_key`
    * ThingSpeak secondary read key
  * `channel_a`
    * `thingspeak.Channel` for primary channel
  * `channel_b`
    * `thingspeak.Channel` for secondary channel
  * `last_seen`
    * The last time the sensor was online
  * `model`
    * The model number of the sensor
  * `hidden`
    * Whether a sensor is hidden from the network
  * `flagged`
    * Whether a sensor has been flagged for bad data
  * `downgraded`
    * Whether a sensor has previously been flagged for bad data
  * `age`
    * Number of minutes old the data returned by the sensor is

See [api/sensor_methods.md](api/sensor_methods.md) for method documentation.
