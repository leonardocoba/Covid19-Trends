from dash import dcc, html, callback, Input, Output
from app import app
import layouts



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return layouts.home_page
    else:
        return layouts.login_page
import callbacks
if __name__ == '__main__':
    app.run_server(debug=True)
