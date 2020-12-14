"""
This module encodes a dash app for non-experts to examine
patterns in bird sightings and air quality in Oregon.
"""

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from urllib.request import urlopen
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

from flask_caching import Cache

from phoenix.code.appfunctions import subset_date, subset_air_quality

# Initialize Dash App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

# Initialize Cache
CACHE_CONFIG = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache',
    'CACHE_DEFAULT_TIMEOUT': 180
}

cache = Cache(app.server, config=CACHE_CONFIG)

# Read in and clean data
months = [6, 7, 8, 9]


@cache.cached(key_prefix='county_map')
def get_county_map():
    """
    Fetches the Oregon County geojson file for mapping

    Args: None

    Returns:
        counties1 (geojson): Oregon county map file from repo
    """
    print("Retrieving Oregon County Map...")
    with urlopen('https://raw.githubusercontent.com/emilysellinger/Phoenix/main/phoenix/data/Oregon_counties_map.geojson') as response:# noqa
        counties1 = json.load(response)
    return counties1


counties = get_county_map()


@cache.cached(key_prefix='aq_data')
def get_aq_data():
    """
    Fetches the Oregon air quality data and filters data based on
    relevant month and valid air quality entry

    Args: None

    Returns:
        aq1 (pd dataframe): Cleaned air quality data from repo
    """
    print("Retrieving Air Quality County Data...")

    aq1 = pd.read_csv('phoenix/data/OR_DailyAQ_byCounty.csv')

    aq1['Date'] = pd.to_datetime(aq1['Date'])
    aq1 = aq1.loc[aq1['Date'].dt.month.isin(months)]
    aq1 = aq1[aq1['Avg_PM2.5'].notna()]

    return aq1


aq = get_aq_data()


@cache.cached(key_prefix='bird_data')
def get_bird_data():
    """
    Fetches the full Oregon eBird dataset and filters data based on
    relevant columns and months

    Args: None

    Returns:
        bird1 (pd dataframe): Cleaned eBird data from repo
    """

    print("Retrieving Bird Data...")
    bird1 = pd.read_csv("phoenix/data/ebird_app_data.csv")
    bird1['observation date'] = pd.to_datetime(bird1['observation date'])
    bird1 = bird1.loc[bird1['observation date'].dt.month.isin(months)]

    return bird1


bird = get_bird_data()

# Get categories for dropdowns
category_labels = pd.read_csv("phoenix/data/category_labels.csv")

common_names = category_labels['species']
county_names = category_labels['county'].unique()
family_names = category_labels['family'].unique()
full_months = ['June', 'July', 'August', 'September']

# Configure the style and layout of the app (including headings etc)
app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[
        html.Div([
            html.Div([
                "Family:",
                dcc.Dropdown(
                    id='family',
                    options=[{'label': i, 'value': i} for i in family_names],
                    value=['Corvidae (Crows, Jays, and Magpies)'],
                    multi=True
                )
            ], style={'width': '21%'}, className="three columns"),

            html.Div([
                "Species:",
                dcc.Dropdown(
                    id='species',
                    value=['American Crow'],
                    multi=True
                ),

                html.Div(id='dd-output-container',
                         style={'width': '10%',
                                'margin-left': 0})
            ], className="two columns")
        ], style={'margin-bottom': 20, 'margin-left': 40}, className="row"),

        html.Div([
            html.Div([
                "Month:",
                dcc.Dropdown(
                    id='month',
                    options=[{'label': i, 'value': i} for i in full_months],
                    value='September'
                ),

                html.Div(id='dd2-output-container',
                         style={'width': '8%',
                                'margin-left': 0
                                })
            ], style={'width': '8%'}, className="two columns"),

            html.Div([
                "Day:",
                dcc.Slider(
                    id='day-slider',
                    min=1,
                    value=1,
                    step=1),
                html.Div(id='slider-output-container')
            ], className="four columns"),

            html.Div([
                "Graph:",
                dcc.RadioItems(
                    id='species/family/order',
                    options=[
                        {'label': 'Species', 'value': 'common name'},
                        {'label': 'Family', 'value': 'family'},
                        {'label': 'Order', 'value': 'order'}
                    ],
                    value='common name',
                    labelStyle={'display': 'inline-block'}
                )
            ], style={'margin-left': 160}, className="three columns offset-by-one"),

            html.Div([
                "County:",
                dcc.Dropdown(
                    id='county-names',
                    options=[{'label': i, 'value': i} for i in county_names],
                    value='Multnomah'),
            ], style={'width': '15%', 'margin-left': -90}, className="two columns")

        ], style={'margin-left': 40}, className="row"),

        html.Div([
            html.Div(
                id='day-indicator',
                style={'color': colors['text'], 'margin-top': 10}, 
                className="five columns offset-by-two"),
        ], className="row"),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='aq-map',
                    style={'width': '90vh', 'height': '60vh'}),
                html.Div(id='graph-output',
                         style={'margin-left': 20, 'backgroundColor': colors['background'],
                                'color': colors['text']})
            ], className="six columns"),

            html.Div([
                dcc.Graph(
                    id='bird-counts',
                    style={'width': '90vh', 'height': '60vh'}),
            ], style={'margin-left': -5}, className="six columns")
        ], className="row")
    ]
)


