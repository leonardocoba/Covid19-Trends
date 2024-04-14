from dash import html, dcc  

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

# Static countries list
countries = ["USA", "India", "Italy", "Switzerland", "South Korea", "Global"]

home_page = html.Div(style={'display': 'flex', 'width': '100%'}, children=[
    html.Div(style={'width': '25%', 'font-size': '16px'}, children=[
        html.H2('Filters', style={'font-size': '20px'}),
        html.Label('Location:', style={'font-size': '18px'}),
        dcc.Dropdown(id='location-filter', options=[
            {'label': country, 'value': country} for country in countries
        ], multi=True),
        html.Label('Gender:', style={'font-size': '18px'}),
        dcc.Checklist(id='gender-filter', options=[
            {'label': 'Male', 'value': 'Male'},
            {'label': 'Female', 'value': 'Female'}
        ], value=['Male', 'Female']),
        html.Label('Age:', style={'font-size': '18px'}),
        dcc.RangeSlider(id='age-filter', min=1, max=100, value=[1, 100], marks={i: str(i) for i in range(0, 101, 10)}),
        html.Label('Mortality:', style={'font-size': '18px'}),
        dcc.Checklist(id='mortality-filter', options=[
            {'label': 'Infected', 'value': 'Infected'},
            {'label': 'Deaths', 'value': 'Deaths'}
        ], value=['Infected', 'Deaths']),
    ]),
    html.Div(style={'width': '75%'}, children=[
        html.H1('Tuberculosis Trends', style={'font-size': '24px'}),
        dcc.Graph(id='tuberculosis-graph'),
        html.H3(id='total-count', style={'font-size': '20px'}),
        html.P(id='graph-description', style={'font-size': '16px'}),
    ]),
])
