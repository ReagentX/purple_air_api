"""
Sample script to run quick tests
"""


from purpleair import channel
from purpleair.network import SensorList
from purpleair.sensor import Sensor


# All Sensors
p = SensorList()
print(len(p.useful_sensors))
s = p.useful_sensors[0]  # First confirmed useful sensor
s.get_location()
df = p.to_dataframe(sensor_filter='all', channel='a')
print(df.head())

# Single sensor
se = Sensor('2890')
print(se)
print(se.channel_a)
print(se.channel_b)
print(se.as_flat_dict('a'))
se.get_field('field3')
se.get_field('field4')
print(se.thingspeak_data.keys())
df = se.channel_a.get_historical(weeks_to_get=1,
                                 sensor_channel='a',
                                 thingspeak_field='secondary')
print(df.head())
