import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import dash

from app import app

# mapbox styles that do not require a token: open-street-map, white-bg, carto-positron, carto-darkmatter, stamen-terrain, stamen-toner, stamen-watercolor
# color scale informaiton: https://plotly.com/python/builtin-colorscales/

#read file
df = pd.read_csv('pollution.csv').fillna(0)

# Create two lists for the loop results to be placed
lat = []
lon = []
# ERROR: THE ABOVE CREATES LISTS BUT APPEND BELOW IS APPENDING TO A SINGLE STRING OBJECT
# For each row in a varible,
for row in df['lat/long']:
    try:
        # contains ' '
        if row[1] == "'":
            split = row.split("'")
            #print(split[1])
            #print(split[3])
            lat.append(split[1])
            lon.append(split[3])
        # doesn't contain ' '
        else:
            split = row.split(',')
            lat.append(split[0][1:])#(row[1:10])
            #print(split[0][1:])
            #print(split[1][:-1])
            lon.append(split[1][:-1])#(row[12:-1])
    except:
        lat.append(np.NaN)
        lon.append(np.NaN)

# Create two new columns from lat and lon
df['Lat'] = lat
df['Long'] = lon

#create lists
indicators = df['Pollutant'].unique()
locations = list(df['Location'].unique())
locations.append('All Monitoring Sites')

layout = html.Div([
    html.H3('(DS4A Team 27 - Air Pollution and Health Ailments around Heathrow Airport - Pollution Levels by Monitoring Sites'),
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='indicatorDropdown',
                options=[{'label': i, 'value': i} for i in indicators],
                value='Carbon monoxide',
            ),
        ],
            style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='monitoringSiteDropdown',
                options=[{'label': i, 'value': i} for i in locations],
                value='All Monitoring Sites',
            ),
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='monitoringSiteMap')
    ]),

    html.Div(dcc.Slider(
        id='yearSlider',
        min=df['Date'].min(),
        max=df['Date'].max(),
        value=df['Date'].max(),
        marks={str(year): str(year) for year in df['Date'].unique()},
        step=None
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'}),

    html.Div(id='app-1-display-value'),

    # Navigation Tree - Don't Delete
    html.Div(dcc.Link('Go to App 1', href='/apps/app1')),
    html.Div(dcc.Link('Go to App 2', href='/apps/app2')),
    html.Div(dcc.Link('Go to App 3', href='/apps/app3')),
    html.Div(dcc.Link('Go to App 4', href='/apps/app4')),
    html.Div(dcc.Link('Go to App 5', href='/apps/app5')),

])

@app.callback(
    dash.dependencies.Output('monitoringSiteMap', 'figure'),
    [dash.dependencies.Input('indicatorDropdown', 'value'),
    dash.dependencies.Input('monitoringSiteDropdown', 'value'),
     dash.dependencies.Input('yearSlider', 'value')
     ])
def update_graph(indicator_val, monitoringsite_val,
                 year_val):

    if monitoringsite_val == 'All Monitoring Sites':
        dff = df
    else:
        dff = df[df['Location'] == monitoringsite_val]

    dff = dff[dff['Pollutant'] == indicator_val]
    dff = dff[dff['Date'] == year_val]

    fig = px.scatter_mapbox(dff, lat="Lat", lon = "Long", color="Indicator Value (R µg/m3)", size="Indicator Value (R µg/m3)",
                            color_continuous_scale=px.colors.diverging.Portland, size_max=30, zoom=7.5,
                            hover_name='Location', hover_data=['Pollutant', 'Indicator Value (R µg/m3)', 'Lat', 'Long'])

    fig.update_layout(mapbox_style="carto-positron")

    return fig