# Frequently Asked Questions and Common Problems

If your question is not answered in this document, please open a new [issue](https://github.com/ReagentX/purple_air_api/issues).

Please refer to the [PurpleAir FAQ](https://www2.purpleair.com/community/faq) for questions related to the sensor network.

## How do I do ___

Please see the sample code section of the [readme](/README.md#example-code).

## What is the relationship between `SensorList`, `Sensor`, `Channel`, and `ThingSpeak`

This is a pseudo-JSON representation of the relationships between these data:

```log
[
    sensor_1: {
        'parent': {
            'primary': thingspeak.Channel,
            'secondary: thingspeak.Channel
        },
        'child': {
            'primary': thingspeak.Channel,
            'secondary: thingspeak.Channel
        }
    },
    sensor_2: {...},
    ...
]
```

The outer list represents the `SensorList`. `sensor_1` is an instance of `Sensor` and has two `Channel`s, `'parent'` and `'child'`. Each `Channel` has two ThingSpeak fields, `'primary'` and `'secondary'`.

## Why is `get_location()` slow

The `Sensor.get_location()` method returns the approximate street address from a sensor given the latitude and longitude value. Since we make the conversion using `geopy`'s `nominatim` API, we are limited to [1 request per second maximum](https://operations.osmfoundation.org/policies/nominatim/).

***

## Python Environment and PurpleAir Network problems

### ValueError: Invalid JSON data returned from network

Occasionally, PurpleAir's API will return invalid JSON. Usually, this means a double quote character or some other delimiter is missing. There is nothing we can do, so this library raise a `ValueError`.

The only fix is to try again or invalidate or delete the cache that `requests_cache` creates. If the invalid response is cached (it shouldn’t be), you can delete the cache by removing the `cache.sqlite` file it creates in the project’s root directory.

### Unable to open cache or purge cache database, requests will not be cached

This error means there is a problem connecting to the `cache.sqlite` file created by `requests_cache`. The program will still run, but results of API calls will not be cached, so affected programs may hit rate limits.

***

## Network and SensorList problems

### Child `{child_sensor_id}` lists parent `{parent_sensor_id}`, but parent does not exist

The child sensor requested lists a parent, but the parent does not exist on the PurpleAir network. This is a problem with PurpleAir, not this program. Try removing the `cache.sqlite` file it creates in the project’s root directory.

### No column name provided to filter on

`to_dataframe` was invoked with `sensor_filter` set to `'column'` but no value for the `column` parameter was provided. It should be invoked like this:

```python
p = SensorList()
p.to_dataframe(sensor_filter='column',
               channel='parent',
               column='m10avg')  # See Channel docs for all column options
```

### Column name provided does not exist in sensor data

`to_dataframe` was invoked with `sensor_filter` set to `'column'` and the value for the `column` parameter does not exist as a column. Please only use properties of a [Channel](/docs/documentation.md#Channel).

### No data for filter set: Column `{column}`, value filter: `{value_filter}`

`to_dataframe` was invoked with `sensor_filter` set to `'column'` and none of the values in the column denoted by the `column` parameter match the given `value_filter`. This means the DataFrame would be empty, so we raise an error here before the user attempts to transform data.

***

## Sensor Problems

### Invalid ThingSpeak key

Provided key does not exist on ThingSpeak. Refer to the [purpleair docs](/docs/purpleair_documentation.md#Field%20descriptions) for valid columns and their meanings.

### Invalid sensor channel: `{channel}`. Must be in `{"parent", "child"}`

A function that requires a `channel` parameter can only look at channels `parent` and `child`. Since there are no other channels, we raise an error when this occurs.

### Invalid sensor: no configuration found for `{identifer}`

The requested sensor does not have any data on PurpleAir.

### Sensor `{identifier}` created without valid data

A `Sensor` was created with the `json_data` parameter filled, but the json is malformed.

### Invalid sensor ID

The given `Sensor()`'s ID is not in valid integer form.

### More than 2 channels found for `{identifier}`

PurpleAir reports that a sensor has more than one child. This is a problem with PurpleAir, not this program. Try removing the `cache.sqlite` file it creates in the project’s root directory.

### No sensor data returned from PurpleAir

This error happens if the API fails to return data with a `results` key, where `results` is mapped to a JSON blob of sensors.

#### Rate Limit Error

If this error includes a rate limit message, try again when the rate limit is expired.

#### Other Message

If the error message is not a rate limit error, try to delete the cache by removing the `cache.sqlite` file it creates in the project’s root directory. If this does not solve the problem, please open a new [issue](https://github.com/ReagentX/purple_air_api/issues) with the full traceback and message.

***

## Other Crashes and Errors

If your problem is not listed here, please open a new [issue](https://github.com/ReagentX/purple_air_api/issues).
