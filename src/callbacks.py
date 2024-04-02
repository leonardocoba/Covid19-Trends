from dash import Input, Output, State, callback
from app import app
from query import QueryObject
import pandas as pd
import plotly.express as px

query_obj = QueryObject()

@app.callback(Output('url', 'pathname'), 
              [Input('login-button', 'n_clicks')],
              [State('username', 'value'), State('password', 'value')])
def login(n_clicks, username, password):
    if n_clicks and username == 'admin' and password == 'admin':
        return '/home'
    return '/'

@app.callback(
    [Output('tuberculosis-graph', 'figure'),
     Output('total-count', 'children'),
     Output('graph-description', 'children')],
    [Input('location-filter', 'value'), Input('gender-filter', 'value'),
     Input('age-filter', 'value'), Input('mortality-filter', 'value')]
)
def update_graph_and_text(location, gender, age, mortality):
    filtered_data = query_obj.filter_data(gender=gender, age_range=age, country=location, mortality_status=mortality)

    proportions = []
    for country in filtered_data['Country'].unique():
        for gen in ['Male', 'Female']:
            for status in ['Infected', 'Deaths']:
                subset = filtered_data[(filtered_data['Country'] == country) & (filtered_data['Gender'] == gen) & (filtered_data['Mortality Status'] == status)]
                proportions.append({'Country': country, 'Gender': gen, 'Mortality Status': status, 'Proportion': len(subset)})

    proportions_df = pd.DataFrame(proportions)
    fig = px.bar(proportions_df, x='Country', y='Proportion', color='Mortality Status', 
                 barmode='stack', facet_col='Gender', title='Tuberculosis Data Visualization',
                 category_orders={"Gender": ["Male", "Female"], "Mortality Status": ["Infected", "Deaths"]})

    total_count = f"Total Count: {len(filtered_data)}"
    selected_avg_age = query_obj.calculate_average_age(filtered_data)
    complementary_avg_age = query_obj.calculate_complementary_average_age(gender=gender, country=location, mortality_status=mortality)
    description = f"The average age for the selected group is {selected_avg_age:.2f}. Compared to the complementary group, which has an average age of {complementary_avg_age:.2f}."

    return fig, total_count, description

"""# Define a function to retrieve data from Oracle and update the graph
def update_graph():
    # Fetch data from the database
    query = "SELECT * FROM toycarorders"
    df = pd.read_sql(query, con=conn)
    
    # Plot the data (you can customize this based on your data)
    graph_data = {
        'x': df['x_column'],
        'y': df['y_column'],
        'type': 'bar',
        'name': 'Data from Oracle'
    }
    
    return {
        'data': [graph_data],
        'layout': {
            'title': 'Data from Oracle Database'
        }
    }

# Update the graph periodically
@app.callback(
    dash.dependencies.Output('tuberculosis-graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)"""
