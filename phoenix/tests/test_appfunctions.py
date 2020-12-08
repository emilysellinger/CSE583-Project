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

    def test_smoke_app_functions(self):
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

    def test_one_shot_app_functions(self):
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

    def test_edgetest_app_functions(self):
        """
        Edge test for subset_data function.
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


if __name__ == '__main__':
    unittest.main()
