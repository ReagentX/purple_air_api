from purpleair.purpleair import PurpleAir
from purpleair.sensor import Sensor


# All Sensors
p = PurpleAir()
print(len(p.useful_sensors))
s = p.useful_sensors[0] # First confirmed useful sensor
s.get_location()
print(s.as_flat_dict())
df = p.to_dataframe('useful')
print(df.head())

# Single sensor
se = Sensor('2891', parse_location=True)
se.get_field('field3')
se.get_field('field4')
print(se.thingspeak_data.keys())
print(se.get_historical(weeks_to_get=1, sensor_channel='a'))
