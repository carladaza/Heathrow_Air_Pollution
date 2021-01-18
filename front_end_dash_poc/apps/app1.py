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

df = pd.read_csv('admission_pollution_melt.csv').fillna(0)
df = df[df['Indicator Name'] != 'heathrow_distance']
available_indicators = df['Indicator Name'].unique()

layout = html.Div([
    html.H3('App 1'),

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
            id='crossfilter-indicator-scattermap')
    ]),

    html.Div(id='app-1-display-value'),
    dcc.Link('Go to App 2', href='/apps/app2'),

    html.Div(dcc.Slider(
        id='crossfilter-year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'}),
])

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scattermap', 'figure'),
    [dash.dependencies.Input('indicator-column', 'value'),
     dash.dependencies.Input('crossfilter-year-slider', 'value')
     ])
def update_graph(indicator_name,
                 year_value):
    dff = df[df['Indicator Name'] == indicator_name]
    dff = dff[dff['Year'] == year_value]

    fig = px.scatter_mapbox(dff, lat="LAT", lon="LONG", color="Value", size="Value",
                            color_continuous_scale=px.colors.diverging.Portland, size_max=30, zoom=7,
                            hover_name='Area Name', hover_data=['Indicator Name', 'Value', 'LAT', 'LONG'])

    fig.update_layout(mapbox_style="carto-positron")

    return fig


#### Density heatmap example ### -- disregarded in favour of the scatter mapbox

# quakes = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')
# fig = go.Figure(go.Densitymapbox(lat=df.LAT, lon=df.LONG, z=df.Value,
#                                  radius=10))
# fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=180)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})