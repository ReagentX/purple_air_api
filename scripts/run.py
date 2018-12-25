from purpleair import purpleair
from purpleair import sensor


p = purpleair.PurpleAir()
print(len(p.useful_sensors))
s = p.useful_sensors[0]
s.get_field('field2')
# s.get_location()
print(s)

se = sensor.Sensor('2891', parse_location=True)
se.get_field('field3')
se.get_field('field4')
print(se.thingspeak_data.keys())
print(se)
