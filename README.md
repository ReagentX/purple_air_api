# purple_air_api

A Python 3.7 API Class to turn data from the PurpleAir/ThingSpeak API into a Pandas Dataframe with several utility methods.

## Installation

- Clone this repo
- `cd` to the folder
- `python setup.py develop`

## Example code:

    from purpleair import purpleair
    from purpleair import sensor


    # All Sensors
    p = purpleair.PurpleAir()  # Initialized 10589 sensors!
    print(len(p.useful_sensors))  # List of sensors with no defects


    # Single sensor
    s = sensor.Sensor('2891', parse_location=True)
    s.get_field('field3')
    s.get_field('field4')
    print(s.thingspeak_data.keys())  # dict_keys(['field3', 'field4'])
    print(s)  # Sensor 2891 at 10834, Canyon Road, Omaha, Douglas County, Nebraska, 68112, USA
