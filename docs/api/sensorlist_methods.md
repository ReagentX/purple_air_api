# `SensorList()` Methods

## `get_all_data()`

Automatically run on instantiation. Retrieves the current network data from the PurpleAir API.

## `to_dataframe(sensor_group: str, channel: str, column: Optional[str] = None, value_filter: Union[str, int, float, None] = None) -> pd.DataFrame`

Converts dictionary representation of a list of sensors to a Pandas DataFrame where `sensor_group` determines which group of sensors are used.

`channel` is one of `{'parent', 'child'}`.

* `'useful'`
  * Sensors with no faults, as determined by [`is_useful()`](/docs/api/sensor_methods.md#is_useful---bool)
* `'outside'`
  * Outdoor sensors only
* `'all'`
  * Do not filter sensors
* `family`
  * Sensor has both parent and child
* `column`
  * Must be a value that exists on a [Channel](/docs/documentation.md#channel)
  * If `value_filter` is not provided:
    * Sensor has data in `column`, i.e. no `None` values
  * If `value_filter` is provided:
    * Sensor has data in `column` that is the same as `value_filter`

If `sensor_group` is not in the above set, `to_dataframe()`  will raise a `ValueError`.
