# `Channel()` Methods

## `setup()`

This converts the JSON metadata to Python class properties, exposing data in a Pythonic way.

## `get_historical(weeks_to_get: int, thingspeak_field: str) -> pd.DataFrame`

Get data from the ThingSpeak API from field `thingspeak_field` one week at a time up to `weeks_to_get` weeks in the past.

`thingspeak_field` is one of `{'primary', 'secondary'}`.

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
