from purpleair import purpleair
from purpleair import sensor


# All Sensors
p = purpleair.PurpleAir()
print(len(p.useful_sensors))
s = p.useful_sensors[0] # First confirmed useful sensor
# s.get_location()
print(s)


# Single sensor
se = sensor.Sensor('2891', parse_location=True)
se.get_field('field3')
se.get_field('field4')
print(se.thingspeak_data.keys())
print(se)
