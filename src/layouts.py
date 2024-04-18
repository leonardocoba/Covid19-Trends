from dash import html, dcc
from datetime import date

login_page = html.Div(
    children=[
        html.H2("Covid19 Trends", className="login-title"),
        html.Div(
            children=[
                dcc.Input(id='username', type='text', placeholder='Username', className="login-input"),
                dcc.Input(id='password', type='password', placeholder='Password', className="login-input"),
                html.Button('Login', id='login-button', className="login-button"),
                html.Button("Don't have an account? Sign up", id='signup-button', className="signup-button"),
            ],
            className="login-form"
        ),
    ],
    className="login-page-container"
)

countries = ["USA", "India", "Italy", "South Korea 1", "South Korea 2", "South Korea 3", "Global", "Brazil"]

home_page = html.Div(className='home-page-container', children=[
    html.Div(className='filters-container', children=[
        html.H2('Filters', style={'font-size': '20px', 'color': 'white'}),
        html.Label('Location:', style={'font-size': '18px', 'color': 'white'}),
        dcc.Dropdown(id='location-filter', options=[
            {'label': country, 'value': country} for country in countries
        ], placeholder="Select a Location"),
        html.Label('Mortality:', style={'font-size': '18px', 'color': 'white'}),
        dcc.Checklist(id='mortality-filter', options=[
            {'label': 'Infected', 'value': 'Infected'},
            {'label': 'Deaths', 'value': 'Deaths'},
            {'label': 'Cured', 'value': 'Cured'},
            {'label': 'Mortality Rate', 'value': 'MortalityRate'},
            {'label': 'Hospitalized Rate', 'value': 'HospitalizedRate'},
            {'label': 'Intensive Care Rate', 'value': 'IntensiveCareRate'},
            {'label': 'Infection Rate', 'value': 'InfectionRate'},
            {'label': 'Population Density', 'value': 'PopulationDensity'}
        ], value=['Infected', 'Deaths', 'Cured', 'MortalityRate', 'HospitalizedRate', 'IntensiveCareRate', 'InfectionRate', 'PopulationDensity']),
        dcc.DatePickerRange(
            id='date-range-filter',
            min_date_allowed=date(2020, 1, 1),
            max_date_allowed=date(2021, 12, 31),
            start_date=date(2020, 1, 1),
            end_date=date(2021, 12, 31)
        ),
    ]),
    html.Div(className='graphs-container', children=[
        html.Div(className='graph', children=[
            html.H1('Covid19 Trends', style={'font-size': '24px', 'color': 'white'}),
            dcc.Graph(id='covid-graph'),
        ]),
        html.Div(className='graph', children=[
            html.H1('Rates', style={'font-size': '24px', 'color': 'white'}),
            dcc.Graph(id='rates-graph'),
        ]),
    ]),
])