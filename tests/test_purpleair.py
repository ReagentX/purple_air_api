import unittest

from purpleair import network


class TestPurpleAirMethods(unittest.TestCase):
    """
    Test that we can initialize the PurpleAir network
    """

    def test_setup_purpleair(self):
        """
        Test that we can initialize a SensorList
        """
        p = network.SensorList()
        self.assertIsInstance(p, network.SensorList)

    def test_outside_sensor_filtering(self):
        """
        Test that outdoor sensor filter work
        """
        p = network.SensorList()
        self.assertLess(len(p.outside_sensors), len(p.all_sensors))

    def test_useful_sensor_filtering(self):
        """
        Test that useful sensor filter works
        """
        p = network.SensorList()
        self.assertLess(len(p.useful_sensors), len(p.all_sensors))

    def test_to_dataframe_filtering(self):
        """
        Test that useful sensor filter works
        """
        p = network.SensorList()
        self.assertEqual(len(p.to_dataframe('all', 'a')), len(p.all_sensors))
        self.assertEqual(len(p.to_dataframe('all', 'b')), len(p.all_sensors))
        self.assertEqual(len(p.to_dataframe('outside', 'a')), len(p.outside_sensors))
        self.assertEqual(len(p.to_dataframe('outside', 'b')), len(p.outside_sensors))
        self.assertEqual(len(p.to_dataframe('useful', 'a')), len(p.useful_sensors))
        self.assertEqual(len(p.to_dataframe('useful', 'b')), len(p.useful_sensors))


if __name__ == '__main__':
    unittest.main()
