# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

'''
Dash app for birder use case
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#markdown text for throughout the app:
TITLE_TEXT = '''
### Phoenix

How have Oregon Bird sightings changed with air quality?
'''
#read in the data here:
aq = pd.read_csv('https://raw.githubusercontent.com/emilysellinger/CSE583-Project/main/Phoenix/data/Daily_Avg_PM2.5_Location.csv')

available_locations = aq["Name"].unique()
#plotly plots go here:

#configures the style and layout of the app (including headings etc)
app.layout = html.Div([
    dcc.Markdown(children = TITLE_TEXT),

    dcc.Dropdown(
    	id = 'sensor-location',
    	options = [{'label' : i, 'value': i} for i in available_locations],
    	value = 'Albany Calapooia School'), #gives you default option

    dcc.Graph(
        id='counts-of-categories',)
])

#interactive components:
@app.callback(
    Output('counts-of-categories','figure'),
    Input('sensor-location', 'value'))

def update_graph(sensor_location):
    '''
    Updates graph depending on user input.
    Par = sensor location from dropdown
    Returns figure for that location
    '''
    sub_aq = aq[aq.Name == sensor_location]
    sub_counts = px.histogram(sub_aq, x="Category")
    sub_counts.update_layout(transition_duration=500)
    return sub_counts

if __name__ == '__main__':
    app.run_server(debug=True)
