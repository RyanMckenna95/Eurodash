import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from apps.navbar import Navbar
import pyrebase
from apps.signup import firebase
from getpass import getpass
from app import app
from apps import homepage

auth = firebase.auth()

body = html.Div(
    [
        dbc.Col([
            html.Hr(),
            dbc.Card([dbc.CardBody(dbc.Form([

                dbc.FormGroup([
                    dbc.Label('Email', html_for='emailin'),
                    dbc.Input(
                        type='email',
                        id='emailin',
                        placeholder='enter email',
                    )
                ]),
                dbc.FormGroup([
                    dbc.Label('Password', html_for='passin'),
                    dbc.Input(
                        type='password',
                        id='passin',
                        placeholder='enter password',
                    )]),
                dbc.Button('login', id='loginbtn', color='primary', n_clicks=0),
                html.Hr(),
                dcc.Link('create account', href='/apps/signup'),
                html.Hr(),
                html.H6(id='tokentest'),
            ])
            )
            ], style={"width": "18rem", 'offset': 3},
            ),
        ], width={"size": 6, "offset": 3}, )
    ])


@app.callback(Output('tokentest', 'children'),
              [Input('loginbtn', 'n_clicks')],
              [State('emailin', 'value'),
               State('passin', 'value')])
def login(n_clicks, email, password):
    if n_clicks:
        '''pyrebase connecting to an existing user'''
        user = auth.sign_in_with_email_and_password(email, password)
        if user is not None:
            return dcc.Link('success...{} '.format(email), href='/apps/homepage')
        else:
            return 'invalid'


def PageLayOut():
    layout = html.Div([
        body
    ])
    return layout
