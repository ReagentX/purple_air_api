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

    def test_to_dataframe_no_filtering(self):
        """
        Test that not using sensor filters works
        """
        p = network.SensorList()
        p.to_dataframe('all', 'a')
        p.to_dataframe('all', 'b')

    def test_to_dataframe_filtering_outside(self):
        """
        Test that outside sensor filter works
        """
        p = network.SensorList()
        p.to_dataframe('outside', 'a')
        p.to_dataframe('outside', 'b')

    def test_to_dataframe_filtering_useful(self):
        """
        Test that useful sensor filter works
        """
        p = network.SensorList()
        p.to_dataframe('useful', 'a')
        p.to_dataframe('useful', 'b')

    def test_to_dataframe_filtering_no_child(self):
        """
        Test that no_child sensor filter works
        """
        p = network.SensorList()
        p.to_dataframe('no_child', 'a')
        p.to_dataframe('no_child', 'b')

    def test_to_dataframe_filtering_family(self):
        """
        Test that family sensor filter works
        """
        p = network.SensorList()
        p.to_dataframe('family', 'a')
        p.to_dataframe('family', 'b')

    def test_to_dataframe_cols(self):
        p = network.SensorList()
        df_a = p.to_dataframe(sensor_filter='all', channel='a')
        df_b = p.to_dataframe(sensor_filter='all', channel='b')
        self.assertListEqual(list(df_a.columns), list(df_b.columns))


class TestPurpleAirColumnFilters(unittest.TestCase):
    """
    Test that we can initialize the PurpleAir network
    """
    def test_to_dataframe_filtering_no_column(self):
        """
        Test that not providing a column fails
        """
        with self.assertRaises(ValueError):
            p = network.SensorList()
            p.to_dataframe('column', 'a')
            p.to_dataframe('column', 'b')

    def test_to_dataframe_filtering_bad_column(self):
        """
        Test that providing a bad column fails
        """
        with self.assertRaises(ValueError):
            p = network.SensorList()
            p.to_dataframe('column', 'a', 'fake_col_name')
            p.to_dataframe('column', 'b', 'fake_col_name')

    def test_to_dataframe_filtering_no_value(self):
        """
        Test that providing a bad value fails
        """
        p = network.SensorList()
        p.to_dataframe('column', 'a', 'temp_f')
        p.to_dataframe('column', 'b', 'temp_f')

    def test_to_dataframe_filtering_good_value(self):
        """
        Test that providing a bad value fails
        """
        p = network.SensorList()
        p.to_dataframe('column', 'a', 'location_type', 'outside')
        with self.assertRaises(ValueError):
            p.to_dataframe('column', 'b', 'location_type', 'outside')

    def test_to_dataframe_filtering_bad_value(self):
        """
        Test that providing a bad value fails
        """
        with self.assertRaises(ValueError):
            p = network.SensorList()
            p.to_dataframe('column', 'a', 'location_type', 1234)
            p.to_dataframe('column', 'b', 'location_type', 1234)

if __name__ == '__main__':
    unittest.main()
