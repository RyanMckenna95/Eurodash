import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps.navbar import Navbar

logo = '../assets/Eurostat-logo.png'

nav = Navbar()

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Disclaimer"),
                        html.P(
                            """\
                            This is a dashboard web application. It is designed to allow users to visualise and generate
                             graphs from the data provided by EuroStat. It is part of a project and us still currently 
                             under construction with not all features yet working. No personal information will be recorded
                             of users. Please try the features and leave a post in the forum if there are any bugs needed to 
                             be reported."""
                        ),
                        dbc.Button("View Eurostat site", color="secondary",
                                   href='https://ec.europa.eu/eurostat/data/database'),
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        html.H2(),
                        html.Img(src=logo,height='200px',width='400px'
                        ),
                    ]
                ),
            ]
        )
    ],
    className="mt-4",
)


def Homepage():
    layout = html.Div([
        nav,
        body
    ])
    return layout



