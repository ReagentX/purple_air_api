import unittest

from purpleair import sensor


class TestChannelMethods(unittest.TestCase):
    """
    Tests for Sensor class
    """

    def test_get_historical(self):
        """
        Test that we properly get a sensor's historical data
        """
        se = sensor.Sensor(2891)
        se.parent.get_historical(1, 'primary')
        se.parent.get_historical(1, 'secondary')
        se.child.get_historical(1, 'primary')
        se.child.get_historical(1, 'secondary')

    def test_as_dict(self):
        """
        Test that channel dictionary representation works
        """
        se = sensor.Sensor(1243)
        expected_shape = {
            'meta': {
                'id': 0,
                'parent': 0,
                'lat': 0,
                'lon': 0,
                'name': 0,
                'location_type': 0,
            },
            'data': {
                'pm_2.5': 0,
                'temp_f': 0,
                'temp_c': 0,
                'humidity': 0,
                'pressure': 0,
                'p_0_3_um': 0,
                'p_0_5_um': 0,
                'p_1_0_um': 0,
                'p_2_5_um': 0,
                'p_5_0_um': 0,
                'p_10_0_um': 0,
                'pm1_0_cf_1': 0,
                'pm2_5_cf_1': 0,
                'pm10_0_cf_1': 0,
                'pm1_0_atm': 0,
                'pm2_5_atm': 0,
                'pm10_0_atm': 0,
            },
            'diagnostic': {
                'last_seen': 0,
                'model': 0,
                'adc': 0,
                'rssi': 0,
                'hidden': 0,
                'flagged': 0,
                'downgraded': 0,
                'age': 0,
                'brightness': 0,
                'hardware': 0,
                'version': 0,
                'last_update_check': 0,
                'created': 0,
                'uptime': 0,
                'is_owner': 0,
            }
        }
        # Parent channel
        result = se.parent.as_dict()
        for key in expected_shape:
            self.assertIn(key, result)
            resolved_data = result[key]
            expected_data = expected_shape[key]
            for key_2 in expected_data:
                self.assertIn(key_2, resolved_data)

        # Child channel
        result = se.child.as_dict()
        for key in expected_shape:
            self.assertIn(key, result)
            resolved_data = result[key]
            expected_data = expected_shape[key]
            for key_2 in expected_data:
                self.assertIn(key_2, resolved_data)

    def test_as_flat_dict(self):
        """
        Test that channel flat dictionary representation works
        """
        se = sensor.Sensor(9234)
        expected_shape = {
            'id': 0,
            'parent': 0,
            'lat': 0,
            'lon': 0,
            'name': 0,
            'location_type': 0,
            'pm_2.5': 0,
            'temp_f': 0,
            'temp_c': 0,
            'humidity': 0,
            'pressure': 0,
            'p_0_3_um': 0,
            'p_0_5_um': 0,
            'p_1_0_um': 0,
            'p_2_5_um': 0,
            'p_5_0_um': 0,
            'p_10_0_um': 0,
            'pm1_0_cf_1': 0,
            'pm2_5_cf_1': 0,
            'pm10_0_cf_1': 0,
            'pm1_0_atm': 0,
            'pm2_5_atm': 0,
            'pm10_0_atm': 0,
            'last_seen': 0,
            'model': 0,
            'adc': 0,
            'rssi': 0,
            'hidden': 0,
            'flagged': 0,
            'downgraded': 0,
            'age': 0,
            'brightness': 0,
            'hardware': 0,
            'version': 0,
            'last_update_check': 0,
            'created': 0,
            'uptime': 0,
            'is_owner': 0,
        }
        # Parent channel
        result = se.parent.as_flat_dict()
        for key in expected_shape:
            self.assertIn(key, result)

        # Child channel
        result = se.child.as_flat_dict()
        for key in expected_shape:
            self.assertIn(key, result)


if __name__ == '__main__':
    unittest.main()
