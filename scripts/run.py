from purpleair import purpleair


p = purpleair.PurpleAir()
print(len(p.useful_sensors))
s = p.useful_sensors[0]
s.get_field('field2')
s.get_location()
# print(s.thingspeak_data)
print(s)