# Purple Air API

A Python 3.x API Class to turn data from the PurpleAir/ThingSpeak API into a Pandas DataFrame with several utility methods.

![Global Sensor Map with Celsius Scale](maps/sensor_map.png)

## Installation

* To use
  * `pip install purpleair`
  * It is a good practice to only install within a [virtual environment](https://docs.python.org/3/library/venv.html)
* To hack
  * Clone this repo
  * `cd` to the folder
  * Create a virtual environment
    * `python -m venv venv`
  * Activate the virtual environment
    * `source venv/bin/activate`
  * Install as dependency in the virtual environment
    * `python setup.py develop`
  * Install third party dependencies
    * Required to run: `pip install -r requirements/common.txt`
    * Install development requirements with `pip install -r requirements/dev.txt`
    * Install example file requirements with `pip install -r requirements/examples.txt`

## Example code

For detailed documentation, see the [docs](docs/documentation.md) file.

### Listing all useful sensors

```python
from purpleair.network import SensorList
p = SensorList()  # Initialized 10,812 sensors!
print(len(p.useful_sensors))  # 10047, List of sensors with no defects
```

### Get location for a single sensor

```python
from purpleair.sensor import Sensor
s = Sensor('2890', parse_location=True)
print(s)  # Sensor 2891 at 10834, Canyon Road, Omaha, Douglas County, Nebraska, 68112, USA
```

### Make a DataFrame from all current sensor data

```python
from purpleair.network import SensorList
p = SensorList()  # Initialized 10,812 sensors!
df = p.to_dataframe(sensor_filter='all' channel='a')  # Other options include 'outside' and 'useful'
```

Result:

```log
             lat         lon                          name location_type  pm_2.5  temp_f     temp_c  ...  downgraded age 10min_avg 30min_avg  1hour_avg  6hour_avg  1week_avg
id                                                                                                   ...
14633  37.275561 -121.964134             Hazelwood canary        outside    7.15    92.0  33.333333  ...       False   1      6.50      5.13       4.11      12.44      42.94
25999  30.053808  -95.494643   Villages of Bridgestone AQI       outside   10.16   103.0  39.444444  ...       False   1      9.96     10.63      12.51      18.40      14.55
14091  37.883620 -122.070087                   WC Hillside       outside   11.36    89.0  31.666667  ...       False   1     10.31      8.74       7.21      20.03      63.44
42073  47.185173 -122.176855                            #1       outside   99.46    73.0  22.777778  ...       False   0    100.06    100.31     101.36     106.93      68.40
53069  47.190197 -122.177992                            #2       outside  109.82    79.0  26.111111  ...       False   0    109.52    108.72     109.33     116.64      74.52
```

### Get historical data for a single sensor

```python
from purpleair.sensor import Sensor
df = se.parent.get_historical(weeks_to_get=1,
                              sensor_channel='a',
                              thingspeak_field='secondary')
print(df.head())
```

Result:

```log
                        created_at  0.3um/dl  0.5um/dl  1.0um/dl  2.5um/dl  5.0um/dl  10.0um/dl  PM1.0_CF_1_ug/m3  PM10.0_CF_1_ug/m3
entry_id
1005925  2020-09-09 00:01:02+00:00      0.45      0.60      0.60   22694.0     -63.0       55.0             100.0               0.60
1005926  2020-09-09 00:03:02+00:00      0.63      0.86      0.86   22696.0     -63.0       55.0             100.0               0.86
1005927  2020-09-09 00:05:02+00:00      0.51      0.86      0.88   22698.0     -64.0       55.0             100.0               0.86
1005928  2020-09-09 00:07:03+00:00      0.71      1.04      1.48   22700.0     -63.0       55.0             100.0               1.04
1005929  2020-09-09 00:09:02+00:00      0.95      1.05      1.50   22702.0     -64.0       55.0             100.0               1.05
```

See examples in `/scripts` for more detail.
