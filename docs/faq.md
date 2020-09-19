# Frequently Asked Questions and Common Problems

## ValueError: Invalid JSON data returned from network

Occasionally, PurpleAir's API will return invalid JSON. Usually, this means a double quote char or some other delimiter is missing. There is nothing we can do, so this library raise a ValueError.

The only fix is to try again or invalidate or delete the cache that `requests_cache` creates. If the invalid response is cached (it shouldn’t be), you can delete the cache by removing the `cache.sqlite` file it creates in the project’s root directory.

## Unable to open cache or purge cache database, requests will not be cached

This error means there is a problem connecting to the `cache.sqlite` file created by `requests_cache`. The program will still run, but results of API calls will not be cached, so affected programs may hit rate limits.

## Invalid ThingSpeak key

Provided key does not exist on ThingSpeak. Refer to the [purpleair docs](/docs/purpleair_documentation.md#Field%20descriptions) for valid columns and their meanings.

## Child `{child_sensor_id}` lists parent `{parent_sensor_id}`, but parent does not exist

The child sensor requested lists a parent, but the parent does not exist on the PurpleAir network. This is a problem with PurpleAir, not this program. Try removing the `cache.sqlite` file it creates in the project’s root directory.

## No column name provided to filter on

`to_dataframe` was invoked with `sensor_filter` set to `'column'` but no value for the `column` parameter was provided. It should be invoked like this:

```python
p = SensorList()
p.to_dataframe(sensor_filter='column',
                      channel='a',
                      column='m10avg')  # See Channel docs for all column options
```

## Column name provided does not exist in sensor data

`to_dataframe` was invoked with `sensor_filter` set to `'column'` and the value for the `column` parameter does not exist as a column. Please only use properties of a [Channel](/docs/documentation.md#Channel).

## No data for filter set: Column `{column}`, value filter: `{value_filter}`

`to_dataframe` was invoked with `sensor_filter` set to `'column'` and none of the values in the column denoted by the `column` parameter match the given `value_filter`. This means the DataFrame would be empty, so we raise an error here before the user attempts to transform data.

## Invalid sensor channel: `{channel}`. Must be in `{"a", "b"}`

A function that requires a `channel` parameter can only look at channels `a` and `b`. Since there are no other channels, we raise an error when this occurs.

## Invalid sensor: no configuration found for `{identifer}`

The requested sensor does not have any data on PurpleAir.

## Sensor `{identifier}` created without valid data

A `Sensor` was created with the `json_data` parameter filled, but the json is malformed.

## Invalid sensor ID

The given `Sensor()`'s ID is not in valid integer form.

## More than 2 channels found for `{identifier}`

PurpleAir reports that a sensor has more than one child. This is a problem with PurpleAir, not this program. Try removing the `cache.sqlite` file it creates in the project’s root directory.

## No sensor data returned from PurpleAir

This error happens if the API fails to return data with a `results` key, where `results` is mapped to a JSON blob of sensors.

### Rate Limit Error

If this error includes a rate limit message, try again when the rate limit is expired.

### Other Message

If the error message is not a rate limit error, please open a new [issue](https://github.com/ReagentX/purple_air_api/issues) with the full traceback and message.

## Other Crashes and Errors

If your problem is not listed here, please open a new [issue](https://github.com/ReagentX/purple_air_api/issues).
