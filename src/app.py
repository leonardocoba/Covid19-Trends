# Import necessary libraries
import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Sample data for demonstration
df = pd.DataFrame({
    "Date": pd.date_range(start='1/1/2020', periods=100),
    "Value": (pd.Series(range(100)) + pd.Series(range(100)).apply(lambda x: x * 0.1)) ** 2
})

# Create a Plotly Express figure
fig = px.line(df, x='Date', y='Value', title='Tuberculosis Trends')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(style={'display': 'flex'}, children=[
    # Sidebar for filters
    html.Div(style={'flex': 1}, children=[
        html.H2('Filters'),
        html.Label('Location:'),
        dcc.Dropdown(id='location-filter', options=[
            {'label': 'Miami, Florida', 'value': 'MIA'},
            # Add other locations here
        ]),
        html.Label('Gender:'),
        dcc.Checklist(id='gender-filter', options=[
            {'label': 'Men', 'value': 'M'},
            {'label': 'Women', 'value': 'W'},
        ], value=['W']),
        html.Label('Age:'),
        dcc.RangeSlider(id='age-filter', min=1, max=100, value=[74, 100]),
        html.Label('Mortality:'),
        dcc.Checklist(id='mortality-filter', options=[
            {'label': 'Infected', 'value': 'INF'},
            {'label': 'Deaths', 'value': 'DTH'},
        ], value=['DTH']),
    ]),
    
    # Main content for Graph and Details
    html.Div(style={'flex': 2}, children=[
        html.H1('Tuberculosis'),
        dcc.Graph(id='tuberculosis-graph', figure=fig),
        html.H3('Total Count: 29,402', id='total-count'),
        html.P('This graph shows the trends of Tuberculosis over time...', id='graph-description'),
    ])
])

# Entry point for running the app
if __name__ == '__main__':
    app.run_server(debug=True)
