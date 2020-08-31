import time
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from apps.eurostatapi import popAgeGroup
from app import app
from apps.navbar import Navbar

nav = Navbar()

body = html.H4('Under construction')

features = popAgeGroup().columns


def PageLayOut():
    layout = html.Div([
        nav,
        body
    ])
    return layout
