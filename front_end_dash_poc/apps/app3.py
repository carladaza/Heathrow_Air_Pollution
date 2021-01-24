# Health and Distance

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import dash
import plotly.express as px

from app import app

df = pd.read_csv('health_data_final.csv')
available_indicators = df['Indicator Name'].unique()

layout = html.Div([
    html.H3('App 3 - Kayli - Health Indicators vs Distance from Airport'),

    html.Div([
        dcc.Dropdown(
            id='indicator-column',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value='Heart Failure Admissions',
        ),
    ],
        style={'width': '48%', 'display': 'inline-block'}),


    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scattermap-k'
        )
    ]),

    # Navigation Tree - Don't Delete
    html.Div(dcc.Link('Go to App 1', href='/apps/app1')),
    html.Div(dcc.Link('Go to App 2', href='/apps/app2')),
    html.Div(dcc.Link('Go to App 3', href='/apps/app3')),
    html.Div(dcc.Link('Go to App 4', href='/apps/app4')),
    html.Div(dcc.Link('Go to App 5', href='/apps/app5')),

])

# this call back enables interactivity via the drop down options, everytime the drop down is changed the df is rebuilt (see dff code below)
@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scattermap-k', 'figure'),
    [dash.dependencies.Input('indicator-column', 'value')
     ])
def update_graph(indicator_name):
    temp_df = df[df["Indicator Name"] == indicator_name]

    fig = px.scatter(temp_df, x="heathrow_distance", y="Value", trendline="ols",
        labels=dict(heathrow_distance="Distance from Heathrow Airport",
            Value="Rate of Health Indicator per 100k People"))

    return fig
