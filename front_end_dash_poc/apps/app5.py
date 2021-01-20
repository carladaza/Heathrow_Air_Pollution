import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import dash
import plotly.express as px


from app import app

df = pd.read_csv('admission_pollution_melt.csv')

available_indicators = df['Indicator Name'].unique()

markdown_text = """
This is an interactive dashboard visualising the correlation between selected health indicators and air pollutants.
Select different indicators from the drop downs to see if they are correlated with each other.
Hover over points (CCGs) on the aggregated correlation graph to generate line plots showing indicators over time for the selected NHS CCGs.

Please note that for the year by year correlation graph, only selected years are available for some indicators. 

"""

layout = html.Div([
    html.H3('App 5 - Joseph/Sheetal?'),

    html.Div([
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-xaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Asthma Admissions Over 19yr',
                ),
                dcc.RadioItems(
                    id='crossfilter-xaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ],
            style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='crossfilter-yaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Asthma Admissions Over 19yr',
                ),
                dcc.RadioItems(
                    id='crossfilter-yaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),

    dcc.Markdown(children=markdown_text),

    html.Div([
        html.H4('Correlation Scatter Plot - Aggregated Across Years - Select Indicators'),
        # html.P('This plot is interactive, please select indicators from the drop down menus'),
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'NHS Richmond CCG'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20', 'text-align': 'center'}),
    html.Div([
        html.H4('Interactive Line Graphs Showing Indicators Over time For Selected CCG'),
        # html.P('This plot is interactive, please hover over the CCGs on the Scatter to see indicators over time'),
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%', 'float': 'right', 'text-align': 'center'}),

    html.Div([
        html.H4('Correlation Scatter Plot - Year by Year Breakdown'),
        dcc.Graph(
            id='crossfilter-indicator-scatter5',
            hoverData={'points': [{'customdata': 'NHS Richmond CCG'}]}
        )
    ], style={'width': '49%', 'display': 'block', 'padding': '0 20', 'margin-left': 'auto','margin-right': 'auto', 'text-align': 'center'}),

    html.Div(dcc.Slider(
        id='crossfilter-year--slider5',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=2018,     # default value of the slider
        marks={str(year): str(year) for year in df['Year'].unique()},
        # marks=slider_values_formatted,
        step=None
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px','margin-left': 'auto','margin-right': 'auto' }),

    # Navigation Tree - Don't Delete
    html.Div(dcc.Link('Go to App 1', href='/apps/app1')),
    html.Div(dcc.Link('Go to App 2', href='/apps/app2')),
    html.Div(dcc.Link('Go to App 3', href='/apps/app3')),
    html.Div(dcc.Link('Go to App 4', href='/apps/app4')),
    html.Div(dcc.Link('Go to App 5', href='/apps/app5')),

])

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     ])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 ):
    dff = df

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Area Name']
            )

    fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Area Name'])
    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')
    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return fig


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter5', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider5', 'value')
     ])
def update_graph2(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value
                 ):
    dff = df[df['Year'] == year_value]

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Area Name']
            )

    fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Area Name'])
    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')
    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return fig


def create_time_series(dff, axis_type, title):

    fig = px.scatter(dff, x='Year', y='Value')
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')
    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
    return fig


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Area Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Area Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)


@app.callback(
    Output('app-2-display-value', 'children'),
    Input('app-2-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)