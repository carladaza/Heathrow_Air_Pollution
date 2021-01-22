import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash

from app import app

# mapbox styles that do not require a token: open-street-map, white-bg, carto-positron, carto-darkmatter, stamen-terrain, stamen-toner, stamen-watercolor
# color scale informaiton: https://plotly.com/python/builtin-colorscales/

#read file
dfOuter = pd.read_csv('yearlyOuterStacked.csv').fillna(0)

#date substring year
dfOuter["Date"] = [int(str(x)[0:4]) for x in dfOuter["Date"]]

#melt indicators to one column
dfOuter = dfOuter.melt(id_vars = ["Date", "Location", "CCG", "Lat", "Long"], var_name = "Indicator", value_name = "Indicator Value")

#create lists
indicators = dfOuter['Indicator'].unique()
locations = list(dfOuter['Location'].unique())
locations.append('All Monitoring Sites')

layout = html.Div([
    html.H3('(DS4A Team 27 - Air Pollution and Health Ailments around Heathrow Airport - Pollution Levels by Monitoring Sites'),
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='indicatorDropdown',
                options=[{'label': i, 'value': i} for i in indicators],
                value='Nitrogen dioxide',
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
        min=dfOuter['Date'].min(),
        max=dfOuter['Date'].max(),
        value=dfOuter['Date'].max(),
        marks={str(year): str(year) for year in dfOuter['Date'].unique()},
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
        dff = dfOuter
    else:
        dff = dfOuter[dfOuter['Location'] == monitoringsite_val]

    dff = dff[dff['Indicator'] == indicator_val]
    dff = dff[dff['Date'] == year_val]

    fig = px.scatter_mapbox(dff, lat="Lat", lon ="Long", color="Indicator Value", size="Indicator Value",
                            color_continuous_scale=px.colors.diverging.Portland, size_max=30, zoom=7.5,
                            hover_name='Location', hover_data=['Indicator', 'Indicator Value', 'Lat', 'Long'])

    fig.update_layout(mapbox_style="carto-positron")

    return fig