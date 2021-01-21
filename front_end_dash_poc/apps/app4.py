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

df = pd.read_csv('health_pollution_final.csv').fillna(0)

# set indicators and CCG locations for hhe drop downs
available_indicators = df['Indicator Name'].unique()
available_locations = list(df['Area Name'].unique())
available_locations.append('All CCGs')

# get pollution indicators
pollution_indicators = df[df['Indicator Type'] == 'Air Pollutant']['Indicator Name'].unique()
health_indicators = df[df['Indicator Type'] != 'Air Pollutant']['Indicator Name'].unique()

# do a groupby to get the correct format for line plots
df_f = df.groupby(['Year', 'Radius Location', 'Indicator Name']).sum('Value').reset_index()
df_f = df_f[df_f['Indicator Name'] == 'COPD Admissions']

fig122 = px.line(df_f[df_f['Value'] != 0], x='Year', y='Value', color='Radius Location')
fig122.update_yaxes(title='COPD Admissions')

layout = html.Div([
    html.H3('(Inspired By Seb Joseph - DS4A Team 27 - Air Pollution and Health Ailments around Heathrow Airport'),
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='indicator-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Heart Failure Admissions',
                clearable=False
            ),
        ],
            style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='ccg-column',
                options=[{'label': i, 'value': i} for i in available_locations],
                value='All CCGs',
                clearable=False
            ),
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        html.Div([
            dcc.Graph(
                id='crossfilter-indicator-scattermap'
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(
                id='crossfilter-indicator-density-mapbox'
            )
        ], style={'width': '49%', 'display': 'inline-block', 'float': 'right'}),
    ]),


    html.Div(dcc.Slider(
        id='crossfilter-year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    ), style={'width': '49%', 'margin-left': 'auto','margin-right': 'auto',}),

    html.H4('Health Indicators and Air Pollutants Over Time'),

    html.Div([

        html.Div([
            html.Div([dcc.Dropdown(
                id='indicator-health-dropdown',
                options=[{'label': i, 'value': i} for i in health_indicators],
                value='Heart Failure Admissions',
                clearable=False
            )]),

            html.Div([

                html.Div([
                    dcc.RadioItems(
                        id='crossfilter-avg-sum',
                        options=[{'label': i, 'value': i} for i in ['Average', 'Sum']],
                        value='Average',
                        labelStyle={'display': 'inline-block'}
                    ),

                ],style={'width': '49%', 'display': 'inline-block'}),

                html.Div([
                    dcc.RadioItems(
                        id='radius-nonradius',
                        options=[{'label': i, 'value': i} for i in ['Inner/Outer CCG Breakdown', 'All CCGs']],
                        value='Inner/Outer CCG Breakdown',
                        labelStyle={'display': 'inline-block'}
                    ),

                ],style={'width': '49%', 'display': 'inline-block', 'float': 'right'})


            ],style={'padding': '5px 5px 5px 5px'}),

            html.Div([dcc.Graph(figure=fig122, id='crossfilter-line-health')]),

        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Div([dcc.Dropdown(
                id='indicator-poll-dropdown',
                options=[{'label': i, 'value': i} for i in pollution_indicators],
                value='Nitrogen dioxide',
                clearable=False
            )]),
            html.Div([
                dcc.RadioItems(
                    id='radius-nonradius1',
                    options=[{'label': i, 'value': i} for i in ['Inner/Outer CCG Breakdown', 'All CCGs']],
                    value='Inner/Outer CCG Breakdown',
                    labelStyle={'display': 'inline-block'}
                ),

            ],style={'padding': '5px 5px 5px 5px'}),

            html.Div([dcc.Graph(figure=fig122, id='crossfilter-line-poll')]),


        ], style={'width': '49%', 'display': 'inline-block', 'float': 'right'}),
    ]),

    # Navigation Tree - Don't Delete
    html.Div(dcc.Link('Go to App 1', href='/apps/app1')),
    html.Div(dcc.Link('Go to App 2', href='/apps/app2')),
    html.Div(dcc.Link('Go to App 3', href='/apps/app3')),
    html.Div(dcc.Link('Go to App 4', href='/apps/app4')),
    html.Div(dcc.Link('Go to App 5', href='/apps/app5')),

])

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scattermap', 'figure'),
    [dash.dependencies.Input('indicator-column', 'value'),
    dash.dependencies.Input('ccg-column', 'value'),
     dash.dependencies.Input('crossfilter-year-slider', 'value')
     ])
