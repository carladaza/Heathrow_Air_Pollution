import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import dash
import plotly.express as px
import math

from app import app

#read file
dfOuter = pd.read_csv('yearlyOuterStacked.csv').fillna(0)

#date substring year
dfOuter["Date"] = [int(str(x)[0:4]) for x in dfOuter["Date"]]

#heathrow distance
heathrow_lat, heathrow_lon = 51.47002, -0.454295

#calculate distance from monitoring sites
def getDistance(x,y):
    xSquared = (heathrow_lat - x) * (heathrow_lat - x)
    ySquared = (heathrow_lon - y) * (heathrow_lon - y)
    radicand = xSquared + ySquared
    return math.sqrt(radicand)
dfOuter["Distance"] = [getDistance(x,y) for x, y in zip(dfOuter["Lat"], dfOuter["Long"])]

#melt indicators to one column
dfOuter = dfOuter.melt(id_vars = ["Date", "Location", "CCG", "Lat", "Long", "Distance"], var_name = "Indicator", value_name = "Indicator Value")

#create lists
indicators = dfOuter['Indicator'].unique()
locations = list(dfOuter['Location'].unique())
locations.append('All Monitoring Sites')

#wgs84_geod = Geod(ellps='WGS84')

#def get_distance(lat1, lon1, lat2, lon2):
        # distance is returned in metres (cross-checked on site)
#        az12,az21,dist = wgs84_geod.inv(lon1,lat1,lon2,lat2)
#        return(dist)

#def calc_heathrow_dist(row):
#    return get_distance(heathrow_lat, heathrow_lon, row['Lat'], row['Long'])
    
    
#def calc_heathrow_dist_from_latlong(lat_long):
#    try:
#        return get_distance(heathrow_lat, heathrow_lon, lat_long[0], lat_long[1])
#    except TypeError:
#        print(lat_long)
#    return 'nothing'

layout = html.Div([
    html.H3('Monitoring Site Values vs. Distance'),

    # container for the two drop down options, (check how the id, correlates to the callback below)
    html.Div([
            html.Div([
                dcc.Dropdown(
                    id='xaxis',
                    options=[{'label': i, 'value': i} for i in indicators],
                    value='Nitrogen dioxide',
                ),
            ], style={'width': '49%', 'display': 'inline-block'}
            ),
            #html.Div([
            #    dcc.Dropdown(
            #        id='yaxis',
            #        options=[{'label': i, 'value': i} for i in available_indicators],
            #        value='Asthma Admissions Over 19yr',
            #    ),
            #], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),

    # container for the graph (check how the id, correlates to the callback below)
    html.Div([
        dcc.Graph(
            id='monitoringSiteDistance',
            hoverData={'points': [{'customdata': 'Oxford'}]}
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
    dash.dependencies.Output('monitoringSiteDistanxe', 'figure'),
    [dash.dependencies.Input('xaxis', 'value'),
     #dash.dependencies.Input('crossfilter-yaxis-column2', 'value'),
     ])
def update_graph(xaxis):#, yaxis,):
    dff = dfOuter

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis]['Value'],
            y=dff[dff['Indicator Value']]['Value'],
            hover_name=dff[dff['Indicator Name'] == xaxis]['Location']
            )
    #fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Area Name'])
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig

