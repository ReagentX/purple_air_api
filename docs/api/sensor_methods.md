# `Sensor()` Methods

## `get_data() -> dict`

If `json_data` is not provided to the constructor, it calls this method to get the metadata for the identified sensor.

## `setup()`

This converts the JSON metadata to Python class members, exposing data in a Pythonic way.

## `get_location()`

Set the location for a Sensor using `geopy`. Sets the `location` property to the result.

## `get_field('field': str)`

Gets the ThingSpeak data from `field` for a sensor. Sets the properties `channel_a` and `channel_b` to the data returned by ThingSpeak.

## `is_useful() -> bool`

Used to determine if a sensor has useful data or not. Not all bad sensors are flagged or downgraded, so this performs additional checks. Useful sensors are guaranteed to have all of the following properties:

* `lat`
* `lon`
* `hidden`
* `flagged`
* `downgraded`
* `current_pm2_5`
* `current_temp_f`
* `current_humidity`
* `current_pressure`
* `last_modified_stats`
* `last2_modified`

## `as_dict() -> dict`

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

## `as_flat_dict() -> dict`

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

## `get_historical(weeks_to_get: int, sensor_channel: str) -> pd.DataFrame`

Get data from the ThingSpeak API from channel `sensor_channel` one week at a time up to `weeks_to_get` weeks in the past.

`sensor_channel` is one of {'a', 'b'}.

* Channel `a` data
  * `'field1': 'PM1 CF=ATM ug/m3'`
  * `'field2': 'PM25 CF=ATM ug/m3'`
  * `'field3': 'PM10 CF=ATM ug/m3'`
  * `'field4': 'Uptime (Minutes)'`
  * `'field5': 'RSSI (WiFi Signal Strength)'`
  * `'field6': 'Temperature (F)'`
  * `'field7': 'Humidity %'`
  * `'field8': 'PM25 CF=1 ug/m3/`
* Channel `b` data
  * `'field1': 'PM1 CF=ATM ug/m3'`
  * `'field2': 'PM25 CF=ATM ug/m3'`
  * `'field3': 'PM10 CF=ATM ug/m3'`
  * `'field4': 'Free HEAP memory'`
  * `'field5': 'ADC0 Voltage'`
  * `'field6': 'Sensor Firmware'`
  * `'field7': 'Unused'`
  * `'field8': 'PM25 CF=1 ug/m3'`
