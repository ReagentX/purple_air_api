import unittest
from purpleair import purpleair, sensor


class TestPurpleAirMethods(unittest.TestCase):


    def test_setup_purpleair(self):
        p = purpleair.PurpleAir()
        self.assertIsInstance(p, purpleair.PurpleAir)


    def test_outside_sensor_filtering(self):
        p = purpleair.PurpleAir()
        self.assertLess(len(p.outside_sensors),len(p.all_sensors))


    def test_useful_sensor_filtering(self):
        p = purpleair.PurpleAir()
        self.assertLess(len(p.useful_sensors),len(p.all_sensors))


if __name__ == '__main__':
    unittest.main()
