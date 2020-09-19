# `Sensor()` Methods

## `get_data() -> dict`

If `json_data` is not provided to the constructor, it calls this method to get the metadata for the identified sensor. 

The JSON data contains a `results` array where the 0th index is the parent sensor and the 1st index is an optional child sensor. The data looks like this:

```json
{
    "mapVersion": "0.19",
    "baseVersion": "7",
    "mapVersionString": "",
    "results": [
        {
            "ID": 2892,
            "Label": "Imola - 1",
            "DEVICE_LOCATIONTYPE": "outside",
            "THINGSPEAK_PRIMARY_ID": "317405",
            "THINGSPEAK_PRIMARY_ID_READ_KEY": "50UQJX9NR475QBWH",
            "THINGSPEAK_SECONDARY_ID": "317406",
            "THINGSPEAK_SECONDARY_ID_READ_KEY": "SOE9YW475VW6WZLA",
            "Lat": 38.280572,
            "Lon": -122.273712,
            "PM2_5Value": "5.69",
            "LastSeen": 1571048794,
            "Type": "PMS5003+PMS5003+BME280",
            "Hidden": "false",
            "DEVICE_BRIGHTNESS": "15",
            "DEVICE_HARDWAREDISCOVERED": "2.0+BME280+PMSX003-B+PMSX003-A",
            "Version": "4.10",
            "LastUpdateCheck": 1571047712,
            "Created": 1502745962,
            "Uptime": "3511208",
            "RSSI": "-79",
            "Adc": "0.0",
            "p_0_3_um": "728.19",
            "p_0_5_um": "200.53",
            "p_1_0_um": "26.16",
            "p_2_5_um": "2.89",
            "p_5_0_um": "0.6",
            "p_10_0_um": "0.0",
            "pm1_0_cf_1": "3.99",
            "pm2_5_cf_1": "5.69",
            "pm10_0_cf_1": "6.69",
            "pm1_0_atm": "3.99",
            "pm2_5_atm": "5.69",
            "pm10_0_atm": "6.69",
            "isOwner": 0,
            "humidity": "54",
            "temp_f": "55",
            "pressure": "1008.76",
            "AGE": 487182,
            "Stats": "{...truncated...}"
        },
        {
            "ID": 2893,
            "ParentID": 2892,
            "Label": "Imola - 1 B",
            "THINGSPEAK_PRIMARY_ID": "317407",
            "THINGSPEAK_PRIMARY_ID_READ_KEY": "V0FJ8SKLX6BOLB26",
            "THINGSPEAK_SECONDARY_ID": "317408",
            "THINGSPEAK_SECONDARY_ID_READ_KEY": "AYUATIO1HW0BIWR5",
            "PM2_5Value": "5.96",
            "LastSeen": 1571048794,
            "Hidden": "false",
            "Created": 1502745962,
            "Adc": "0.01",
            "p_0_3_um": "901.52",
            "p_0_5_um": "263.74",
            "p_1_0_um": "36.33",
            "p_2_5_um": "0.91",
            "p_5_0_um": "0.2",
            "p_10_0_um": "0.0",
            "pm1_0_cf_1": "4.39",
            "pm2_5_cf_1": "5.96",
            "pm10_0_cf_1": "6.01",
            "pm1_0_atm": "4.39",
            "pm2_5_atm": "5.96",
            "pm10_0_atm": "6.01",
            "isOwner": 0,
            "AGE": 487182,
            "Stats": "{...truncated...}"
        }
    ]
}
```

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
    'parent': {
        'meta': {
            'id': a.identifier,
            'parent': None,
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
            'pressure': a.current_pressure,
            'p_0_3_um': a.current_p_0_3_um,
            'p_0_5_um': a.current_p_0_5_um,
            'p_1_0_um': a.current_p_1_0_um,
            'p_2_5_um': a.current_p_2_5_um,
            'p_5_0_um': a.current_p_5_0_um,
            'p_10_0_um': a.current_p_10_0_um,
            'pm1_0_cf_1': a.current_pm1_0_cf_1,
            'pm2_5_cf_1': a.current_pm2_5_cf_1,
            'pm10_0_cf_1': a.current_pm10_0_cf_1,
            'pm1_0_atm': a.current_pm1_0_atm,
            'pm2_5_atm': a.current_pm2_5_atm,
            'pm10_0_atm': a.current_pm10_0_atm
        },
        'diagnostic': {
            'last_seen': a.last_seen,
            'model': a.model,
            'hidden': a.hidden,
            'flagged': a.flagged,
            'downgraded': a.downgraded,
            'age': a.age,
            'brightness': a.brightness,
            'hardware': a.hardware,
            'version': a.version,
            'last_update_check': a.last_update_check,
            'created': a.created,
            'uptime': a.uptime,
            'is_owner': a.is_owner
        },
        'statistics': {
            '10min_avg': a.m10avg,
            '30min_avg': a.m30avg,
            '1hour_avg': a.h1ravg,
            '6hour_avg': a.h6ravg,
            '1day_avg': a.d1avg,
            '1week_avg': a.w1avg
        }
    },
    'child':{
        'meta': {
            'id': b.identifier,
            'parent': a.identifier,
            'lat': b.lat,
            'lon': b.lon,
            'name': b.name,
            'location_type': b.location_type
        },
        'data': {
            'pm_2.5': b.current_pm2_5,
            'temp_f': b.current_temp_f,
            'temp_c': b.current_temp_c,
            'humidity': b.current_humidity,
            'pressure': b.current_pressure,
            'p_0_3_um': b.current_p_0_3_um,
            'p_0_5_um': b.current_p_0_5_um,
            'p_1_0_um': b.current_p_1_0_um,
            'p_2_5_um': b.current_p_2_5_um,
            'p_5_0_um': b.current_p_5_0_um,
            'p_10_0_um': b.current_p_10_0_um,
            'pm1_0_cf_1': b.current_pm1_0_cf_1,
            'pm2_5_cf_1': b.current_pm2_5_cf_1,
            'pm10_0_cf_1': b.current_pm10_0_cf_1,
            'pm1_0_atm': b.current_pm1_0_atm,
            'pm2_5_atm': b.current_pm2_5_atm,
            'pm10_0_atm': b.current_pm10_0_atm
        },
        'diagnostic': {
            'last_seen': b.last_seen,
            'model': b.model,
            'adc': b.adc,
            'rssi': b.rssi,
            'hidden': b.hidden,
            'flagged': b.flagged,
            'downgraded': b.downgraded,
            'age': b.age,
            'brightness': b.brightness,
            'hardware': b.hardware,
            'version': b.version,
            'last_update_check': b.last_update_check,
            'created': b.created,
            'uptime': b.uptime,
            'is_owner': b.is_owner
        },
        'statistics': {
            '10min_avg': b.m10avg,
            '30min_avg': b.m30avg,
            '1hour_avg': b.h1ravg,
            '6hour_avg': b.h6ravg,
            '1day_avg': b.d1avg,
            '1week_avg': b.w1avg
        }
    }
}
```

## `as_flat_dict(channel: str) -> dict`

Returns a flat dictionary representation of the Sensor data.

`channel` is one of `{'parent', 'child'}`.

The data is shaped like this:

```python
{
    'parent': 0,
    'lat': 0,
    'lon': 0,
    'name': 0,
    'location_type': 0,
    'pm_2.5': 0,
    'temp_f': 0,
    'temp_c': 0,
    'humidity': 0,
    'pressure': 0,
    'p_0_3_um': 0,
    'p_0_5_um': 0,
    'p_1_0_um': 0,
    'p_2_5_um': 0,
    'p_5_0_um': 0,
    'p_10_0_um': 0,
    'pm1_0_cf_1': 0,
    'pm2_5_cf_1': 0,
    'pm10_0_cf_1': 0,
    'pm1_0_atm': 0,
    'pm2_5_atm': 0,
    'pm10_0_atm': 0,
    'last_seen': 0,
    'model': 0,
    'adc': 0,
    'rssi': 0,
    'hidden': 0,
    'flagged': 0,
    'downgraded': 0,
    'age': 0,
    'brightness': 0,
    'hardware': 0,
    'version': 0,
    'last_update_check': 0,
    'created': 0,
    'uptime': 0,
    'is_owner': 0,
    '10min_avg': 0,
    '30min_avg': 0,
    '1hour_avg': 0,
    '6hour_avg': 0,
    '1day_avg': 0,
    '1week_avg': 0
}
```
