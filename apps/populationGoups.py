import time

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import dash_table as dt
from apps.eurostatapi import popAgeGroup
from app import app
from apps.navbar import Navbar

nav = Navbar()
'''used to create dropdown menues'''
year_options = []
for time in popAgeGroup()['time'].unique():
    year_options.append({'label': str(time), 'value': time})

group_options = []
for group in popAgeGroup()['indic_de'].unique():
    group_options.append({'label': str(group), 'value': group})

country_options = []
for country in popAgeGroup()['geo'].unique():
    country_options.append({'label': str(country), 'value': country})

features = popAgeGroup().columns

body = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Population by age group - tps00010"),
        html.Hr(),
        dbc.Row([
            dbc.Col(html.H3('Year filter')),
            dbc.Col(html.H3('Age Group filter')),
            dbc.Col(html.H3('Country filter')),
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(id='year-picker', options=year_options,
                             value=popAgeGroup()['time'].min(), multi=True, clearable=False)
            ),
            dbc.Col(
                dcc.Dropdown(id='group-picker', options=group_options,
                             value='PC_Y0_14', multi=True, clearable=False)
            ),
            dbc.Col(
                dcc.Dropdown(id='country-picker', options=country_options,
                             value=popAgeGroup()['geo'].unique(), multi=True, clearable=True)
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.H3("X-axis selection")
            ),
            dbc.Col(
                html.H3("Y-axis selection")
            )], justify='around'),
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(id='xaxis',
                             options=[{'label': i, 'value': i} for i in features],
                             value='geo',
                             clearable=False,
                             disabled=False)
            ),
            dbc.Col(
                dcc.Dropdown(id='yaxis',
                             options=[{'label': i, 'value': i} for i in features],
                             value='values',
                             clearable=False)
            )
        ], justify='around'),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Hr(),
                    dcc.Dropdown(id='styles',
                                 options=[{'label': 'Light Style', 'value': 'plotly_white'},
                                          {'label': 'Dark style', 'value': 'plotly_dark'},
                                          {'label': 'ggplot2 style', 'value': 'ggplot2'},
                                          {'label': 'seaborn style', 'value': 'seaborn'},
                                          {'label': 'presentation style', 'value': 'presentation'},
                                          {'label': 'x grid off style', 'value': 'xgridoff'},
                                          {'label': 'y grid off style', 'value': 'ygridoff'},
                                          {'label': 'grid on style', 'value': 'gridon'},
                                          {'label': 'none style', 'value': 'none'}],
                                 value='plotly_white',
                                 clearable=False
                                 ),
                    html.Hr(),
                    dbc.Button(id='update-button',
                               n_clicks=0,
                               children='Update graph',
                               color='primary',
                               className='mr-1',
                               block=True),

                ]), width={'size': 6, 'offset': 3}
            ),

        ]),
        dbc.Tabs(
            [
                dbc.Tab(label="Scatter", tab_id="scatter"),
                dbc.Tab(label="Pie chart", tab_id="pie"),
                dbc.Tab(label="Bar", tab_id='bar'),
                dbc.Tab(label="Sunburst", tab_id='sun'),
                dbc.Tab(label="Table", tab_id='table')
            ],
            id="tabs",
            active_tab="scatter",
        ),
        html.Div(id="tab-content", className="p-4"),
    ], className="mt-4", fluid=True,
)

'''graphs will be rendered in tab-content when the tab is clicked on to become active'''
@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"),
     Input("store", "data")],
)
def render_tab_content(active_tab, data):
    if active_tab and data is not None:
        if active_tab == "scatter":
            return dcc.Graph(figure=data["scatter"])

        elif active_tab == "pie":
            return dcc.Graph(figure=data["pie"])

        elif active_tab == "bar":
            return dcc.Graph(figure=data["bar"])

        elif active_tab == "sun":
            return dcc.Graph(id='sunburstout')

        elif active_tab == "table":
            return html.Table(id="datatable"), html.Div(id='tableout')

    return "No tab selected"


"""function to generate tables from selected data"""


@app.callback(Output('tableout', 'children'),
              [Input('update-button', 'n_clicks')],
              [State('year-picker', 'value'),
               State('group-picker', 'value'),
               State('country-picker', 'value'),
               ])
def gen_table(clicks, yearpick, grouppicker, countrypick):
    """filtering by year down to group down to country selected"""
    if clicks:
        if isinstance(yearpick, str):
            filtered_by_year = popAgeGroup()[popAgeGroup()['time'].isin([yearpick])]
        else:
            filtered_by_year = popAgeGroup()[popAgeGroup()['time'].isin(yearpick)]

        if isinstance(grouppicker, str):
            filter_by_group = filtered_by_year[filtered_by_year['indic_de'].isin([grouppicker])]
        else:
            filter_by_group = filtered_by_year[filtered_by_year['indic_de'].isin(grouppicker)]

        if isinstance(countrypick, str):
            filter_by_country = filter_by_group[filter_by_group['geo'].isin([countrypick])]
        else:
            filter_by_country = filter_by_group[filter_by_group['geo'].isin(countrypick)]

            table_out = dt.DataTable(
                data=filter_by_country.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in filter_by_country.columns],
                fixed_rows={'headers': True},
                page_size=30,
                style_table={'height': '300px', 'overflowY': 'auto'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                },
                export_format='xlsx',
                export_headers='display',
            )

            return table_out


