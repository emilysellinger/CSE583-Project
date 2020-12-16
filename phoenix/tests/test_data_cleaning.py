"""
Unittests for functions to add categorical AQI assignment to air quality data.
"""

# Import packages
import unittest
import phoenix.code.data_cleaning as dc
import pandas as pd

class TestDataCleaning(unittest.TestCase):
	"""
	Contains test cases for data cleaning.
	"""

	def test_smoke_assign_aqicat(self):
		"""
		Smoke test for assign_aqicat function.
		Returns: True if function produces data frame.
		"""
		data = {'Avg_PM2.5':[8.4,17.3,39,76.2,204.9,360.8]}
		data = pd.DataFrame(data, columns=['Avg_PM2.5'])

		self.assertTrue(
				isinstance(dc.assign_aqicat(data
				), pd.DataFrame))

	def test_oneshot_assign_aqicat(self):
		"""
		One shot test for assign_aqicat.
		Returns true if resulting dataframe is equal to data_result.
		"""
		data = {'Avg_PM2.5':[8.4]}
		data = pd.DataFrame(data, columns=['Avg_PM2.5'])
		data_result = {'Avg_PM2.5': [8.4],
                       'AQI_Category': ['Good']}
		data_result = pd.DataFrame(data_result, columns=['Avg_PM2.5', 'AQI_Category'])
		data_test = dc.assign_aqicat(data)

		self.assertTrue(data_test.equals(data_result))

	def test_edgetest_assign_aqicat(self):
		"""
		Edge test for assign_aqicat function.
		Returns true if a Value Error is raised.
		"""
		data = {'Avg_PM2.5':['good']}
		data = pd.DataFrame(data, columns=['Avg_PM2.5'])

		with self.assertRaises(ValueError):
			dc.assign_aqicat(data)

if __name__ == '__main__':
    unittest.main()