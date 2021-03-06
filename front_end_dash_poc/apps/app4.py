import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_bootstrap_components as dbc


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

layout = html.Div([
    # Navigation Tree - Don't Delete
    html.Div([
        html.Div([
            dcc.Link('Air Pollution and Distance', href='/apps/app1'),
            dcc.Link('Air Pollution/Distance Relationship', href='/apps/app2', style={"margin-left": "30px"}),
            dcc.Link('Health and Distance', href='/apps/app3', style={"margin-left": "30px"}),
            dcc.Link('Health/Distance Over Time', href='/apps/app4', style={"margin-left": "30px"}),
            dcc.Link('Health and Air Pollution', href='/apps/app5', style={"margin-left": "30px"})]),
    ]),

    html.H3('Heathrow Airport Study: Air Pollution and Health Ailments Analysis For Select NHS CCGs Regions'),


    html.Div([

        html.Div([
            dcc.Dropdown(
                id='indicator-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='COPD Admissions',
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

    html.H4('Geographical Visualisation of Health and Pollution Indicators Over Time'),

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

        html.Div(dcc.Slider(
                id='crossfilter-year-slider',
            ), style={'width': '49%', 'margin-left': 'auto', 'margin-right': 'auto',}),
    ]),


    html.H4('Health Indicator and Air Pollutant Visualisations Over Time'),

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
                        id='radius-nonradius',
                        options=[{'label': i, 'value': i} for i in ['Inner/Outer CCG Breakdown', 'All CCGs']],
                        value='Inner/Outer CCG Breakdown',
                        labelStyle={'display': 'inline-block'}
                    ),

                ],style={'width': '49%', 'display': 'inline-block',})


            ],style={'padding': '5px 5px 5px 5px'}),

            html.Div([dcc.Graph(id='crossfilter-line-health')]),

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

            html.Div([dcc.Graph(id='crossfilter-line-poll')]),


        ], style={'width': '49%', 'display': 'inline-block', 'float': 'right'}),
    ]),



    ])


@app.callback(
    [dash.dependencies.Output('crossfilter-year-slider', 'marks'),
    dash.dependencies.Output('crossfilter-year-slider', 'min'),
    dash.dependencies.Output('crossfilter-year-slider', 'max'),
    dash.dependencies.Output('crossfilter-year-slider', 'value'),
     ],
    [dash.dependencies.Input('indicator-column', 'value'),
     ])
def update_slider(indicator_name):
    tmp = df.copy()

    # Only display values that have a reading, Filter the NaNs/0 values (I had 0 in df for this, as had to change nans to 0 for map originally)
    tmp = tmp[(tmp['Indicator Name'] == indicator_name) & (~tmp['Value'].isnull())]
    tmp = tmp[tmp['Value'] != 0]

    # return the new marks, new min and new max
    new_marks = {str(year): str(year) for year in tmp['Year'].unique()}
    new_min = tmp['Year'].min()
    new_max = tmp['Year'].max()
    return new_marks, new_min, new_max, new_max


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
    # dash.dependencies.Input('crossfilter-avg-sum', 'value'),
    dash.dependencies.Input('radius-nonradius', 'value'),
     ])
def update_health_line(indicator_name,
                       radius_toggle):
    if radius_toggle == 'Inner/Outer CCG Breakdown':
        dff = df.groupby(['Year', 'Radius Location', 'Indicator Name']).mean('Value').reset_index()

        #rename the radius location and values appropriately
        dff = dff.rename(columns={'Radius Location': 'CCG Distance'})
        dff['CCG Distance'] = dff['CCG Distance'].apply(lambda x: '<15km' if x == 'Inner' else '>15km')

    else:
        dff = df.groupby(['Year', 'Indicator Name']).mean('Value').reset_index()

    title = 'Average {0} Across Time for NHS CCGs Regions'.format(indicator_name)
    dff = dff[dff['Indicator Name'] == indicator_name]

    # remove 0 at this point we wouldn't expect an average of 0, for visualisation purposes
    dff = dff[dff['Value'] != 0]

    fig12245 = px.line(dff,
                     x='Year',
                     y='Value',
                     color='CCG Distance' if radius_toggle == 'Inner/Outer CCG Breakdown' else None,
                     title=title)

    fig12245.update_yaxes(title='Indicator Value, Per 100,000 Population')
    return fig12245


@app.callback(
    dash.dependencies.Output('crossfilter-line-poll', 'figure'),
    [dash.dependencies.Input('indicator-poll-dropdown', 'value'),
    dash.dependencies.Input('radius-nonradius1', 'value'),
     ])
def update_poll_line(indicator_name, radius_toggle):
    if radius_toggle == 'Inner/Outer CCG Breakdown':
        dff = df.groupby(['Year', 'Radius Location', 'Indicator Name']).mean('Value').reset_index()

        #rename the radius location and values appropriately
        dff = dff.rename(columns={'Radius Location': 'CCG Distance'})
        dff['CCG Distance'] = dff['CCG Distance'].apply(lambda x: '<15km' if x == 'Inner' else '>15km')
    else:
        dff = df.groupby(['Year', 'Indicator Name']).mean('Value').reset_index()

    title = 'Average {0} Across Time for NHS CCGs Regions'.format(indicator_name)

    dff = dff[dff['Indicator Name'] == indicator_name]

    # remove 0 at this point we wouldn't expect an average of 0 or sum of 0 ? (maybe though, double check)
    dff = dff[dff['Value'] != 0]

    fig12223 = px.line(dff,
                     x='Year',
                     y='Value',
                     color='CCG Distance' if radius_toggle == 'Inner/Outer CCG Breakdown' else None,
                     title=title)

    fig12223.update_yaxes(title='Indicator Value (R µg/m3)')
    return fig12223
