# purple_air_api

A Python 3.7 API Class to turn data from the PurpleAir/ThingSpeak API into a Pandas Dataframe with several utility methods.

![](https://github.com/ReagentX/purple_air_api/blob/master/maps/sensor_map.png)

## Installation

- Clone this repo
- `cd` to the folder
- `python setup.py develop`

## Example code:

### Listing all useful sensors

    from purpleair import purpleair
    p = purpleair.PurpleAir()  # Initialized 10589 sensors!
    print(len(p.useful_sensors))  # List of sensors with no defects


### Get location for a single sensor

    from purpleair import sensor
    s = sensor.Sensor('2891', parse_location=True)
    print(s)  # Sensor 2891 at 10834, Canyon Road, Omaha, Douglas County, Nebraska, 68112, USA

### Get historical data for a single sensor

    from purpleair import sensor
    se = sensor.Sensor('2891', parse_location=True)
    print(se.get_historical(3).head())

    # Will print
                            created_at  PM1 CF=ATM ug/m3  PM25 CF=ATM ug/m3  PM10 CF=ATM ug/m3  Free HEAP memory  ADC0 Voltage  Sensor Firmware  Unused  PM25 CF=1 ug/m3
    entry_id
    536245   2019-01-27 00:00:35+00:00             12.87              17.70              18.39           30032.0          0.02           973.99     NaN            17.70
    536246   2019-01-27 00:01:55+00:00             13.04              18.13              18.53           30584.0          0.02           974.00     NaN            18.13
    536247   2019-01-27 00:03:15+00:00             14.80              18.91              20.33           30632.0          0.02           973.97     NaN            18.91
    536248   2019-01-27 00:04:36+00:00             14.64              19.22              20.98           30720.0          0.02           974.03     NaN            19.22
    536249   2019-01-27 00:05:55+00:00             15.16              19.71              20.56           30776.0          0.02           974.05     NaN            19.71

See examples in `/scripts` for more detail.