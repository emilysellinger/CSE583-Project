'''
Assign counties and aqi category to air quality data for use in dash app.

Functions:

    assign_aqicat(data)
'''

# Import packages
import pandas as pd

# import air quality and county data

air_quality = pd.read_csv("https://raw.githubusercontent.com/emilysellinger/Phoenix.github.io/main/phoenix/data/Daily_Avg_PM2.5_Location.csv")  # noqa
air_quality.head()
station_counties = pd.read_csv("https://raw.githubusercontent.com/emilysellinger/Phoenix.github.io/main/phoenix/data/ORAQ_StationCounties.csv")  # noqa
station_counties.head()

# Assign county values to air quality station readings by shared name
aq = air_quality.join(station_counties.set_index('Name'), on='Name')
aq.head()

# Calculate mean daily PM2.5 reading for counties with multiple stations
cols = ['Date', 'County']
county_aq = aq.groupby(cols, as_index=False)['Avg_PM2.5'].mean()
county_aq.head()

# Assign PM2.5 values for counties without stations to nearest county
# and append to dataframe with county means.
coos = county_aq[county_aq['County'] == 'Douglas']
coos = coos.replace(['Douglas'], 'Coos')
curry = county_aq[county_aq['County'] == 'Josephine']
curry = curry.replace(['Josephine'], 'Curry')
malheur = county_aq[county_aq['County'] == 'Harney']
malheur = malheur.replace(['Harney'], 'Malheur')
morrow = county_aq[county_aq['County'] == 'Umatilla']
morrow = morrow.replace(['Umatilla'], 'Morrow')
gilliam = county_aq[county_aq['County'] == 'Umatilla']
gilliam = gilliam.replace(['Umatilla'], 'Gilliam')
wheeler = county_aq[county_aq['County'] == 'Grant']
wheeler = wheeler.replace(['Grant'], 'Wheeler')
sherman = county_aq[county_aq['County'] == 'Wasco']
sherman = sherman.replace(['Wasco'], 'Sherman')
hood_river = county_aq[county_aq['County'] == 'Wasco']
hood_river = hood_river.replace(['Wasco'], 'Hood River')
columbia = county_aq[county_aq['County'] == 'Washington']
columbia = columbia.replace(['Washington'], 'Columbia')
clatsop = county_aq[county_aq['County'] == 'Washington']
clatsop = clatsop.replace(['Washington'], 'Clatsop')
tillamook = county_aq[county_aq['County'] == 'Washington']
tillamook = tillamook.replace(['Washington'], 'Tillamook')
yamhill = county_aq[county_aq['County'] == 'Washington']
yamhill = yamhill.replace(['Washington'], 'Yamhill')
polk = county_aq[county_aq['County'] == 'Marion']
polk = polk.replace(['Marion'], 'Polk')
lincoln = county_aq[county_aq['County'] == 'Benton']
lincoln = lincoln.replace(['Benton'], 'Lincoln')
or_counties = county_aq.append([coos, curry, malheur, morrow,
                               gilliam, wheeler, sherman, hood_river,
                               columbia, clatsop, tillamook, yamhill,
                               polk, lincoln])


def assign_aqicat(data):
    '''
    Returns a dataset of PM2.5 values with categorical AQI ratings assigned.

        Parameters:
                data (array): Dataframe with column of daily avg PM2.5 values

        Returns:
                data (array): Dataframe with AQI ratings appended as new column
    '''
    if data['Avg_PM2.5'].dtype != 'float64':
        raise ValueError("Provided PM 2.5 ratings are not floating point values")

    aqi_cat = []

    for row in data['Avg_PM2.5']:
        if row >= 250.5:
            aqi_cat.append('Hazardous')
        elif row >= 150.5:
            aqi_cat.append('Very Unhealthy')
        elif row >= 55.5:
            aqi_cat.append('Unhealthy')
        elif row >= 35.5:
            aqi_cat.append('Unhealthy for Sensitive Groups')
        elif row >= 12.1:
            aqi_cat.append('Moderate')
        elif row < 12.1:
            aqi_cat.append('Good')
        else:
            aqi_cat.append('NA')
    data['AQI_Category'] = aqi_cat
    return data


# Can use the following code to append AQI categories
# to county daily PM2.5 dataframe and download that dataframe as csv.
# assign_aqicat(or_counties)
# or_counties.to_csv("../data/OR_DailyAQ_byCounty.csv")