@app.callback(Output("store", "data"),
              [Input('update-button', 'n_clicks')],
              [State('year-picker', 'value'),
               State('xaxis', 'value'),
               State('yaxis', 'value'),
               State('group-picker', 'value'),
               State('styles', 'value'),
               State('country-picker', 'value'),
               ])
def generate_graphs(n_clicks, yearpick, xaxis_name, yaxis_name, grouppicker, stylepick, countrypick):
    if not n_clicks:
        # generate empty graphs when app loads
        return {k: go.Figure(data=[]) for k in ["scatter", "pie", 'bar', 'sun']}

    """isinstance used due to a dropdown single item is a string not a list object and requires to be given []"""
    """to present is as a list for .isin to read"""

    if n_clicks:
        if isinstance(yearpick, str):
            filtered_year = popAgeGroup()[popAgeGroup()['time'].isin([yearpick])]
        else:
            filtered_year = popAgeGroup()[popAgeGroup()['time'].isin(yearpick)]

        if isinstance(grouppicker, str):
            filtered_group = filtered_year[filtered_year['indic_de'].isin([grouppicker])]
        else:
            filtered_group = filtered_year[filtered_year['indic_de'].isin(grouppicker)]

        if isinstance(countrypick, str):
            filtered_country = filtered_group[filtered_group['geo'].isin([countrypick])]
        else:
            filtered_country = filtered_group[filtered_group['geo'].isin(countrypick)]

    traces = []
    traces2 = []
    traces3 = []

    for country_name in filtered_country['geo'].unique():
        df_by_country = filtered_country[filtered_country['geo'] == country_name]
        (go.Figure(
            traces3.append(go.Bar(
                x=df_by_country[df_by_country['geo'] == country_name]['time'],
                y=df_by_country[df_by_country['geo'] == country_name]['values'],
                textposition='auto',
                name=country_name,
                text=df_by_country['indic_de'],
                hoverinfo='name+text+x+y'
            )
            )
        )
        )
        """generating the scatter plot"""
        go.Figure(
            traces.append(go.Scatter(x=df_by_country[xaxis_name],
                                     y=df_by_country[yaxis_name],
                                     mode='markers',
                                     marker={'size': 14,
                                             'opacity': 0.5,
                                             'line': {'width': 1},
                                             },
                                     name=country_name,
                                     text=df_by_country['time'],
                                     hoverinfo='x+y+text'
                                     ))

        )

    """generating the Pie chart"""
    (go.Figure(
        traces2.append(go.Pie(
            name="pop",
            values=filtered_country[yaxis_name],
            labels=filtered_country[xaxis_name],
            textinfo='value+label'
        ))
    ))
    ''''filling pie figure with data and layout'''
    pie = {'data': traces2,
           'layout': go.Layout(
               title='% population from groups {} in the year {} '.format(grouppicker, yearpick),
               template=stylepick,
               height=800,
           )}
    ''''filling scatter figure with data and layout'''
    scatter = {'data': traces,
               'layout': go.Layout(
                   title='% population from groups {} in the year {} '.format(grouppicker, yearpick),
                   xaxis={'title': xaxis_name},
                   yaxis={'title': yaxis_name},
                   hoverlabel=dict(
                       bgcolor="white",
                       font_size=16
                   ),
                   template=stylepick,
                   hovermode='closest',
                   height=800,
                   autosize=True),
               }
    ''''filling bar figure with data and layout'''
    bar = {'data': traces3,
           'layout': go.Layout(
               title='% population from groups {} in the year {} '.format(grouppicker, yearpick),
               xaxis={'title': 'year'},
               yaxis={'title': '% of population'},
               template=stylepick,
               hoverlabel=dict(
                   bgcolor="white",
                   font_size=16
               ),
               hovermode='closest',
               height=800
           )}

    # save figures in a dictionary for sending to the dcc.Store
    return {"pie": pie, "scatter": scatter, "bar": bar}


@app.callback(Output('sunburstout', 'figure'),
              [Input('update-button', 'n_clicks')],
              [State('year-picker', 'value'),
               State('group-picker', 'value'),
               State('country-picker', 'value'),
               State('styles', 'value')
               ])
def gen_sunburst(clicks, yearpick, grouppicker, countrypick, stylepick):
    if clicks:
        if isinstance(yearpick, str):
            filtered_byyear = popAgeGroup()[popAgeGroup()['time'].isin([yearpick])]
        else:
            filtered_byyear = popAgeGroup()[popAgeGroup()['time'].isin(yearpick)]

        if isinstance(grouppicker, str):
            filter_bygroup = filtered_byyear[filtered_byyear['indic_de'].isin([grouppicker])]
        else:
            filter_bygroup = filtered_byyear[filtered_byyear['indic_de'].isin(grouppicker)]

        if isinstance(countrypick, str):
            filter_bycountry = filter_bygroup[filter_bygroup['geo'].isin([countrypick])]
        else:
            filter_bycountry = filter_bygroup[filter_bygroup['geo'].isin(countrypick)]
        ''''PX is being used rather then go.Sunburst due to px requirements fitting more easily with our
         requirements as go.Scatter required all possible parent relation ships to be given '''
        sunburstout = (px.sunburst(
            filter_bycountry,
            path=['time', 'geo', 'indic_de'],
            values='values',
            height=800,
            template=stylepick
        ))
        return sunburstout


def PageLayOut():
    layout = html.Div([
        nav,
        body
    ])
    return layout
