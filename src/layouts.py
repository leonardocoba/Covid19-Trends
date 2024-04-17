<<<<<<< Updated upstream
from dash import html, dcc  
from query import QueryObject

query_obj = QueryObject()
=======
from dash import html, dcc
from datetime import date
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
home_page = html.Div(style={'display': 'flex', 'width': '100%'}, children=[
    html.Div(style={'width': '25%', 'font-size': '16px'}, children=[
=======
countries = ["USA", "India", "Italy", "South Korea 1", "South Korea 2", "South Korea 3", "Global", "Brazil"]

home_page = html.Div(style={'display': 'flex', 'flexDirection': 'column', 'width': '100%', 'height': "100%"}, children=[
    html.Div(style={'width': '100%', 'font-size': '16px'}, children=[
>>>>>>> Stashed changes
        html.H2('Filters', style={'font-size': '20px'}),
        
        html.Label('Location:', style={'font-size': '18px'}),
        dcc.Dropdown(id='location-filter', options=[
<<<<<<< Updated upstream
            {'label': country, 'value': country} for country in query_obj.data['Country'].unique()
        ], multi=True),
        html.Label('Gender:', style={'font-size': '18px'}),
        dcc.Checklist(id='gender-filter', options=[
            {'label': 'Male', 'value': 'Male'},
            {'label': 'Female', 'value': 'Female'}
        ], value=['Male', 'Female']),
        html.Label('Age:', style={'font-size': '18px'}),
        dcc.RangeSlider(id='age-filter', min=1, max=100, value=[1, 100], marks={i: str(i) for i in range(0, 101, 10)}),
=======
            {'label': country, 'value': country} for country in countries
        ], placeholder="Select a Location"),
        
>>>>>>> Stashed changes
        html.Label('Mortality:', style={'font-size': '18px'}),
        dcc.Checklist(id='mortality-filter', options=[
            {'label': 'Infected', 'value': 'Infected'},
            {'label': 'Deaths', 'value': 'Deaths'},
            {'label': 'Cured', 'value': 'Cured'}
        ], value=['Infected', 'Deaths', 'Cured']),

        html.Label('Select Date Range:', style={'font-size': '18px'}),
        dcc.DatePickerRange(
            id='date-range-filter',
            min_date_allowed=date(2020, 1, 1),
            max_date_allowed=date(2021, 12, 31),
            start_date=date(2020, 1, 1),
            end_date=date(2021, 12, 31)
        ),
    ]),

    html.Div(style={'width': '100%', 'height': '50%'}, children=[
        html.H1('Covid19 Trends', style={'font-size': '24px'}),
        dcc.Graph(id='covid-graph'),
        html.H3(id='total-count', style={'font-size': '20px'}),
        html.P(id='graph-description', style={'font-size': '16px'}),
    ]),
    html.Div(style={'width': '100%', 'height': '50%'}, children=[
        html.H1('Rates', style={'font-size': '24px'}),
        dcc.Graph(id='rates-graph'),
        html.H3(id='total-count', style={'font-size': '20px'}),
        html.P(id='graph-description', style={'font-size': '16px'}),
    ]),
])
