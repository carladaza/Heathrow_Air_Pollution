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

#convert object columns to float (pd.to_numeric can be done in one line, but with the errors argument I had an error)
df["Lat"] = pd.to_numeric(df["Lat"], errors='coerce')
df["Long"] = pd.to_numeric(df["Long"], errors='coerce')

#create lists
indicators = df['Pollutant'].unique()
locations = list(df['Location'].unique())
locations.append('All Monitoring Sites')

layout = html.Div([
    
    html.Div([
        html.Div([
            dcc.Link('Air Pollution and Distance', href='/apps/app1'),
            dcc.Link('Air Pollution/Distance Relationship', href='/apps/app2', style={"margin-left": "30px"}),
            dcc.Link('Health and Distance', href='/apps/app3', style={"margin-left": "30px"}),
            dcc.Link('Health/Distance Over Time', href='/apps/app4', style={"margin-left": "30px"}),
            dcc.Link('Health and Air Pollution', href='/apps/app5', style={"margin-left": "30px"})]),
    ]),

    html.H3('(DS4A Team 27 - Air Pollution and Health Ailments around Heathrow Airport - Pollution Levels by Monitoring Sites'),
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='indicatorDropdown',
                options=[{'label': i, 'value': i} for i in indicators],
                value='PM10 particulate matter (Hourly measured)',
                clearable=False
            ),
        ],
            style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='monitoringSiteDropdown',
                options=[{'label': i, 'value': i} for i in locations],
                value='All Monitoring Sites',
                clearable=False
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
    ), style={'width': '49%', 'margin-left': 'auto', 'margin-right': 'auto',}),

    html.Div(id='app-1-display-value'),
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

    dff = dff[dff['Indicator Value (R µg/m3)'] != 0]

    fig = px.scatter_mapbox(dff, lat="Lat", lon = "Long", color="Indicator Value (R µg/m3)", size="Indicator Value (R µg/m3)",
                            color_continuous_scale=px.colors.diverging.Portland, size_max=30, zoom=7.5,
                            hover_name='Location', hover_data=['Pollutant', 'Indicator Value (R µg/m3)', 'Lat', 'Long'])

    fig.update_layout(mapbox_style="carto-positron")

    return fig

@app.callback(
    [dash.dependencies.Output('yearSlider', 'marks'),
    dash.dependencies.Output('yearSlider', 'min'),
    dash.dependencies.Output('yearSlider', 'max'),
    dash.dependencies.Output('yearSlider', 'value'),
     ],
    [dash.dependencies.Input('indicatorDropdown', 'value'),
     ])
def update_slider(indicator_name):
    tmp = df.copy()
    # Only display values that have a reading, Filter the NaNs/0 values (I had 0 in df for this, as had to change nans to 0 for map originally)
    tmp = tmp[(tmp['Pollutant'] == indicator_name) & (~tmp['Indicator Value (R µg/m3)'].isnull())]
    tmp = tmp[tmp['Indicator Value (R µg/m3)'] != 0]
    # return the new marks, new min and new max
    new_marks = {str(year): str(year) for year in tmp['Date'].unique()}
    new_min = tmp['Date'].min()
    new_max = tmp['Date'].max()
    return new_marks, new_min, new_max, new_max