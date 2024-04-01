import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px  # Correct import for Plotly Express
from query import QueryObject
import pandas as pd  # Ensure pandas is imported for DataFrame operations

app = dash.Dash(__name__)

# Initializing the query object
query_obj = QueryObject()

app.layout = html.Div(style={'display': 'flex'}, children=[
    # Sidebar filters
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
    # Graph and titles
    html.Div(style={'flex': 2}, children=[
        html.H1('Tuberculosis Trends'),
        dcc.Graph(id='tuberculosis-graph'),
        html.H3(id='total-count'),
        html.P(id='graph-description'),
    ]),
])

@app.callback(
    [Output('tuberculosis-graph', 'figure'),
     Output('total-count', 'children'),
     Output('graph-description', 'children')],
    [Input('location-filter', 'value'), Input('gender-filter', 'value'),
     Input('age-filter', 'value'), Input('mortality-filter', 'value')]
)
def update_graph_and_text(location, gender, age, mortality):
    filtered_data = query_obj.filter_data(gender=gender, age_range=age, country=location, mortality_status=mortality)

    # Creating a DataFrame to store the proportions
    proportions = []

    for country in filtered_data['Country'].unique():
        for gen in ['Male', 'Female']:
            for status in ['Infected', 'Deaths']:
                subset = filtered_data[(filtered_data['Country'] == country) & (filtered_data['Gender'] == gen) & (filtered_data['Mortality Status'] == status)]
                proportions.append({'Country': country, 'Gender': gen, 'Mortality Status': status, 'Proportion': len(subset)})

    proportions_df = pd.DataFrame(proportions)

    # Plotting
    fig = px.bar(proportions_df, x='Country', y='Proportion', color='Mortality Status', 
                 barmode='stack', facet_col='Gender', title='Tuberculosis Data Visualization',
                 category_orders={"Gender": ["Male", "Female"], "Mortality Status": ["Infected", "Deaths"]})

    # Update the total count
    total_count = f"Total Count: {len(filtered_data)}"
    
    # Calculate and update the dynamic description
    selected_avg_age = query_obj.calculate_average_age(filtered_data)
    complementary_avg_age = query_obj.calculate_complementary_average_age(gender=gender, country=location, mortality_status=mortality)
    description = f"The average age for the selected group is {selected_avg_age:.2f}. "
    description += f"Compared to the complementary group, which has an average age of {complementary_avg_age:.2f}."

    return fig, total_count, description

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