# Callbacks - Interactive Components
# Plotting on Choropleth Map
@app.callback(
    Output('aq-map', 'figure'),
    Input('species', 'value'),
    Input('month', 'value'),
    Input('day-slider', 'value'))
@cache.memoize(timeout=360)
def update_aq_graph(species, month, day_slider):
    """
    Creates an air quality choropleth map depending on the species,
    month, and day selected in the app. Bird sightings for selected
    species are plotted as a scatter plot over air quality choropleth.
    Args:
        species(str): common name selected from dropdown
        month(str): name of month selected from dropdown
        day_slider(int): day value from slider
    Returns:
        Air Quality Choropleth map with bird sightings overlayed
    """

    aq_map_choropleth = render_map(month, day_slider)

    if isinstance(species, str):
        sub_bird = bird.loc[bird['common name'] == species]
    else:
        sub_bird = bird.loc[bird['common name'].isin(species)]

    try:
        sub_bird = subset_date(sub_bird, 'observation date', month, day_slider)

        if sub_bird['observation count'].max() < 1500:
            maxsize = sub_bird['observation count'].max()/6
        else:
            maxsize = 250

        aq_map_scatter = px.scatter_mapbox(
            sub_bird, lat='latitude', lon='longitude',
            size='observation count',
            size_max=maxsize,
            zoom=5, color_discrete_sequence=['#EF553B'],
            mapbox_style="carto-positron",
            center={"lat": 44.14495826303137, "lon": -120.60278690370761}
        )
        aq_map_choropleth.add_trace(aq_map_scatter.data[0])

    except ValueError:
        pass
    return aq_map_choropleth

# Separate callback for updating the county aq map
@cache.memoize(timeout=360)
def render_map(month, day):
    """
    Secondary function that actually does the choropleth map creation.
    This is subsetting for caching purposes: if the day input does not
    change but the species does, the map will not have to be created
    from scratch again.

    Args:
        month (str): month input from the 'month' dropdown
        day (int): day input from the 'day' slider

    Returns:
        aq_map(choropleth_mapbox): map with county-level air quality data
    """
    print("Updating AQ Map...")
    sub_aq = subset_date(aq, 'Date', month, day)

    aq_map = px.choropleth_mapbox(
            sub_aq, geojson=counties,
            featureidkey='properties.altname', locations="County",
            color="Avg_PM2.5", hover_name="County",
            color_continuous_scale=px.colors.sequential.Turbo,
            range_color=(0, 300),
            mapbox_style='carto-positron', zoom=5,
            center={"lat": 44.14495826303137, "lon": -120.60278690370761},
            opacity=0.5,
            labels={'Avg_PM2.5': 'Average PM 2.5'}
            )

    return aq_map


# adding indicator of the day of the month
@app.callback(
    Output('day-indicator', 'children'),
    Input('month', 'value'),
    Input('day-slider', 'value'))
