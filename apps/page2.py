import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from apps.navbar import Navbar
from app import app
from apps.eurostatapi import popAgeGroup
import plotly.graph_objs as go
import plotly.express as px

nav = Navbar()

year_options = []
for time in popAgeGroup()['time'].unique():
    year_options.append({'label': str(time), 'value': time})

features = popAgeGroup().columns

body = html.Div([
    html.Div([
        html.H3('Population'),

        html.Div(id='app-2-display-value'),
        dcc.Link('Go to App 1', href='/apps/page1'),


        html.Div([
            html.Div([
                dcc.Dropdown(id='xaxis',
                             options=[{'label': i, 'value': i} for i in features],
                             value='indic_de')
            ], style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(id='yaxis',
                             options=[{'label': i, 'value': i} for i in features],
                             value='values')
            ], style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(id='year-picker', options=year_options,
                             value=popAgeGroup()['time'].min())
            ])
        ]),

        html.Div([
            dcc.Graph(id='bar')
        ])
    ]),

], style={'padding': 5})


@app.callback(Output('scatter', 'figure'),
              [Input('year-picker', 'value'),
               Input('xaxis', 'value'),
               Input('yaxis', 'value')])
def update_graph(picked_year, xaxis_name, yaxis_name):
    filtered_df = popAgeGroup()[popAgeGroup()['time'] == picked_year]

    traces = []

    for country_name in filtered_df['geo'].unique():
        df_by_country = filtered_df[filtered_df['geo'] == country_name]
        traces.append(go.Scatter(x=df_by_country[xaxis_name],
                                 y=df_by_country[yaxis_name],
                                 mode='markers',
                                 marker={'size': 15,
                                         'opacity': 0.5,
                                         'line': {'width': 0.5, 'color': 'white'}}
                                 ))
    return {'data': traces,
            'layout': go.Layout(title='population from groups',
                                xaxis={'title': xaxis_name},
                                yaxis={'title': yaxis_name},
                                hovermode='closest'),
            }


@app.callback(
    Output('app-2-display-value', 'children'),
    [Input('app-2-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


def PageLayOut():
    layout = html.Div([
        nav,
        body
    ])
    return layout
