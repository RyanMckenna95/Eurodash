import dash
from flask import Flask
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from apps import navbar

light = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/cosmo/bootstrap.min.css"

server = Flask(__name__)
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[light])



