from dash import Input, Output, callback, State
from app import app
from query import OracleDataBase
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Initialize your database connection
db = OracleDataBase()

@app.callback(Output('url', 'pathname'), 
              [Input('login-button', 'n_clicks')],
              [State('username', 'value'), State('password', 'value')])
def login(n_clicks, username, password):
    if n_clicks and username == 'admin' and password == 'admin':
        return '/home'
    return '/'

@callback(
    Output('mortality-filter', 'options'),
    [Input('location-filter', 'value')]
)
def update_mortality_options(selected_location):
    dataframes = {
        "USA": db.USAData,
        "India": db.IndiaData,
        "Italy": db.ItalyData,
        "South Korea 1": db.SouthKoreaAgeData,
        "South Korea 2": db.SouthKoreaGenderData,
        "South Korea 3": db.SouthKoreaProvinceData,
        "Global": db.GlobalData,
        "Brazil": db.BrazilData,
    }
    
    # Basic options for Infection and Mortality Rates if they exist in the dataframe
    base_options = [
        {'label': 'Infected', 'value': 'Infected'}, 
        {'label': 'Deaths', 'value': 'Deaths'},
        {'label': 'Mortality Rate', 'value': 'MortalityRate'},
        {'label': 'Infection Rate', 'value': 'InfectionRate'}
    ]

    # Additional metrics specific to certain locations
    if selected_location == 'Italy':
        base_options.extend([
            {'label': 'Hospitalized Rate', 'value': 'HospitalizedRate'},
            {'label': 'Intensive Care Rate', 'value': 'IntensiveCareRate'}
        ])
    elif selected_location == 'USA':
        base_options.extend([
            {'label': 'Population Density', 'value': 'PopulationDensity'},
        ])
    
    return base_options

@callback(
    Output('covid-graph', 'figure'),
    [Input('location-filter', 'value'),
     Input('mortality-filter', 'value'),
     Input('date-range-filter', 'start_date'),
     Input('date-range-filter', 'end_date')]
)
def update_covid_graph(selected_location, selected_metrics, start_date, end_date):
    dataframes = {
        "USA": db.USAData,
        "India": db.IndiaData,
        "Italy": db.ItalyData,
        "South Korea 1": db.SouthKoreaAgeData,
        "South Korea 2": db.SouthKoreaGenderData,
        "South Korea 3": db.SouthKoreaProvinceData,
        "Global": db.GlobalData,
        "Brazil": db.BrazilData,
    }
    df = dataframes.get(selected_location, pd.DataFrame())
    if df.empty:
        return px.line(title="No data available for the selected location.")

    df['RecordDate'] = pd.to_datetime(df['RecordDate'])
    mask = (df['RecordDate'] >= start_date) & (df['RecordDate'] <= end_date)
    filtered_df = df.loc[mask]

    if filtered_df.empty:
        return px.line(title="No data available for the selected date range.")

    y_data = {
        'Infected': 'TotalConfirmed',
        'Deaths': 'TotalDeaths',
    }

    y_values = [y_data[metric] for metric in selected_metrics if metric in y_data]

    if not y_values:
        return px.line(title="No metrics selected. Please select a metric to display data.")

    color_column = 'State' if selected_location not in ["South Korea 1", "South Korea 2"] else 'Age' if selected_location == "South Korea 1" else 'Gender'

    fig = px.line(filtered_df, x='RecordDate', y=y_values, color=color_column, title=f'COVID Trends Over Time for {selected_location}', labels={'value': 'Cases', 'variable': 'Type', 'RecordDate': 'Date'})
    fig.update_layout(xaxis_title='Date', yaxis_title='Number of Cases', legend_title=color_column)
    return fig




