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

### Listing all useful sensors

```python
from purpleair.network import SensorList
p = SensorList()  # Initialized 18,877 sensors!
print(len(p.useful_sensors))  # 7174, List of sensors with no defects
```

### Get location for a single sensor

```python
from purpleair.sensor import Sensor
s = Sensor('2891', parse_location=True)
print(s)  # Sensor 2891 at 10834, Canyon Road, Omaha, Douglas County, Nebraska, 68112, USA
```

### Make a DataFrame from all current sensor data

```python
from purpleair.network import SensorList
p = SensorList()  # Initialized 18,877 sensors!
df = p.to_dataframe('all')  # Other options include 'outdoor' and 'useful'
```

Result:

```log
            age  downgraded  flagged  hidden  humidity         last_seen  ...                  name   parent  pm_2.5 pressure     temp_c  temp_f
id                                                                        ...
24115   36026       False    False   False      0.15 2019-01-09 20:33:05  ...   2nd South 12th East      NaN    0.15   869.14  31.666667    89.0
16791       0       False    False   False      0.60 2019-02-03 20:59:26  ...                DW0435      NaN    1.96  1009.82  30.000000    86.0
16792       0       False    False   False      0.60 2019-02-03 20:59:29  ...              DW0435 B  16791.0    1.65  1009.77  30.000000    86.0
14633       0       False    False   False      0.55 2019-02-03 20:59:48  ...     Hazelwood canary       NaN    0.29  1000.25  18.333333    65.0
6522   538227       False    False   False      0.22 2018-01-26 02:32:25  ...                Indoor      NaN    1.33   837.97  23.888889    75.0
```

### Get historical data for a single sensor

```python
from purpleair.sensor import Sensor
se = Sensor('2891')
print(se.get_historical(weeks_to_get=1, sensor_channel='a').head())
```

Result:

```log
                        created_at  PM1 CF=ATM ug/m3  PM25 CF=ATM ug/m3  PM10 CF=ATM ug/m3  Free HEAP memory  ADC0 Voltage  Sensor Firmware  Unused  PM25 CF=1 ug/m3
entry_id
536245   2019-01-27 00:00:35+00:00             12.87              17.70              18.39           30032.0          0.02           973.99     NaN            17.70
536246   2019-01-27 00:01:55+00:00             13.04              18.13              18.53           30584.0          0.02           974.00     NaN            18.13
536247   2019-01-27 00:03:15+00:00             14.80              18.91              20.33           30632.0          0.02           973.97     NaN            18.91
536248   2019-01-27 00:04:36+00:00             14.64              19.22              20.98           30720.0          0.02           974.03     NaN            19.22
536249   2019-01-27 00:05:55+00:00             15.16              19.71              20.56           30776.0          0.02           974.05     NaN            19.71
```

See examples in `/scripts` for more detail.
