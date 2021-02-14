# `Channel()` Methods

## `setup()`

This converts the JSON metadata to Python class properties, exposing data in a Pythonic way.

## `as_dict() -> dict`

Return a dictionary representation of a Channel. The data is shaped like this:

```python
{
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
}
```

## `as_flat_dict() -> dict`

Returns a flat dictionary representation of the Channel data.

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

## `get_historical(weeks_to_get: int, thingspeak_field: str, start_date: datetime = datetime.now()) -> pd.DataFrame`

Get data from the ThingSpeak API from field `thingspeak_field` one week at a time up to `weeks_to_get` weeks in the past.

`thingspeak_field` is one of `{'primary', 'secondary'}`.

`start_date` is an optional field to supply a start date. `weeks_to_get` is relative to this value. If not set, it defaults to `datetime.now()`

Parent Primary:

* `created_at`
  * Timestamp of data posting to ThingSpeak (created by ThingSpeak)
* `entry_id`
  * row number relative to all data Parent primary data (created by ThingSpeak)
* `PM1.0_CF_ATM_ug/m3`
  * mass concentration calculated from count data for particle sizes ~0.3um to ~1.0um for “atmospheric” particles (From Plantower 5003/1003)
* `PM2.5_CF_ATM_ug/m3`
  * mass concentration calculated from count data for particle sizes ~0.3um to ~2.5um for “atmospheric” particles (From Plantower 5003/1003)
* `PM10.0_CF_ATM_ug/m3`
  * mass concentration calculated from count data for particle sizes ~0.3um to ~10um for “atmospheric” particles (From Plantower 5003/1003)
* `UptimeMinutes`
  * the amount time the unit CPU has been running since it was powered up (From ESP8266 WiFi chip)
* `ADC`
  * Voltage (From ESP8266 WiFi chip)
* `Temperature_F`
  * Temperature inside of the sensor housing in Fahrenheit. On average, this is 8F higher than ambient conditions. (From BME280)
* `Humidity_%`
  * Relative humidity inside of the sensor housing as a percentage. On average, this is 4% lower than ambient conditions (From BME280)
* `PM2.5_CF_1_ug/m3`
  * mass concentration calculated from count data for particle sizes ~0.3um to ~2.5um for “standard” particles (From Plantower 5003/1003)

Parent Secondary:

* `created_at`
  * Timestamp of data posting to ThingSpeak (created by ThingSpeak)
* `entry_id`
  * row number relative to all data Parent primary data (created by ThingSpeak)
* `0.3um/dl`
  * aerodynamic diameter of >0.3 micrometer particle counts per deciliter of air
* `0.5um/dl`
  * aerodynamic diameter of >0.5 micrometer particle counts per deciliter of air (From Plantower 5003/1003)
* `1.0um/dl`
  * aerodynamic diameter of >1.0 micrometer particle counts per deciliter of air (From Plantower 5003/1003)
* `2.5um/dl`
  * aerodynamic diameter of >2.5 micrometer particle counts per deciliter of air (From Plantower 5003/1003)
* `5.0um/dl`
  * aerodynamic diameter of >5.0 micrometer particle counts per deciliter of air  (From Plantower 5003/1003)
* `10.0um/dl`
  * aerodynamic diameter of >10.0 micrometer particle counts per deciliter of air (From Plantower 5003/1003)
* `PM1.0_CF_1_ug/m3`
  * mass concentration calculated from count data for particle sizes 0.3um to ~1.0um for “standard” particles (From Plantower 5003/1003)
* `PM10.0_CF_1_ug/m3`
  * mass concentration calculated from count data for particle sizes ~0.3um to ~10um for “standard” particles (From Plantower 5003/1003)

Child Primary:

* `created_at`
  * Timestamp of data posting to ThingSpeak (created by ThingSpeak)
* `entry_id`
  * row number relative to all data child primary data (created by ThingSpeak)
* `PM1.0_CF_ATM_ug/m3`
  * mass concentration calculated from count data for particle sizes ~0.3um to ~1.0um for “atmospheric” particles (From Plantower 5003/1003)
* `PM2.5_CF_ATM_ug/m3`
  * mass concentration calculated from count data for particle sizes ~0.3um to ~2.5um for “atmospheric” particles (From Plantower 5003/1003)
* `PM10.0_CF_ATM_ug/m3`
  * mass concentration calculated from count data for particle sizes ~0.3um to ~10um for “atmospheric” particles (From Plantower 5003/1003)
* `UptimeMinutes`
  * the amount time the unit CPU has been running since it was powered up
* `RSSI_dbm`
  * WiFi strength (From ESP8266 WiFi chip)
* `Pressure_hpa`
  * Pressure inside of the sensor housing in hectopascal. (From BME280)
* `Blank`
  * No Data
  * Note: there appears to be some float data in this column
* `PM2.5_CF_1_ug/m3`
  * mass concentration calculated from count data for particle sizes ~0.3um to ~2.5um for “standard” particles (From Plantower 5003/1003)

Child Secondary:

* `created_at`
  * Timestamp of data posting to ThingSpeak (created by ThingSpeak)
* `entry_id`
  * row number relative to all data child primary data (created by ThingSpeak)
* `0.3um/dl`
  * aerodynamic diameter of >0.3 micrometer particle counts per deciliter of air
* `0.5um/dl`
  * aerodynamic diameter of >0.5 micrometer particle counts per deciliter of air (From Plantower 5003/1003)
* `1.0um/dl`
  * aerodynamic diameter of >1.0 micrometer particle counts per deciliter of air (From Plantower 5003/1003)
* `2.5um/dl`
  * aerodynamic diameter of >2.5 micrometer particle counts per deciliter of air (From Plantower 5003/1003)
* `5.0um/dl`
  * aerodynamic diameter of >5.0 micrometer particle counts per deciliter of air (From Plantower 5003/1003)
* `10.0um/dl`
  * aerodynamic diameter of >10.0 micrometer particle counts per deciliter of air (From Plantower 5003/1003)
* `PM1.0_CF_1_ug/m3`
  * mass concentration calculated from count data for particle sizes 0.3um to ~1.0um for “standard” particles (From Plantower 5003/1003)
* `PM10.0_CF_1_ug/m3`
  * mass concentration calculated from count data for particle sizes ~0.3um to ~10um for “standard” particles (From Plantower 5003/1003)
