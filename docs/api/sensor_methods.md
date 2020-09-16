# `Sensor()` Methods

## `get_data() -> dict`

If `json_data` is not provided to the constructor, it calls this method to get the metadata for the identified sensor.

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

## `get_location()`

Set the location for a Sensor using `geopy`. Sets the `location` property to the result.

## `as_dict() -> dict`

Return a dictionary representation of a sensor. The data is shaped like this:

```python
{
    'channel_a': {
        'meta': {
            'id': self.identifier,
            'lat': a.lat,
            'lon': a.lon,
            'name': a.name,
            'location_type': a.location_type
        },
        'data': {
            'pm_2.5': a.current_pm2_5,
            'temp_f': a.current_temp_f,
            'temp_c': a.current_temp_c,
            'humidity': a.current_humidity,
            'pressure': a.current_pressure
        },
        'diagnostic': {
            'last_seen': a.last_seen,
            'model': a.model,
            'hidden': a.hidden,
            'flagged': a.flagged,
            'downgraded': a.downgraded,
            'age': a.age
        }
        'statistics': {
            '10min_avg': a.m10avg,
            '30min_avg': a.m30avg,
            '1hour_avg': a.h1ravg,
            '6hour_avg': a.h6ravg,
            '1week_avg': a.w1avg
        }
    },
    'channel_b':{
        'meta': {
            'id': self.identifier,
            'lat': b.lat,
            'lon': b.lon,
            'name': b.name,
            'location_type': b.location_type,
        },
        'data': {
            'pm_2.5': b.current_pm2_5,
            'temp_f': b.current_temp_f,
            'temp_c': b.current_temp_c,
            'humidity': b.current_humidity,
            'pressure': b.current_pressure,
        },
        'diagnostic': {
            'last_seen': b.last_seen,
            'model': b.model,
            'hidden': b.hidden,
            'flagged': b.flagged,
            'downgraded': b.downgraded,
            'age': b.age
        }
        'statistics': {
            '10min_avg': b.m10avg,
            '30min_avg': b.m30avg,
            '1hour_avg': b.h1ravg,
            '6hour_avg': b.h6ravg,
            '1week_avg': b.w1avg
        }
    }
}
```

## `as_flat_dict(channel: str) -> dict`

Returns a flat dictionary representation of the Sensor data.

`channel` is one of `{'a', 'b'}`.

The data is shaped like this:

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