def update_graph(indicator_name, ccg_name,
                 year_value):

    if ccg_name == 'All CCGs':
        dff = df
    else:
        dff = df[df['Area Name'] == ccg_name]

    dff = dff[dff['Indicator Name'] == indicator_name]
    dff = dff[dff['Year'] == year_value]

    fig = px.scatter_mapbox(dff, lat="LAT", lon="LONG", color="Value", size="Value",
                            color_continuous_scale=px.colors.diverging.Portland, size_max=30, zoom=7.5,
                            hover_name='Area Name', hover_data=['Indicator Name', 'Value', 'LAT', 'LONG'])

    fig.update_layout(mapbox_style="carto-positron")

    return fig


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-density-mapbox', 'figure'),
    [dash.dependencies.Input('indicator-column', 'value'),
    dash.dependencies.Input('ccg-column', 'value'),
     dash.dependencies.Input('crossfilter-year-slider', 'value')
     ])
def update_density_graph(indicator_name, ccg_name,
                 year_value):

    if ccg_name == 'All CCGs':
        dff = df
    else:
        dff = df[df['Area Name'] == ccg_name]

    dff = dff[dff['Value'] != 0]

    dff = dff[dff['Indicator Name'] == indicator_name]
    dff = dff[dff['Year'] == year_value]

    fig_f = px.density_mapbox(dff, lat='LAT', lon='LONG', z='Value', radius=40, zoom=7,
                              mapbox_style="open-street-map", hover_name='Area Name',
                              hover_data=['Indicator Name', 'Value', 'LAT', 'LONG'])
    return fig_f


@app.callback(
    dash.dependencies.Output('crossfilter-line-health', 'figure'),
    [dash.dependencies.Input('indicator-health-dropdown', 'value'),
    dash.dependencies.Input('crossfilter-avg-sum', 'value'),
    dash.dependencies.Input('radius-nonradius', 'value'),
     ])
def update_health_line(indicator_name, avg_sum, radius_toggle):
    if avg_sum == 'Average':
        if radius_toggle == 'Inner/Outer CCG Breakdown':
            dff = df.groupby(['Year', 'Radius Location', 'Indicator Name']).mean('Value').reset_index()
        else:
            dff = df.groupby(['Year', 'Indicator Name']).mean('Value').reset_index()

    else:
        if radius_toggle == 'Inner/Outer CCG Breakdown':
            dff = df.groupby(['Year', 'Radius Location', 'Indicator Name']).sum('Value').reset_index()
        else:
            dff = df.groupby(['Year', 'Indicator Name']).sum('Value').reset_index()

    title = '{0} Across Time for NHS CCGs Regions'.format(indicator_name)

    dff = dff[dff['Indicator Name'] == indicator_name]

    # remove 0 at this point we wouldn't expect an average of 0 or sum of 0 ? (maybe though, double check)
    dff = dff[dff['Value'] != 0]

    fig122 = px.line(dff,
                     x='Year',
                     y='Value',
                     color='Radius Location' if radius_toggle == 'Inner/Outer CCG Breakdown' else None,
                     title=title)
    fig122.update_yaxes(title=indicator_name)

    return fig122



@app.callback(
    dash.dependencies.Output('crossfilter-line-poll', 'figure'),
    [dash.dependencies.Input('indicator-poll-dropdown', 'value'),
    # dash.dependencies.Input('crossfilter-avg-sum1', 'value'),
    dash.dependencies.Input('radius-nonradius1', 'value'),
     ])
def update_poll_line(indicator_name, radius_toggle):
    if radius_toggle == 'Inner/Outer CCG Breakdown':
        dff = df.groupby(['Year', 'Radius Location', 'Indicator Name']).mean('Value').reset_index()
    else:
        dff = df.groupby(['Year', 'Indicator Name']).mean('Value').reset_index()

    title = 'Average {0} Across Time for NHS CCGs Regions'.format(indicator_name)

    dff = dff[dff['Indicator Name'] == indicator_name]

    # remove 0 at this point we wouldn't expect an average of 0 or sum of 0 ? (maybe though, double check)
    dff = dff[dff['Value'] != 0]

    fig122 = px.line(dff,
                     x='Year',
                     y='Value',
                     color='Radius Location' if radius_toggle == 'Inner/Outer CCG Breakdown' else None,
                     title=title)
    fig122.update_yaxes(title=indicator_name)

    return fig122