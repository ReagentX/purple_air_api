import unittest
from purpleair import purpleair, sensor


class TestSensorMethods(unittest.TestCase):


    def test_create_sensor_location(self):
        se = sensor.Sensor('2891', parse_location=True)
        self.assertEqual(se.__repr__(), 'Sensor 2891 at 10834, Canyon Road, Omaha, Douglas County, Nebraska, 68112, United States of America')


    def test_create_sensor_no_location(self):
        se = sensor.Sensor('2891')
        self.assertEqual(se.__repr__(), 'Sensor 2891')


    def test_is_useful(self):
        se = sensor.Sensor('14633')
        self.assertEqual(se.is_useful(), True)


    def test_as_dict(self):
        se = sensor.Sensor('2891')
        expected_shape = {
            'meta': {
                'id': 0,
                'lat': 0,
                'lon': 0,
                'name': 0,
                'locaction_type': 0
            },
            'data': {
                'pm_2.5': 0,
                'temp_f': 0,
                'temp_c': 0,
                'humidity': 0,
                'pressure': 0
            },
            'statistics': {
                '10min_avg': 0,
                '30min_avg': 0,
                '1hour_avg': 0,
                '6hour_avg': 0,
                '1week_avg': 0
            },
            'diagnostic': {
                'last_seen': 0,
                'model': 0,
                'hidden': 0,
                'flagged': 0,
                'downgraded': 0,
                'age': 0
            }
        }
        src = se.as_dict()
        for data_category in expected_shape:
            self.assertIn(data_category, src)
            for data in expected_shape[data_category]:
                self.assertIn(data, src[data_category])


    def test_as_flat_dict(self):
        se = sensor.Sensor('2891')
        src = se.as_flat_dict()
        for data in src:
            self.assertNotIsInstance(src[data], dict)


if __name__ == '__main__':
    unittest.main()