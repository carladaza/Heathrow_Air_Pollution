import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import dash
import plotly.express as px
import math

from app import app

#read file
df = pd.read_csv('complete_pollution.csv').fillna(0)

# melt
df = pd.melt(df, id_vars = ["Location", "Date", "CCG", "Radius", "lat/long", "distance_from_LHR"], value_vars = ["Carbon monoxide", "Nitric Oxide", "Nitrogen dioxide", "Oxides of Nitrogen", "Ozone", "PM10 Particulate matter", "PM10 particulate matter (Hourly measured)", "PM2.5 particulate matter (Hourly measured)", "Sulphur dioxide"], var_name = "Pollutant", value_name = "Indicator Value (R µg/m3)")

#create lists
indicators = df['Pollutant'].unique()
locations = list(df['Location'].unique())
locations.append('All Monitoring Sites')
dates = df["Date"].unique()

layout = html.Div([
    html.H3('Monitoring Site Values vs. Distance'),

    # container for the two drop down options, (check how the id, correlates to the callback below)
    html.Div([
            html.Div([
                dcc.Dropdown(
                    id='xaxis',
                    options=[{'label': i, 'value': i} for i in indicators],
                    value='Carbon monoxide',
                ),
            ], style={'width': '49%', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Dropdown(
                    id='yaxis',
                    options=[{'label': i, 'value': i} for i in dates],
                    value=df['Date'].max(),
                ),
            ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),

    # container for the graph (check how the id, correlates to the callback below)
    html.Div([
        dcc.Graph(
            id='monitoringSiteDistance',
            hoverData={'points': [{'customdata': 'Ealing - Acton Town Hall'}]}
        )
    ],
        # style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}   ---> commented out, you can edit the graph style via html this way
    ),

    # Navigation Tree - Don't Delete
    html.Div(dcc.Link('Go to App 1', href='/apps/app1')),
    html.Div(dcc.Link('Go to App 2', href='/apps/app2')),
    html.Div(dcc.Link('Go to App 3', href='/apps/app3')),
    html.Div(dcc.Link('Go to App 4', href='/apps/app4')),
    html.Div(dcc.Link('Go to App 5', href='/apps/app5')),

])

# this call back enables interactivity via the drop down options, everytime the drop down is changed the df is rebuilt (see dff code below)
@app.callback(
    dash.dependencies.Output('monitoringSiteDistance', 'figure'),
    [dash.dependencies.Input('xaxis', 'value'),
     dash.dependencies.Input('yaxis', 'value'),
     ])
def update_graph(xaxis, yaxis,):
    dff = df
    dff = dff[dff['Date'] == yaxis]
#ERROR
    fig = px.scatter(x=dff[dff['Pollutant'] == xaxis]['Indicator Value (R µg/m3)'],
            y=dff[dff['Pollutant'] == xaxis]["distance_from_LHR"],
            hover_name=dff[dff['Pollutant'] == xaxis]['Location']
            )
    #fig.update_traces(customdata=dff[dff['Pollutant'] == yaxis]['Location'])
    fig.update_xaxes(title=xaxis)
    fig.update_yaxes(title='Distance From Heathrow')
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig