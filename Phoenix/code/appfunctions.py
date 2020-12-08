
"""
Contains functions for manipulating data used in the Phoenix app.
Functions:
    1) subset_date: given a month and a day,
        subsets dataframe to only those dates.

"""

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
