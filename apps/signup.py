import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from apps.navbar import Navbar
from app import app
import pyrebase
from getpass import getpass
from app import app
from flask import session
from functools import wraps

config = {
    "apiKey": "AIzaSyBiJDSJs-ObnzZfassrwGsDzyqkoKop2_k",
    "authDomain": "eurodash.firebaseapp.com",
    "databaseURL": "https://eurodash.firebaseio.com",
    "projectId": "eurodash",
    "storageBucket": "eurodash.appspot.com",
    "messagingSenderId": "443957669997",
    "appId": "1:443957669997:web:a40dd36221c2bf14024f64",
    "measurementId": "G-1R32N6EL83"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

body = html.Div(
    [
        dbc.Card([dbc.CardBody(dbc.Form([

            dbc.FormGroup([
                dbc.Label('Email', html_for='emailup'),
                dbc.Input(
                    type='email',
                    id='emailup',
                    placeholder='enter email',
                )
            ]),
            dbc.FormGroup([
                dbc.Label('Password', html_for='emailup'),
                dbc.Input(
                    type='password',
                    id='passup',
                    placeholder='enter password',
                )]),
            dbc.Button('Sign up', id='signinbtn', color='primary', n_clicks=0),
            html.H1(id='returnmsgup')
        ])
        )
        ], style={"width": "18rem"},
        )
    ])


@app.callback(Output('returnmsgup', 'children'),
              [Input('signinbtn', 'n_clicks')],
              [State('emailup', 'value'),
               State('passup', 'value')])
def signup(n_clicks, email, password):
    if n_clicks:
        '''pyerbase creating a new user in firebase'''
        user = auth.create_user_with_email_and_password(email, password)
        auth.send_email_verification(user['idToken'])

    if n_clicks:
        return 'success...{}'.format(email)
    else:
        return ''


def PageLayOut():
    layout = html.Div([
        body
    ])
    return layout
