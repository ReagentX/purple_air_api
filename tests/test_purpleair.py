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
        p.to_dataframe('all', 'parent')
        p.to_dataframe('all', 'child')

    def test_to_dataframe_filtering_outside(self):
        """
        Test that outside sensor filter works
        """
        p = network.SensorList()
        p.to_dataframe('outside', 'parent')
        p.to_dataframe('outside', 'child')

    def test_to_dataframe_filtering_useful(self):
        """
        Test that useful sensor filter works
        """
        p = network.SensorList()
        p.to_dataframe('useful', 'parent')
        p.to_dataframe('useful', 'child')

    def test_to_dataframe_filtering_no_child(self):
        """
        Test that no_child sensor filter works
        """
        p = network.SensorList()
        p.to_dataframe('no_child', 'parent')
        p.to_dataframe('no_child', 'child')

    def test_to_dataframe_filtering_family(self):
        """
        Test that family sensor filter works
        """
        p = network.SensorList()
        p.to_dataframe('family', 'parent')
        p.to_dataframe('family', 'child')

    def test_to_dataframe_cols(self):
        p = network.SensorList()
        df_a = p.to_dataframe(sensor_filter='all', channel='parent')
        df_b = p.to_dataframe(sensor_filter='all', channel='child')
        self.assertListEqual(list(df_a.columns), list(df_b.columns))


class TestPurpleAirColumnFilters(unittest.TestCase):
    """
    Test that we can initialize the PurpleAir network
    """

    def test_to_dataframe_filtering_no_column(self):
        """
        Test that not providing a column fails
        """
        p = network.SensorList()
        with self.assertRaises(ValueError):
            p.to_dataframe('column', 'parent')

        with self.assertRaises(ValueError):
            p.to_dataframe('column', 'child')

    def test_to_dataframe_filtering_bad_column(self):
        """
        Test that providing a bad column fails
        """
        p = network.SensorList()
        with self.assertRaises(ValueError):
            p.to_dataframe('column', 'parent', 'fake_col_name')

        with self.assertRaises(ValueError):
            p.to_dataframe('column', 'child', 'fake_col_name')

    def test_to_dataframe_filtering_no_value(self):
        """
        Test that providing a bad value fails
        """
        p = network.SensorList()
        p.to_dataframe('column', 'parent', 'temp_f')
        p.to_dataframe('column', 'child', 'temp_f')

    def test_to_dataframe_filtering_good_value(self):
        """
        Test that providing a bad value fails
        """
        p = network.SensorList()
        p.to_dataframe('column', 'parent', 'location_type', 'outside')
        with self.assertRaises(ValueError):
            p.to_dataframe('column', 'child', 'location_type', 'outside')

    def test_to_dataframe_filtering_bad_value(self):
        """
        Test that providing a bad value fails
        """
        p = network.SensorList()
        with self.assertRaises(ValueError):
            p.to_dataframe('column', 'parent', 'location_type', 1234)

        with self.assertRaises(ValueError):
            p.to_dataframe('column', 'child', 'location_type', 1234)