def display_date_aq(month, day_slider):
    """
    Displays the date that was selected using text.
    Args:
        month(str): selected month from dropdown
        day_slider(int): selected day from slider
    Returns:
        Date text (str): full text of selected date
    """
    return str(month) + ' ' + str(day_slider) + ', 2020'


# Setting slider day values based on month
@app.callback(
    Output('day-slider', component_property='max'),
    Output('day-slider', component_property='marks'),
    Input('month', 'value'))
def set_days_in_month(month_picked):
    """
    Changes the values in the slider based on how many days are
    in the month selected.

    Args:
        month_picked (str): month June through Sept
    Returns:
        days (int): number of days in that month
        marks (dict): dictionary of day intervals for corresponding tick
            marks on the slider
    """
    if month_picked in ['July', 'August']:
        days = 31
        marks = {1: '1', 10: '10', 20: '20', 31: '31'}
    else:
        days = 30
        marks = {1: '1', 10: '10', 20: '20', 30: '30'}

    return days, marks


# Setting species selection by family chosen
@app.callback(
    Output('species', 'options'),
    Input('family', 'value'))
def set_species_options(family_picked):
    """
    Filters the species dropdown based on the input in the family dropdown

    Args:
        family_picked (list): all families chosen by the family dropdown
    Returns:
        dict_species_list (dictionary): dictionary of matching labels and values
        for all of the species that fall under the selected families
    """
    if family_picked == []:
        species_list = common_names
    else:
        species_list = category_labels.loc[category_labels['family'].isin(family_picked), 'species']
    dict_species_list = [{'label': i, 'value': i} for i in species_list]
    return dict_species_list


# Bird Count Line Graph
@app.callback(
    Output('bird-counts', 'figure'),
    Input('county-names', 'value'),
    Input('species/family/order', 'value'))
def update_count_graph(county_name, taxon):
    """
    Displays a chart with the counts of birds by species for selected county.
    Args:
        county_name (str): selected county from dropdown
    Returns:
        count_plot (figure): plot of bird observations over time with AQI category
    """
    if isinstance(county_name, str):
        sub_bird_county = bird.loc[bird['county'] == county_name]
        # reformat to a list to keep consistent when subsetting later
        county_name = [county_name]
    else:
        sub_bird_county = bird.loc[bird['county'].isin(county_name)]

    haz_dates, haz_dates_offset, vh_dates, vh_dates_offset = subset_air_quality(aq, county_name)

    count_plot = plot_bird_obs(sub_bird_county, taxon)

    for count, ele in enumerate(haz_dates):
        count_plot.add_vrect(x0=haz_dates[count], x1=haz_dates_offset[count],
                             fillcolor="OrangeRed", opacity=0.5, layer="below", line_width=0)

    for count, ele in enumerate(vh_dates):
        count_plot.add_vrect(x0=vh_dates[count], x1=vh_dates_offset[count],
                             fillcolor="Gold", opacity=0.5,
                             layer="below", line_width=0)

    return count_plot


def plot_bird_obs(bird_df, taxonomy):
    """
    Subsetted function that does the actual plotting for the bird count graph.
    Selects data to plot based on the input of the species/family/order
    RadioItem, and sums observation count across like taxonomic resolution.

    Args:
        bird_df (pd dataframe): bird data filtered by county selected
        taxonomy (str): "common name", "family", or "order" based on what the
            user selects
    Returns:
        plot_birds (scatter): scatter plot of bird observations against date
    """
    summed_obs = bird_df.groupby([taxonomy, 'observation date'])['observation count'].sum()
    summed_obs_df = summed_obs.to_frame().reset_index()

    plot_birds = px.scatter(
        summed_obs_df, x='observation date',
        y='observation count', color=taxonomy,
        labels={taxonomy: "species", "observation date": "Date",
                          "observation count": "Observation Count"},
        category_orders={taxonomy: sorted(bird[taxonomy].unique())})
    return plot_birds


if __name__ == '__main__':
    app.run_server(debug=True)