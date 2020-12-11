"""
Unittests for the k-nearest-neighbors function (air_quality_knn.py)
and associated verify_location function that jointly work
to output air quality estimates for each bird observation.
"""
import unittest
import pandas as pd
import numpy as np

from phoenix.code import air_quality_knn as knn


class Testairqualityknn(unittest.TestCase):
    """
    Contains test cases for air_quality_knn
    """

    def setUp(self):

        # Set up bare-bones bird observation data
        bird_data_example = {
            'taxonomic order': [20638, 21132, 20703, 529, 11284,
                                20353, 20558, 297, 10805, 602],

            'common name': ['American Crow', 'Black-capped Chickadee',
                            'Common Raven', 'Green-winged Teal',
                            'Northern Flicker', 'Stellers Jay',
                            'Black-billed Magpie', 'Canada Goose',
                            'Downy Woodpecker', 'Lesser Scaup'],

            'observation count': [1, 5, 10, 2, 5, 1, 3, 14, 7, 1],

            'county': ['Baker', 'Baker', 'Coos', 'Hood River',
                       'Baker', 'Lane', 'Linn', 'Marion',
                       'Marion', 'Polk'],

            'latitude': [44.9274024, 44.7792552, 43.154114,
                         45.717025, 44.9274024, 44.070449,
                         44.7823649, 44.8938248, 44.8318405,
                         44.825075],

            'longitude': [-117.1194828, -117.8320175, -124.398644,
                          -121.525898, -117.1194828, -123.1747973,
                          -122.6085624, -123.0744322, -123.0037897,
                          -123.615491],

            'observation date': ['2020-09-21', '2020-09-01', '2020-09-10',
                                 '2020-09-05', '2020-09-20', '2020-09-18',
                                 '2020-09-08', '2020-09-02', '2020-09-09',
                                 '2020-09-30']
                            }

        # Set up (somewhat) shortened air quality data
        air_data = pd.read_csv('phoenix/data/Daily_Avg_PM2.5_Location.csv').iloc[::4, :]

        self.bird_data_example = pd.DataFrame(bird_data_example)
        self.air_data = air_data

    def test_initialize_new_column(self):
        """
        Smoke test, whether the knn function initializes new column to
        hold the new data points.

        Asserts: True if function adds 'Avg_PM2.5' column to output dataframe
        """

        birds_air_quality = knn.air_quality_knn(self.air_data, self.bird_data_example)

        self.assertTrue(('Avg_PM2.5' in birds_air_quality.columns))

    def test_verify_location(self):
        """
        Tests whether the verify_location function will correctly handle
        a gps coordinate that is outside of the range of the state of Oregon.

        Asserts: Raises ValueError if the gps coordinate lies outside of OR
        """

        bad_location_birds = self.bird_data_example[['latitude', 'longitude']]
        bad_location_birds.at[0, 'latitude'] = 30

        with self.assertRaises(ValueError):
            knn.verify_location(bad_location_birds)

    def test_invalid_input_order(self):
        """
        Tests that the knn function will correctly handle incorrect input order.

        Asserts: Raises ValueError if a unique column name for each dataframe
            does not appear in the correct input.
        """

        with self.assertRaises(ValueError):
            knn.air_quality_knn(self.bird_data_example, self.air_data)

    def test_invalid_input_type(self):
        """
        Tests that the user gives the input in the correct format for knn

        Asserts: Raises TypeError if the inputs are not pandas DataFrames
        """

        air_arr = np.array([1, 2, 3, 4])
        bird_list = ['One Bird', 'Two Bird', 'Redwing', 'Blackbird?']

        with self.assertRaises(TypeError):
            knn.air_quality_knn(air_arr, bird_list)

    def test_knn_bounds(self):
        """
        Tests that an output from the knn function is within the range of
        observed air quality values for that day. Essentially checks that
        knn isn't producing an impossible value.

        Asserts: True if function outputs a Avg_PM2.5 that falls within the
            range found in the training data for that day.
        """

        within_range = True
        birds_air_quality = knn.air_quality_knn(self.air_data, self.bird_data_example)

        for ind in birds_air_quality.index:
            day = birds_air_quality.at[ind, 'observation date']
            aq_day = self.air_data[self.air_data['Date'] == day]
            aq_day = aq_day[aq_day['Avg_PM2.5'].notna()]

            min_air_obs = min(aq_day['Avg_PM2.5'])
            max_air_obs = max(aq_day['Avg_PM2.5'])

            if min_air_obs <= birds_air_quality.at[ind, 'Avg_PM2.5'] <= max_air_obs:
                pass
            else:
                within_range = False

        self.assertTrue(within_range)

    def test_knn_correct(self):
        """
        Zooms in a little closer than the previous test to check the
        accuracy of output from the knn. Uses a different method to
        calculate (without normalizing) and checks whether the function's
        output is within 25% of this simplified version.

        Asserts: True if this ('manual') version of knn outputs
            Avg_PM2.5 values that capture the function's output
            within plus or minus 25%.
        """

        manual_knn = pd.DataFrame(columns=['Avg_PM2.5'])
        manual_knn = manual_knn.fillna(0)

        for ind in self.bird_data_example.index:
            day = self.bird_data_example.at[ind, 'observation date']
            aq_day = self.air_data[self.air_data['Date'] == day]
            aq_day = aq_day[aq_day['Avg_PM2.5'].notna()]
            aq_day = aq_day.reset_index()

            query = self.bird_data_example[['latitude', 'longitude']]
            query = query.loc[ind]
            query = np.reshape(query.values, (1, 2))

            diffs = aq_day[['Latitude', 'Longitude']].values - query

            diffs_sq = np.square(diffs)

            sum_diffs_sq = diffs_sq.sum(axis=1)

            ordered_array = sorted(enumerate(sum_diffs_sq), key=lambda x: x[1])

            sum_labels = 0

            for i in range(0, 5):
                sum_labels = sum_labels + aq_day.at[ordered_array[i][0], 'Avg_PM2.5']

            mean_label = sum_labels/5
            manual_knn.at[ind, 'Avg_PM2.5'] = mean_label

        birds_air_quality = knn.air_quality_knn(self.air_data, self.bird_data_example)
        birds_knn = birds_air_quality['Avg_PM2.5'].to_frame()

        knn_diffs = birds_knn.add(-manual_knn).abs()

        self.assertTrue(all(knn_diffs.le(0.25*birds_knn)))


if __name__ == '__main__':
    unittest.main()
