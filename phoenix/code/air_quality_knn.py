"""A k-nearest-neighbors regression algorithm that provides
air quality estimates for GPS locations between observation
stations from the Oregon air quality dataset.
Uses the Scikit Learn KNN method.

Functions:

air_quality_knn(air_quality, ebd_data)
    -- Performs a 5-neighbor knn for air quality on each day
    at the locations specified by the observations in the
    eBird data.

verify_location(coordinates)
    -- Performs a check that the inputted gps coordinates
    roughly fall within the state of Oregon.
"""

import warnings
import pandas as pd
import numpy as np


from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler


def air_quality_knn(air_quality, ebd_data):

    """
    Performs knn for the given data around a query point.
    Each query point has a location and a date for which
    the air quality is to be calculated.

    Args:
        air_quality_data (pandas dataframe): full air quality
            dataset for the state of Oregon. Listed below are
            the relevant columns.
            (Date, Latitude, Longitude, Avg_PM2.5)

        ebd_data (pandas dataframe): full eBird observation
            dataset for the state of Oregon. Listed below
            are the relevant columns.
            (observation date, latitude, longitude)
            These are the points for which the k-nearest-neighbors
            are to be found.

    Returns:
        ebd_data (pandas dataframe): the inputted dataset with an
            additional column 'Avg_PM2.5' that gives the air quality
            for an observation.

    Warnings:
        'NaN produced: <5 neighbors for (day)'
            Days for which there may be fewer than 5 air quality
            observations will yield NaN values.

    Raises:
        TypeError: If the input data are not both pandas DataFrames.
        ValueError: If the inputs are swapped or the column naming
            is incorrect.

    """

    # Verify correct input type, raise TypeError if not
    air_is_df = isinstance(air_quality, pd.DataFrame)
    bird_is_df = isinstance(ebd_data, pd.DataFrame)

    if not air_is_df or not bird_is_df:
        raise TypeError("Incorrect data type. Must be pandas DataFrame.")

    # More informatively, verify correct input order and raise
    # exception if they might be switched or have incorrect
    # column names. (Just using two important ones as indicators)
    categ_in_air = 'Date' in air_quality
    tax_in_birds = 'taxonomic order' in ebd_data

    if not categ_in_air or not tax_in_birds:
        raise ValueError("Input order may be reversed, otherwise check column names")

    # Convert the air-quality dates to datetime format and
    # remove the data points that occur after September to match
    # the eBird data.
    air_quality['Date'] = pd.to_datetime(air_quality['Date'])
    months = [10, 11, 12]
    air_quality = air_quality[-air_quality['Date'].dt.month.isin(months)]

    # Reduce the dataframe to only the relevant columns:
    # ['Date', 'Latitude', 'Longitude', 'Avg_PM2.5']
    air_quality_data = air_quality[['Date', 'Latitude',
                                    'Longitude', 'Avg_PM2.5']]

    # Verify that the air quality observations are in Oregon
    verify_location(air_quality_data[['Latitude', 'Longitude']])

    # Remove NaN values from the air quality data
    air_quality_data = air_quality_data[air_quality_data['Avg_PM2.5'].notna()]

    # Also convert eBird dates to datetime format for compatibility.
    ebd_data['observation date'] = pd.to_datetime(ebd_data['observation date'])

    # Verify that the bird observations are in Oregon
    verify_location(ebd_data[['latitude', 'longitude']])

    # Initialize a column in the eBird dataframe to hold the air
    # quality measure for each observation.
    ebd_data['Avg_PM2.5'] = np.nan

    # Now iterate over each day that the data describes, creating
    # a separate knn for each. This will allow us to estimate air
    # quality for a certain location on a certain day.
    for day in air_quality_data['Date'].unique():

        # Define the 'training' data: the observed air quality
        # at the station locations on the respective day.
        air_today = air_quality_data[air_quality_data['Date'] == day]
        x_train = air_today[['Latitude', 'Longitude']]
        y_train = air_today['Avg_PM2.5']

        # Skip over days when there aren't enough air quality points
        # to produce 5 nearest neighbors.
        if len(air_today['Latitude']) < 5:
            date = pd.to_datetime(day).date()
            warnings.warn(f"NaN produced: <5 neighbors for {date}")
            continue
        else:
            pass

        # Define the 'test' or 'query' data: the locations of
        # the bird observations on the respective day.
        birds_today = ebd_data[ebd_data['observation date'] == day]
        x_test = birds_today[['latitude', 'longitude']]

        # Skip over this day if there aren't any bird observations.
        if birds_today.empty is True:
            continue
        else:
            pass

        # Normalize and fit the location data to ensure proper scaling.
        scaler = StandardScaler()
        scaler.fit(x_train)

        x_train_norm = scaler.transform(x_train)
        x_test_norm = scaler.transform(x_test)

        # Perform k-nearest-neighbors regression on continuous data.
        regressor = KNeighborsRegressor(n_neighbors=5)
        regressor.fit(x_train_norm, y_train)

        # Output the air quality predictions for the locations of the
        # bird observations on this day, maintaining the indexing from
        # the original dataset.
        y_pred = regressor.predict(x_test_norm)

        y_pred = pd.DataFrame(y_pred, columns=['Avg_PM2.5'])
        y_pred = y_pred.set_index(x_test.index)

        # Finally, add these outputs to the dataset to get the air quality
        # at the day and location of the bird observation.
        ind = x_test.index[:].tolist()
        ebd_data.loc[ind, 'Avg_PM2.5'] = y_pred

    # Return the whole eBird dataset with new column for air quality.
    return ebd_data


def verify_location(coordinates):

    """
    Performs a simple check of all gps coordinates found in inputs.
    If a (latitude,longitude) pair is not found within the (rough)
    range of the state of Oregon, a ValueError is raised.

    Args:
        coordinates (pandas dataframe): contains two columns, first
            one for latitude, the other for longitude.

    Returns:
        None. This function simply raises warnings then passes.

    Warnings:
        'Coordinate not in Oregon': 
            If any gps coordinates in the data do not fall
            within the predetermined (lat,long) extremes of Oregon.
    """
    coordinates.columns = coordinates.columns.str.lower()

    # Verify that all air quality locations are (roughly) within Oregon
    for ind in coordinates.index:
        lat = coordinates.at[ind, 'latitude']
        long = coordinates.at[ind, 'longitude']

        if 40 <= lat <= 47 and -125 <= long <= -115:
            pass
        else:
            warnings.warn(f"Coordinate not in Oregon at index: {ind}")
