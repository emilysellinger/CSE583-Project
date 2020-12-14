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
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

from phoenix.code.appfunctions import subset_date, subset_air_quality

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

# read in the data here:

aq = pd.read_csv('https://raw.githubusercontent.com/emilysellinger/Phoenix/main/phoenix/data/OR_DailyAQ_byCounty.csv')  # noqa

bird = pd.read_csv('https://raw.githubusercontent.com/emilysellinger/Phoenix/main/phoenix/data/shortened_bird_data.csv')  # noqa

with urlopen('https://raw.githubusercontent.com/emilysellinger/Phoenix/main/phoenix/data/Oregon_counties_map.geojson') as response:  # noqa
    counties = json.load(response)

# subsetting data to relevant months
aq['Date'] = pd.to_datetime(aq['Date'])
months = [8, 9, 10, 11]
aq = aq.loc[aq['Date'].dt.month.isin(months)]
bird['observation date'] = pd.to_datetime(bird['observation date'])
bird = bird.loc[bird['observation date'].dt.month.isin(months)]

# categories for dropdowns
common_names = sorted(bird['common name'].unique())
county_names = aq['County'].unique()
full_months = ['August', 'September', 'October', 'November']

# configures the style and layout of the app (including headings etc)
app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=[
        html.H1(
            children='PHOENIX',
            style={
                'textAlign': 'left',
                'color': colors['text'],
                'margin-top': 0,
                'margin-bottom': 20,
                'margin-left': 20,
                'font-weight': 'bold'
            }
        ),

        html.Div(
            children='How have Oregon bird sightings changed with air quality?',
            style={
                'textAlign': 'left',
                'color': colors['text'],
                'margin-top': 20,
                'margin-bottom': 20,
                'margin-left': 20,
                'font-style': 'italic'}
        ),

        html.Div([
            dcc.Dropdown(
                id='species',
                options=[{'label': i, 'value': i} for i in common_names],
                value='Acorn Woodpecker'),  # gives you default option

            html.Div(id='dd-output-container',
                     style={'width': '90%', 'margin-bottom': 5,
                            'margin-left': 20})
        ]),

        html.Div([
            dcc.Dropdown(
                id='month',
                options=[{'label': i, 'value': i} for i in full_months],
                value='August'),  # gives you default option

            html.Div(id='dd2-output-container',
                     style={'width': '90%', 'margin-bottom': 5,
                            'margin-left': 20})
        ]),

        html.Div([
            dcc.Graph(
                id='aq-map',
                style={'width': '90vh', 'height': '50vh'}),
            html.Div(id='graph-output',
                     style={'margin-left': 20, 'backgroundColor': colors['background'],
                            'color': colors['text']})
        ]),

        html.Div([
            dcc.Slider(
                id='day-slider',
                min=1,
                max=31,
                value=1,
                step=1,
                marks={1: '1', 10: '10', 20: '20', 31: '31'}),
            html.Div(id='slider-output-container',
                     style={'width': '90%'})
        ]),

        html.Div(
            id='day-indicator',
            style={'margin-top': 20, 'margin-bottom': 20,
                   'margin-left': 20, 'color': colors['text']}),

        dcc.Dropdown(
            id='county-names',
            options=[{'label': i, 'value': i} for i in county_names],
            value='Baker'),

        dcc.Graph(
            id='bird-counts')
    ]
)


# interactive components:
# AQ choropleth map
@app.callback(
    Output('aq-map', 'figure'),
    Input('species', 'value'),
    Input('month', 'value'),
    Input('day-slider', 'value'))
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
    sub_bird = bird.loc[bird['common name'] == species]

    sub_aq = subset_date(aq, 'Date', month, day_slider)

    aq_map_choropleth = px.choropleth_mapbox(
        sub_aq, geojson=counties,
        featureidkey='properties.altname', locations="County",
        color="Avg_PM2.5", hover_name="County",
        color_continuous_scale=px.colors.sequential.Turbo,
        range_color=(0, 300),
        mapbox_style='carto-positron', zoom=5,
        center={"lat": 43.81395826303137, "lon": -120.60278690370761},
        opacity=0.5,
        labels={'Avg_PM2.5': 'Average PM 2.5'}
    )

    try:
        sub_bird = subset_date(sub_bird, 'observation date', month, day_slider)

        aq_map_scatter = px.scatter_mapbox(
            sub_bird, lat='latitude', lon='longitude',
            size='observation count', zoom=5,
            color_discrete_sequence=['#EF553B'],
            mapbox_style="carto-positron",
            center={"lat": 43.81395826303137, "lon": -120.60278690370761}
        )
        aq_map_choropleth.add_trace(aq_map_scatter.data[0])

    except ValueError:
        pass
    return aq_map_choropleth

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
    return 'Date: ' + str(month) + ' ' + str(day_slider) + ', 2020'

    # Bird Count Line Graph


@app.callback(
    Output('bird-counts', 'figure'),
    Input('county-names', 'value'))
def update_count_graph(county_name):
    """
    Displays a chart with the counts of birds by species for selected county.

    Args:
        county_name (str): selected county from dropdown
    Returns:
        count_plot (figure): plot of bird observations over time with AQI category
    """
    sub_bird_county = bird.loc[bird['county'] == county_name]

    haz_dates, haz_dates_offset, vh_dates, vh_dates_offset = subset_air_quality(aq, county_name)

    count_plot = px.scatter(
            sub_bird_county, x='observation date',
            y='observation count', color='common name',
            labels={"common name": "Species", "observation date": "Date", "observation count": "Observation Count"},
            category_orders={"common name": sorted(bird['common name'].unique())})

    for i in range(len(haz_dates)):
        count_plot.add_vrect(x0=haz_dates[i], x1=haz_dates_offset[i],
                             fillcolor="OrangeRed", opacity=0.5, layer="below", line_width=0)

    for i in range(len(vh_dates)):
        count_plot.add_vrect(x0=vh_dates[i], x1=vh_dates_offset[i],
                             fillcolor="Gold", opacity=0.5,
                             layer="below", line_width=0)

    return count_plot


if __name__ == '__main__':
    app.run_server(debug=True)
