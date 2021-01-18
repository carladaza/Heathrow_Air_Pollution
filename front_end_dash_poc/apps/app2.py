import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import dash
import plotly.express as px

from app import app

df = pd.read_csv('admission_pollution_melt.csv')
available_indicators = df['Indicator Name'].unique()

layout = html.Div([
    html.H3('App 2 - Carla/Kayli'),

    # container for the two drop down options, (check how the id, correlates to the callback below)
    html.Div([
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-xaxis-column2',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Asthma Admissions Over 19yr',
                ),
            ], style={'width': '49%', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-yaxis-column2',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Asthma Admissions Over 19yr',
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
            id='crossfilter-indicator-scatter2',
            hoverData={'points': [{'customdata': 'NHS Richmond CCG'}]}
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
    dash.dependencies.Output('crossfilter-indicator-scatter2', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column2', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column2', 'value'),
     ])
def update_graph(xaxis_column_name, yaxis_column_name,):
    dff = df

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Area Name']
            )
    fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Area Name'])
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig

