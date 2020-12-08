"""
Unittests for Phoenix
#ADD MORE HERE LATER
"""
import unittest

from code import app_functions

import pandas as pd


class TestPhoenix(unittest.TestCase):
    """
    Contains test cases for Phoenix
    """

    def smoke_test_app_functions(self):
        """
        Smoke test for subset_date function.
        Returns: True if function produces a data frame
        """
        data = {'observation date': ['08-01-2020', '09-01-2020',
                '10-01-2020', '11-01-2020'],
                'species': ['American Crow', 'American Crow',
                            'American Crow', 'American Crow']}
        bird_data = pd.DataFrame(data, columns=['observation date', 'species'])
        month = 'August'
        day = 1

        self.assertTrue(
                isinstance(app_functions.subset_date(
                    bird_data, 'observation date', month, day),
                    pd.DataFrame))

    def one_shot_test_app_functions(self):
        """
        One shot test for subset_data function.
        Returns true if resulting dataframe is equal to data_result.
        """

        data = {'observation date': ['08-01-2020', '09-01-2020',
                '10-01-2020', '11-01-2020'],
                'species': ['American Crow', 'American Crow',
                            'American Crow', 'American Crow']}
        bird_data = pd.DataFrame(data, columns=['observation date', 'species'])
        month = 'August'
        day = 1
        data_result = {'observation date': ['08-01-2020'],
                       'species': ['American Crow']}
        data_result = pd.DataFrame(data_result,
                                   columns=['observation date', 'species'])

        self.assertEqual(
            app_functions.subset_date(
                bird_data, 'observation date', month, day
            ),
            data_result
        )

    def edgetest_app_functions(self):
        """
        Edge test for subset_data function.
        Returns true if a Value Error is raised.
        """
        data = {'observation date': ['08-01-2020', '09-01-2020',
                '10-01-2020', '11-01-2020'],
                'species': ['American Crow', 'American Crow',
                            'American Crow', 'American Crow']}
        bird_data = pd.DataFrame(data, columns=['observation date', 'species'])
        month = 'August'
        day = 5

        with self.assertRaises(ValueError):
            app_functions.subset_date(
                bird_data, 'observation date', month, day)


suite = unittest.TestLoader().loadTestsFromTestCase(TestPhoenix)
_ = unittest.TextTestRunner().run(suite)


if __name__ == '__main__':
    unittest.main()
