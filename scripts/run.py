"""
Sample script to run quick tests
"""


from purpleair.network import SensorList
from purpleair.sensor import Sensor

# All Sensors
p = SensorList()
s = p.all_sensors[0]  # First sensor found
s.get_location()
df = p.to_dataframe(sensor_filter='all', channel='parent')
print(df.head())

# Single sensor
se = Sensor(2890)
print(se)
print(se.parent)
print(se.child)
print(se.parent.as_flat_dict())
se.get_field(3)
se.get_field(4)
print(se.thingspeak_data.keys())
df = se.parent.get_historical(weeks_to_get=1,
                              thingspeak_field='secondary')
print(df.head())
