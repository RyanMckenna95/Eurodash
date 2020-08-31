import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State

logo = '../assets/EuroLogo.jpg'

dropdown = dbc.Row(
    [
        dbc.Col(dbc.DropdownMenu(
            label="Population tables",
            color='primary',
            children=[
                dbc.DropdownMenuItem('Population on 1 January ', href='/economy'),
                dbc.DropdownMenuItem('Population as a percentage of EU27', href='/apps/page2'),
                dbc.DropdownMenuItem('Population by age group', href='/apps/popgroups'),
                dbc.DropdownMenuItem('Population density', href='/apps/forum'),
                dbc.DropdownMenuItem('Forum', href='/apps/forum'),
            ],
            direction="down"
        )),
        dbc.Col(dbc.DropdownMenu(
            label="Immigration and Emigration tables",
            color='primary',
            children=[
                dbc.DropdownMenuItem('Immigration'),
                dbc.DropdownMenuItem('Emigration'),
            ],
            direction="down"
        )),
        dbc.Col(dbc.DropdownMenu(
            label="Health Tables",
            color='primary',
            children=[
                dbc.DropdownMenuItem('Healthy life years at birth by sex'),
                dbc.DropdownMenuItem('Life expectancy at age 65 by sex'),
            ],
            direction="down"
        )),
        dbc.Col(dbc.DropdownMenu(
            label="Economic Tables",
            color='primary',
            children=[
                dbc.DropdownMenuItem('Gross domestic product at market prices'),
                dbc.DropdownMenuItem('Compensation of employees'),
                dbc.DropdownMenuItem('Taxes on production and imports less subsidies'),
                dbc.DropdownMenuItem('GDP per capita in PPS'),
                dbc.DropdownMenuItem('Exports of goods and services in % of GDP'),
            ],
            direction="left"
        )),
    ],
    no_gutters=False,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)


def Navbar():
    navbar = dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=logo, height="100px"), style={'padding': '0px'}),
                        dbc.Col(dbc.NavbarBrand("EuroDash", className="ml-1")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/apps/homepage",
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(dropdown, id="navbar-collapse", navbar=True),
        ],
        color="dark",
        dark=True,
    )
    return navbar
