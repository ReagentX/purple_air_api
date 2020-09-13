# `SensorList()` Methods

## `get_all_data()`

Automatically run on instantiation. Retrieves the current network data from the PurpleAir API.

## `to_dataframe(sensor_group: str) -> pd.DataFrame`

Converts dictionary representation of a list of sensors to a Pandas DataFrame where `sensor_group` determines which group of sensors are used.

* `'useful'`
  * Sensors with no faults, as determined by [`is_useful()`](/docs/api/sensor_methods.md#is_useful)
* `'outside'`
  * Outdoor sensors only
* `'all'`
  * Do not filter sensors

If `sensor_group` is not in the above set, `to_dataframe()`  will raise a `ValueError`.
