
"""
Contains functions for manipulating data used in the phoenix app.
Functions:
    1) subset_date: given a month and a day,
        subsets dataframe to only those dates.
    2) subset_air_quality: given a county, creates lists of dates,
        and day after of very unhealhty and hazardous air quality.

"""

import pandas as pd

# variables

months = [8, 9, 10, 11, 12]
full_months = ['August', 'September', 'October', 'November', 'December']


def subset_date(data_frame, df_date, month, day):
    """
    Subsets the dataframe based on the month and day selected.

    Args:
        df (dataframe): dataframe to be subset
        df_date (str): name of column that holds datetime values
        month(str): month of interest
        day (int): day of interest

    Returns:
        new_df (dataframe): subsetted dataframe
    Raises:
        ValueError: There are no observations for this date
    """

    month_index = [
        idx for idx,
        element in enumerate(full_months) if element == month]
    new_df = data_frame.loc[data_frame[
                            df_date].dt.month == months[month_index[0]]]
    new_df = new_df.loc[new_df[df_date].dt.day == day]

    if new_df.empty:
        raise ValueError('There are no observations for this date')

    return new_df


def subset_air_quality(df, county_name):
    """
    Subsets AQ dataframe based on the county and the AQI category.

    Args:
        df (pandas dataframe): air quality dataframe to be subset
        county_name (str): name of county selected from dropdown
    Returns:
        haz_dates (list): list of dates with hazardous air quality
        haz_dates_offset (list): day after the day with hazardous air quality
        vh_dates (list): list of dates with very unhealthy air quality
        vh_dates_offset (list): day after day with very unhealthy air quality
    """
    if 'County' not in df.columns:
        raise ValueError('Air quality data is missing county information')
    if 'AQI_Category' not in df.columns:
        raise ValueError('Air quality data is missing EPA Categories')

    vh_aq = df.loc[df['AQI_Category'] == 'Very Unhealthy']
    haz_aq = df.loc[df['AQI_Category'] == 'Hazardous']
    sub_vh_aq = vh_aq.loc[vh_aq['County'] == county_name].copy()
    sub_haz_aq = haz_aq.loc[haz_aq['County'] == county_name].copy()
    sub_vh_aq['Date offset'] = sub_vh_aq['Date'] + pd.DateOffset(days=1)
    sub_haz_aq['Date offset'] = sub_haz_aq['Date'] + pd.DateOffset(days=1)

    haz_dates = []
    for date in sub_haz_aq['Date']:
        new_date = str(date)
        new_date = new_date.split()
        new_date = new_date[0]
        haz_dates.append(new_date)

    haz_dates_offset = []
    for date in sub_haz_aq['Date offset']:
        new_date = str(date)
        new_date = new_date.split()
        new_date = new_date[0]
        haz_dates_offset.append(new_date)

    vh_dates_offset = []
    for date in sub_vh_aq['Date offset']:
        new_date = str(date)
        new_date = new_date.split()
        new_date = new_date[0]
        vh_dates_offset.append(new_date)

    vh_dates = []
    for date in sub_vh_aq['Date']:
        new_date = str(date)
        new_date = new_date.split()
        new_date = new_date[0]
        vh_dates.append(new_date)

    return haz_dates, haz_dates_offset, vh_dates, vh_dates_offset