@app.callback(
    Output('rates-graph', 'figure'),
    [Input('location-filter', 'value'),
     Input('mortality-filter', 'value'),
     Input('date-range-filter', 'start_date'),
     Input('date-range-filter', 'end_date')]
)
def update_rates_graph(selected_location, selected_metrics, start_date, end_date):
    dataframes = {
        "USA": db.USAData,
        "India": db.IndiaData,
        "Italy": db.ItalyData,
        "South Korea 1": db.SouthKoreaAgeData,
        "South Korea 2": db.SouthKoreaGenderData,
        "South Korea 3": db.SouthKoreaProvinceData,
        "Global": db.GlobalData,
        "Brazil": db.BrazilData,
    }

    df = dataframes.get(selected_location, pd.DataFrame())
    if df.empty:
        return go.Figure(layout=go.Layout(title="No Data Available"))

    df['RecordDate'] = pd.to_datetime(df['RecordDate'])
    df_filtered = df[(df['RecordDate'] >= pd.to_datetime(start_date)) & (df['RecordDate'] <= pd.to_datetime(end_date))]
    if df_filtered.empty:
        return go.Figure(layout=go.Layout(title="No Data Available for the Selected Date Range"))

    fig = go.Figure()

    if selected_location == 'Italy':
        italy_special_metrics = ['HospitalizedRate', 'IntensiveCareRate']
        for metric in selected_metrics:
            if metric not in italy_special_metrics and metric in df_filtered.columns:
                plot_rates(df_filtered, fig, metric, selected_location) 
        for metric in italy_special_metrics:
            if metric in selected_metrics:
                plot_rates(df_filtered, fig, metric, selected_location)
        
    elif selected_location in ['South Korea 1', 'South Korea 2']:
        plot_all_categories(df_filtered, fig, selected_metrics)

    elif selected_location == 'USA':
        plot_usa_cases(df_filtered, fig, selected_metrics)
    else:
        for metric in selected_metrics:
            if metric in df_filtered.columns:
                plot_rates(df_filtered, fig, metric, selected_location)

    fig.update_layout(
        title=f"Rate Trends for {selected_location}",
        xaxis_title='Date',
        yaxis_title='Rate',
        legend_title='Metric/Category',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig

def plot_all_categories(df, fig, selected_metrics):
    # Determine the category column based on available data
    category_column = 'Age' if 'Age' in df.columns else 'Gender'
    # Plot data for each selected metric and category
    for metric in selected_metrics:
        if metric in df.columns:
            category_data = df.groupby([category_column, 'RecordDate'])[metric].mean().reset_index()
            for category in category_data[category_column].unique():
                data_to_plot = category_data[category_data[category_column] == category]
                fig.add_trace(go.Scatter(
                    x=data_to_plot['RecordDate'], 
                    y=data_to_plot[metric], 
                    mode='lines', 
                    name=f"{metric} - {category}"
                ))

def plot_rates(df, fig, rate_name, location):
    average_rate = df.groupby('State')[rate_name].mean().reset_index()
    top3 = average_rate.nlargest(3, rate_name)['State'].tolist()
    bottom3 = average_rate.nsmallest(3, rate_name)['State'].tolist()
    middle_index = len(average_rate) // 2
    middle3 = average_rate.iloc[middle_index-1:middle_index+2]['State'].tolist()

    existing_traces = {trace.name for trace in fig.data}

    # Add traces for top 3, checking for existing plots
    for i, state in enumerate(top3):
        trace_name = f"Top {i+1} {rate_name} - {state}"
        if trace_name not in existing_traces:
            state_data = df[df['State'] == state]
            fig.add_trace(go.Scatter(
                x=state_data['RecordDate'], 
                y=state_data[rate_name], 
                mode='lines', 
                name=trace_name
            ))

    # Add traces for bottom 3, checking for existing plots
    for i, state in enumerate(reversed(bottom3)):
        trace_name = f"Bottom {len(bottom3)-i} {rate_name} - {state}"
        if trace_name not in existing_traces:
            state_data = df[df['State'] == state]
            fig.add_trace(go.Scatter(
                x=state_data['RecordDate'], 
                y=state_data[rate_name], 
                mode='lines', 
                name=trace_name
            ))

    # Add traces for middle 3, checking for existing plots
    for state in middle3:
        trace_name = f"Middle {rate_name} - {state}"
        if trace_name not in existing_traces:
            state_data = df[df['State'] == state]
            fig.add_trace(go.Scatter(
                x=state_data['RecordDate'], 
                y=state_data[rate_name], 
                mode='lines', 
                name=trace_name
            ))

def plot_usa_cases(df, fig, selected_metrics):
    # Check if population density is a selected metric to plot high density states
    if 'PopulationDensity' in selected_metrics:
        plot_high_density_states(df, fig)
    for metric in selected_metrics:
        if metric != 'PopulationDensity' and metric in df.columns:
            plot_rates(df, fig, metric, 'USA')

def plot_high_density_states(df, fig):
    top_density_states = df.groupby('State')['PopulationDensity'].mean().nlargest(3).index
    df_top_density = df[df['State'].isin(top_density_states)]
    for index, state in enumerate(top_density_states, start=1):
        state_data = df_top_density[df_top_density['State'] == state]
        fig.add_trace(go.Scatter(
            x=state_data['RecordDate'], 
            y=state_data['InfectionRate'],  # Assuming 'InfectionRate' is an available column
            mode='lines',
            name=f"High Pop Density {index} - {state}"  # Adding enumeration here
        ))
