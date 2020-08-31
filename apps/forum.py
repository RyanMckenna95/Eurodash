import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from apps.navbar import Navbar
from app import app
from apps.signup import auth
import base64
import datetime
import pyrebase
from apps.signup import config
import io
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

nav = Navbar()

cred = credentials.Certificate('firebaseAdminConfig.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

body = dbc.Container(
    [
        html.H3('Forum'),
        html.Div(id='app-2-display-value'),
        html.H1(id='new-name'),
        dbc.Row([
            dbc.Col(dbc.FormGroup([
                dbc.Label('Title'),
                dbc.Input(id='documentnm', type="text")
            ])
            ),
            dbc.Col(dbc.FormGroup([
                dbc.Label('Overview'),
                dbc.Input(id='overviewin', type="text")
            ])
            ),
            dbc.Col(dbc.FormGroup([
                dbc.Label('Post'),
                dbc.Textarea(id='posttxt')
            ])

            ),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Button(id='makepost', n_clicks=0,
                           children='Make Post',
                           color='primary',
                           className='mr-1',
                           block=True)
            ]),
            dbc.Col([
                dbc.Button(id='viewist', n_clicks=0,
                           children='view list',
                           color='primary',
                           className='mr-1',
                           block=True)
            ]),
        ]),
        dbc.Row([
            html.Div(id='output1', )

        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col(
            html.Div(id='list-of' ,children=[

            ]),width={"size": 6, "offset": 3}
            )
        ]),
    ])


@app.callback(Output('output1', 'children'),
              [Input('makepost', 'n_clicks')],
              [State('documentnm', 'value'),
               State('overviewin', 'value'),
               State('posttxt', 'value'),
               ])
def make_post(n_click, doc, titl, posttxt, ):
    if n_click:
        '''posting a document to the forum collection after the post button is clicked'''
        post = db.collection('forum').document(doc)

        post.set({
            'overview': titl,
            'post': posttxt,
        })
        return 'posted'


@app.callback(Output('list-of', 'children'),
              [Input('viewist', 'n_clicks')])
def retrun_list(n):
    if n:
        list = db.collection('forum')
        '''requesting documents in the forum collection'''
        docs = list.stream()
        index=[]
        '''creating an array of cards with the data returned from docs'''
        for doc in docs:
           index.append(dbc.Col(children=[
               dbc.Card([
                   dbc.CardBody([
                       html.H3('title: {}'.format(doc.id), className='card-title'),
                       html.P('title: {}'.format(doc.to_dict()),className="card-text")
                       ])
               ])
               ])
           )

        return index



def PageLayOut():
    layout = html.Div([
        nav,
        body
    ])
    return layout
