# PurpleAir API Documentation

There are two main components of this program: `SensorList` and `Sensor`. A `SensorList` instance represents the network or a subset of the network of PurpleAir sensors, while a `Sensor` represents a single sensor.

`Sensor`s have up to two channels, a `parent` and an optional `child`, that hold data the sensor generates.

## SensorList

PurpleAir sensor network representation

### `class SensorList(parse_location: bool)`

`SensorList` parent class. Initialize with `SensorList()`.

To parse location of all sensors from coordinates to addresses, pass `SensorList(parse_location=True)`.

* Properties
  * `all_sensors`
    * All sensors in the PurpleAir network

See [api/sensorlist_methods.md](api/sensorlist_methods.md) for method documentation.

## Sensor

Representation of a single PurpleAir sensor

### `class Sensor(identifier: int, json_data: dict, parse_location: bool)`

Initialize a new sensor.

`identifier` is the sensor ID number from the PurpleAir network.

`json_data` is an optional dict parameter of JSON data representing metadata about the sensor. If we are initializing a sensor without using `SensorList()`, we need this metadata to use the sensor. Since this metadata is returned by the PurpleAir API, sensors created through `SensorList()` do not need to make an additional API call to get sensor data.

`parse_location` is an optional boolean parameter to use `geopy` to parse the rough address of the location of the sensor based on the latitude and longitude from the sensor's metadata.

* Properties
  * `identifier`
    * Sensor ID Number
  * `data`
    * JSON blob of parent and child sensor data where the 0th index is the parent and the 1st index is the optional child
  * `parent_data`
    * Reference to parent JSON data
  * `child_data`
    * Reference to child JSON data
  * `parse_location`
    * `True` if we want to parse the location of the sensor, default `False`
  * `thingspeak_data`
    * Empty dictionary that we optionally populate with [`get_field()`](api/sensor_methods.md#get_fieldfield-str)
  * `parent`
    * [Channel](#channel) instance for parent data
  * `child`
    * [Channel](#channel) instance for child data
    * Not all parent data is available from the child sensor
  * `location_type`
    * The location type of the sensor, one of `{'indoor', 'outdoor', 'unknown'}`
  * `location`
    * Location string if `parse_location` was true, otherwise empty string

See [api/sensor_methods.md](api/sensor_methods.md) for method documentation.

## Channel

Representation of a sensor channel, either `a` or `b`. For channel `b` (child) some of the data may be missing.

### `class Channel(channel_data: dict)`

* Properties
  * `channel_data`
    * metadata in Python dictionary format about the channel
  * `lat`
    * Sensor latitude
  * `lon`
    * Sensor longitude
  * `identifier`
    * The unique integer identifier of the sensor in the network
  * `type`
    * Whether the channel is for the parent or the child sensor
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
  * `p_0_3_um`
    * Current pm0.3 / um
  * `p_0_5_um`
    * Current pm0.5 / um
  * `p_1_0_um`
    * Current pm1.0 / um
  * `p_2_5_um`
    * Current pm2.5 / um
  * `p_5_0_um`
    * Current pm5.0 / um
  * `p_10_0_um`
    * Current pm10.0 / um
  * `pm1_0_cf_1`
    * Current pm1.0 / um secondary reading
  * `pm2_5_cf_1`
    * Current pm2.5 / um secondary reading
  * `pm10_0_cf_1`
    * Current pm10.0 / um secondary reading
  * `pm1_0_atm`
    * Current pm1.0 / atm
  * `pm2_5_atm`
    * Current pm2.5 / atm
  * `pm10_0_atm`
    * Current pm10.0 / atm
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
  * `brightness`
    * Ambient brightness
  * `hardware`
    * Hardware model IDs
  * `version`
    * Software version
  * `last_update_check`
    * Last software update check
  * `created`
    * Date first seen
  * `uptime`
    * Time since boot in seconds
  * `is_owner`
    * Unknown

See [api/channel_methods.md](api/channel_methods.md) for method documentation.
