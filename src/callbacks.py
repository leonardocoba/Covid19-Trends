from dash import Input, Output, State, callback
from app import app
import pandas as pd
import plotly.express as px


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
    # Creating an empty DataFrame with the structure needed for the plot
    proportions_df = pd.DataFrame(columns=['Country', 'Gender', 'Mortality Status', 'Proportion'])
    
    # Creating an empty plot using the empty DataFrame
    fig = px.bar(proportions_df, x='Country', y='Proportion', color='Mortality Status', 
                 barmode='stack', facet_col='Gender', title='Tuberculosis Data Visualization',
                 category_orders={"Gender": ["Male", "Female"], "Mortality Status": ["Infected", "Deaths"]})
    
    # Setting static text as there's no data to count or describe
    total_count = "Total Count: 0"
    description = "The average age for the selected group is N/A. Compared to the complementary group, which has an average age of N/A."

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
