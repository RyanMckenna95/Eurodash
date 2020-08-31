import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import page1, page2, populationGoups, homepage, forum, signup,login

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

'''creating routes for the index to pass in different layouts'''
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/economy':
        return page1.PageLayOut()
    elif pathname == '/apps/page2':
        return page2.PageLayOut()
    elif pathname == '/apps/popgroups':
        return populationGoups.PageLayOut()
    elif pathname == '/apps/forum':
        return forum.PageLayOut()
    elif pathname == '/apps/homepage':
        return homepage.Homepage()
    elif pathname == '/apps/login':
        return login.PageLayOut()
    elif pathname == '/apps/signup':
        return signup.PageLayOut()
    else:
        return homepage.Homepage()


if __name__ == '__main__':
    app.run_server(debug=True)
