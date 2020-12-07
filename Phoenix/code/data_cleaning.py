import pandas as pd
air_quality = pd.read_csv("../data/Daily_Avg_PM2.5_Location.csv")
air_quality.head()

station_counties = pd.read_csv("../data/ORAQ_StationCounties.csv")
station_counties.head()

aq = air_quality.join(station_counties.set_index('Name'), on='Name')
aq.head()

cols = ['Date', 'County']
county_aq = aq.groupby(cols, as_index=False)['Avg_PM2.5'].mean()
county_aq.head()

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
or_counties = county_aq.append([coos, curry, malheur, morrow, gilliam, wheeler, sherman, hood_river,
                               columbia, clatsop, tillamook, yamhill, polk, lincoln])


def assign_aqicat(data):
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


assign_aqicat(or_counties)
or_counties.to_csv("../data/OR_DailyAQ_byCounty.csv")
