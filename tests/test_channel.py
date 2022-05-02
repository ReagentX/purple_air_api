import unittest

from purpleair import sensor
from purpleair import api_data
import datetime

class TestChannelMethods(unittest.TestCase):
    """
    Tests for Sensor class
    """

    def test_can_repr(self):
        """
        Test that we properly generate a Channel's string representation
        """
        se = sensor.Sensor(2891)
        self.assertEqual(se.child.__repr__(), 'Sensor 2891, child of 2890')

    def test_get_historical(self):
        """
        Test that we properly get a sensor's historical data
        """
        se = sensor.Sensor(2891)
        se.parent.get_historical(2, 'primary')
        se.parent.get_historical(1, 'secondary')
        se.child.get_historical(1, 'primary')
        se.child.get_historical(1, 'secondary')
    
    def columns_for_channel(self, channel_type):
        if channel_type == 'child':
            columns = set(api_data.CHILD_PRIMARY_COLS.values())
            columns.update( api_data.CHILD_SECONDARY_COLS.values())
            columns.remove('entry_id') # remove entry_id
        else:
            columns = set(api_data.PARENT_PRIMARY_COLS.values())
            columns.update( api_data.PARENT_SECONDARY_COLS.values())
            columns.remove('entry_id') # remove entry_id
        
        return columns

    def test_get_all_historical(self):
        """
        Test that we properly get both primary and secondary data in one go using the _all method
        """
        se = sensor.Sensor(2891)
        
        # parent sensor
        parent_results = se.parent.get_all_historical(1)
        parent_columns = self.columns_for_channel('parent')

        for field in parent_columns:
            self.assertTrue(field in parent_results.columns)
        
        
        # child sensor
        child_results = se.child.get_all_historical(1)
        child_columns = self.columns_for_channel('child')
        
        for field in child_columns:
            self.assertTrue(field in child_results.columns)
    
    def test_get_historical_between(self):
        """
        Test getting the sensor's historical data between two dates
        """
        
        se = sensor.Sensor(2891)
        start_date = datetime.datetime.today() - datetime.timedelta(weeks=1)
        se.parent.get_historical_between('primary', start_date)
    
    def test_get_all_historical_between(self):
        """
        Test getting all the sensor's historical data (primary and secondary) between two dates
        """
        se = sensor.Sensor(2891)
        start_date = datetime.datetime.today() - datetime.timedelta(weeks=1)
        results = se.parent.get_all_historical_between(start_date)
        columns = self.columns_for_channel('parent')
        for field in columns:
            self.assertTrue(field in results.columns)

    def test_get_average_values(self):
        se = sensor.Sensor(2891)
        results = se.parent.get_historical(1, 'primary', thingspeak_args={'average': 'daily'})
        self.assertTrue(len(results) in [7,8]) # either 7 or 8 results will be returned - depending on if we span 7 or 8 days with our 'week' time

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
