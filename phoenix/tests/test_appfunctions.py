"""
Unittests for functions used to modify data for use in the dash app.
"""
import unittest

import phoenix.code.appfunctions as af

import pandas as pd


class TestAppFunctions(unittest.TestCase):
    """
    Contains test cases for Phoenix
    """

    def test_smoke_subset_date(self):
        """
        Smoke test for subset_date function.
        Returns: True if function produces a data frame
        """
        data = {'observation date': ['08-01-2020', '09-01-2020',
                '10-01-2020', '11-01-2020'],
                'species': ['American Crow', 'American Crow',
                            'American Crow', 'American Crow']}
        bird_data = pd.DataFrame(data, columns=['observation date', 'species'])
        bird_data['observation date'] = pd.to_datetime(bird_data['observation date'])
        month = 'August'
        day = 1

        self.assertTrue(
                isinstance(af.subset_date(
                    bird_data, 'observation date', month, day),
                    pd.DataFrame))

    def test_one_shot_subset_date(self):
        """
        One shot test for subset_data function.
        Returns true if resulting dataframe is equal to data_result.
        """

        data = {'observation date': ['08-01-2020', '09-01-2020',
                '10-01-2020', '11-01-2020'],
                'species': ['American Crow', 'American Crow',
                            'American Crow', 'American Crow']}
        bird_data = pd.DataFrame(data, columns=['observation date', 'species'])
        bird_data['observation date'] = pd.to_datetime(bird_data['observation date'])
        month = 'August'
        day = 1
        data_result = {'observation date': ['08-01-2020'],
                       'species': ['American Crow']}
        data_result = pd.DataFrame(data_result,
                                   columns=['observation date', 'species'])
        data_result['observation date'] = pd.to_datetime(data_result['observation date'])

        data_test = af.subset_date(
                    bird_data, 'observation date', month, day)
        self.assertTrue(data_test.equals(data_result))

    def test_edgetest_subset_date(self):
        """
        Edge test for subset_date function.
        Returns true if a Value Error is raised.
        """
        data = {'observation date': ['08-01-2020', '09-01-2020',
                '10-01-2020', '11-01-2020'],
                'species': ['American Crow', 'American Crow',
                            'American Crow', 'American Crow']}
        bird_data = pd.DataFrame(data, columns=['observation date', 'species'])
        bird_data['observation date'] = pd.to_datetime(bird_data['observation date'])
        month = 'August'
        day = 5

        with self.assertRaises(ValueError):
            af.subset_date(
                bird_data, 'observation date', month, day)

    def test_smoke_subset_air_quality(self):
        """
        Smoke test for subset_air_quality function.
        Returns true if function returns four lists.
        """
        data = {'Date': ['09-15-2020', '09-20-2020', '08-15-2020', '09-10-2020'],
                'AQI_Category': ['Hazardous', 'Very Unhealthy', 'Good', 'Very Unhealthy'],
                'County': ['Baker', 'Baker', 'Baker', 'Clackamas']}
        aq_data = pd.DataFrame(data, columns=['Date', 'AQI_Category', 'County'])
        aq_data['Date'] = pd.to_datetime(aq_data['Date'])
        county_name = 'Baker'
        haz_dates, haz_dates_offset, vh_dates, vh_dates_offset = af.subset_air_quality(
            aq_data, county_name)

        self.assertTrue(isinstance(haz_dates, list))
        self.assertTrue(isinstance(haz_dates_offset, list))
        self.assertTrue(isinstance(vh_dates, list))
        self.assertTrue(isinstance(vh_dates_offset, list))

    def test_one_shot_subset_air_quality(self):
        """
        One shot test for subset_air_quality function.
        Returns true if function lists match result_ variable.
        """
        data = {'Date': ['09-15-2020', '09-20-2020', '08-15-2020', '09-10-2020'],
                'AQI_Category': ['Hazardous', 'Very Unhealthy', 'Good', 'Very Unhealthy'],
                'County': ['Baker', 'Baker', 'Baker', 'Clackamas']}
        aq_data = pd.DataFrame(data, columns=['Date', 'AQI_Category', 'County'])
        aq_data['Date'] = pd.to_datetime(aq_data['Date'])
        county_name = 'Baker'
        haz_dates, haz_dates_offset, vh_dates, vh_dates_offset = af.subset_air_quality(
            aq_data, county_name)
        result_haz_dates = ['2020-09-15']
        result_haz_dates_offset = ['2020-09-16']
        result_vh_dates = ['2020-09-20']
        result_vh_dates_offset = ['2020-09-21']

        self.assertTrue(result_haz_dates == haz_dates)
        self.assertTrue(result_haz_dates_offset == haz_dates_offset)
        self.assertTrue(result_vh_dates == vh_dates)
        self.assertTrue(result_vh_dates_offset == vh_dates_offset)

    def test_edge_subset_air_quality(self):
        """
        Edge test for subset_air_quality function.
        Returns true if the function raises a value error
        when dataframe is missing a county column.
        """
        data = {'Date': ['09-15-2020', '09-20-2020', '08-15-2020', '09-10-2020'],
                'AQI_Category': ['Hazardous', 'Very Unhealthy', 'Good', 'Very Unhealthy'],
                'County': ['Baker', 'Baker', 'Baker', 'Clackamas']}
        aq_data = pd.DataFrame(data, columns=['Date', 'AQI_Category'])
        aq_data['Date'] = pd.to_datetime(aq_data['Date'])
        county_name = 'Baker'
        with self.assertRaises(ValueError):
            af.subset_air_quality(
                aq_data, county_name)

    def test_edge2_subset_air_quality(self):
        """
        Edge test for subset_air_quality function.
        Returns true if the function raises a value error
        when dataframe is missing a EPA catergory column.
        """
        data = {'Date': ['09-15-2020', '09-20-2020', '08-15-2020', '09-10-2020'],
                'AQI_Category': ['Hazardous', 'Very Unhealthy', 'Good', 'Very Unhealthy'],
                'County': ['Baker', 'Baker', 'Baker', 'Clackamas']}
        aq_data = pd.DataFrame(data, columns=['Date', 'County'])
        aq_data['Date'] = pd.to_datetime(aq_data['Date'])
        county_name = 'Baker'
        with self.assertRaises(ValueError):
            af.subset_air_quality(
                aq_data, county_name)


if __name__ == '__main__':
    unittest.main()
