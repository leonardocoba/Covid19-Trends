from dash import html, dcc  
from query import QueryObject

query_obj = QueryObject()

login_page = html.Div(
    children=[
        html.H2("Tuberculosis Trends", className="login-title"),
        html.Div(
            children=[
                html.Div(dcc.Input(id='username', type='text', placeholder='Username', className="login-input"), className="input-container"),
                html.Div(dcc.Input(id='password', type='password', placeholder='Password', className="login-input"), className="input-container"),
                html.Button('Login', id='login-button', className="login-button"),
                html.Button("Don't have an account? Sign up", id='signup-button', className="signup-button"),
            ],
            className="login-form"
        ),
    ],
    className="login-page-container"
)


home_page = html.Div(style={'display': 'flex'}, children=[
    html.Div(style={'flex': 1}, children=[
        html.H2('Filters'),
        html.Label('Location:'),
        dcc.Dropdown(id='location-filter', options=[
            {'label': country, 'value': country} for country in query_obj.data['Country'].unique()
        ], multi=True),
        html.Label('Gender:'),
        dcc.Checklist(id='gender-filter', options=[
            {'label': 'Male', 'value': 'Male'},
            {'label': 'Female', 'value': 'Female'}
        ], value=['Male', 'Female']),
        html.Label('Age:'),
        dcc.RangeSlider(id='age-filter', min=1, max=100, value=[1, 100], marks={i: str(i) for i in range(0, 101, 10)}),
        html.Label('Mortality:'),
        dcc.Checklist(id='mortality-filter', options=[
            {'label': 'Infected', 'value': 'Infected'},
            {'label': 'Deaths', 'value': 'Deaths'}
        ], value=['Infected', 'Deaths']),
    ]),
    html.Div(style={'flex': 2}, children=[
        html.H1('Tuberculosis Trends'),
        dcc.Graph(id='tuberculosis-graph'),
        html.H3(id='total-count'),
        html.P(id='graph-description'),
    ]),
])
