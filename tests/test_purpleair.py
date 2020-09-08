import unittest
from purpleair import network


class TestPurpleAirMethods(unittest.TestCase):


    def test_setup_purpleair(self):
        p = network.SensorList()
        self.assertIsInstance(p, network.SensorList)


    def test_outside_sensor_filtering(self):
        p = network.SensorList()
        self.assertLess(len(p.outside_sensors),len(p.all_sensors))


    def test_useful_sensor_filtering(self):
        p = network.SensorList()
        self.assertLess(len(p.useful_sensors),len(p.all_sensors))


if __name__ == '__main__':
    unittest.main()
