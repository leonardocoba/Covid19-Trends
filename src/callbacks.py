from dash import Input, Output, callback, State
from app import app
from query import OracleDataBase
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import query
import numpy as np


db = query.OracleDataBase()

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
        # "Brazil": db.BrazilData,
    }
    
    base_options = [{'label': 'Infected', 'value': 'Infected'}, {'label': 'Deaths', 'value': 'Deaths'}]
    special_options = []
    if selected_location == None:
        return base_options
    if 'TotalRecovered' in dataframes[selected_location].columns:
        special_options.append({'label': 'Cured', 'value': 'Cured'})

    if 'MortalityRate' in dataframes[selected_location].columns:
        special_options.append({'label': 'Mortality Rate', 'value': 'MortalityRate'})

    if selected_location == 'Italy':
        special_options.extend([
            {'label': 'Hospitalized Rate', 'value': 'HospitalizedRate'},
            {'label': 'Intensive Care Rate', 'value': 'IntensiveCareRate'}
        ])
    
    if selected_location in ['South Korea 1', 'South Korea 2']:  # Risk Ratio applicable to these locations
        special_options.append({'label': 'Risk Ratio', 'value': 'RiskRatio'})

    return base_options + special_options

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
        # "Brazil": db.BrazilData,
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
        # 'Cured': 'TotalRecovered' - not included in special cases
    }

    y_values = [y_data[metric] for metric in selected_metrics if metric in y_data]

    if not y_values:
        return px.line(title="No metrics selected. Please select a metric to display data.")

    # Adjust color grouping based on the selected location
    color_column = 'State'
    if selected_location == "South Korea 1":
        color_column = 'Age'
    elif selected_location == "South Korea 2":
        color_column = 'Gender'

    fig = px.line(filtered_df, x='RecordDate', y=y_values,
                  color=color_column,
                  title=f'COVID Trends Over Time for {selected_location}',
                  labels={'value': 'Cases', 'variable': 'Type', 'RecordDate': 'Date'})

    fig.update_layout(xaxis_title='Date',
                      yaxis_title='Number of Cases',
                      legend_title=color_column)
    return fig




@callback(
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
    }
    
    df = dataframes.get(selected_location, pd.DataFrame())
    if df.empty:
        return go.Figure(layout=go.Layout(title="No Data Available for the Selected Location"))

    df['RecordDate'] = pd.to_datetime(df['RecordDate'])
    df_filtered = df[(df['RecordDate'] >= pd.to_datetime(start_date)) & (df['RecordDate'] <= pd.to_datetime(end_date))]
    if df_filtered.empty:
        return go.Figure(layout=go.Layout(title="No Data Available for the Selected Date Range"))

    fig = go.Figure()

    # General mortality rate plots for non-special cases
    if selected_location not in ["South Korea 1", "South Korea 2", "Italy"]:
        if 'MortalityRate' in df_filtered.columns and 'MortalityRate' in selected_metrics:
            plot_mortality_rates(df_filtered, fig)

    # Special Case: Italy
    if selected_location == "Italy":
        if 'MortalityRate' in df_filtered.columns and 'MortalityRate' in selected_metrics:
            plot_mortality_rates(df_filtered, fig)

        # Calculate and plot Hospitalized Rate with top 3 and bottom 3 states
        if 'HospitalizedRate' in selected_metrics and 'Hospitalized' in df_filtered.columns:
            df_filtered['HospitalizedRate'] = df_filtered['Hospitalized'] / df_filtered['TotalConfirmed']
            # Calculating top 3 and bottom 3 states for Hospitalized Rate
            top3_hospitalized = df_filtered.groupby('State')['HospitalizedRate'].mean().nlargest(3).index
            bottom3_hospitalized = df_filtered.groupby('State')['HospitalizedRate'].mean().nsmallest(3).index
            
            # Adding traces for top 3 and bottom 3 Hospitalized Rates
            for state in top3_hospitalized:
                state_data = df_filtered[df_filtered['State'] == state]
                fig.add_trace(go.Scatter(x=state_data['RecordDate'], y=state_data['HospitalizedRate'], 
                                        mode='lines', name=f'{state}'))
            for state in bottom3_hospitalized:
                state_data = df_filtered[df_filtered['State'] == state]
                fig.add_trace(go.Scatter(x=state_data['RecordDate'], y=state_data['HospitalizedRate'], 
                                        mode='lines', name=f'{state}'))

        # Calculate and plot Intensive Care Rate with top 3 and bottom 3 states
        if 'IntensiveCareRate' in selected_metrics and 'IntensiveCare' in df_filtered.columns:
            df_filtered['IntensiveCareRate'] = df_filtered['IntensiveCare'] / df_filtered['TotalConfirmed']
            # Calculating top 3 and bottom 3 states for Intensive Care Rate
            top3_intensive = df_filtered.groupby('State')['IntensiveCareRate'].mean().nlargest(3).index
            bottom3_intensive = df_filtered.groupby('State')['IntensiveCareRate'].mean().nsmallest(3).index
            
            # Adding traces for top 3 and bottom 3 Intensive Care Rates
            for state in top3_intensive:
                state_data = df_filtered[df_filtered['State'] == state]
                fig.add_trace(go.Scatter(x=state_data['RecordDate'], y=state_data['IntensiveCareRate'], 
                                        mode='lines', name=f'{state}'))
            for state in bottom3_intensive:
                state_data = df_filtered[df_filtered['State'] == state]
                fig.add_trace(go.Scatter(x=state_data['RecordDate'], y=state_data['IntensiveCareRate'], 
                                        mode='lines', name=f'{state}'))


    # Special Case: South Korea 1 (Age Data)
    if selected_location == "South Korea 1":
        if 'MortalityRate' in df_filtered.columns and 'MortalityRate' in selected_metrics:
            # Plot mortality rate for each age group
            for age_group in df_filtered['Age'].unique():
                age_group_data = df_filtered[df_filtered['Age'] == age_group]
                fig.add_trace(go.Scatter(x=age_group_data['RecordDate'], y=age_group_data['MortalityRate'],
                                        mode='lines', name=f'Age {age_group}'))
            # Calculate and plot age risk ratio

    # Special Case: South Korea 2 (Gender Data)
    if selected_location == "South Korea 2":
        if 'MortalityRate' in df_filtered.columns and 'MortalityRate' in selected_metrics:
            # Plot mortality rate for each gender
            for gender in df_filtered['Gender'].unique():
                gender_data = df_filtered[df_filtered['Gender'] == gender]
                fig.add_trace(go.Scatter(x=gender_data['RecordDate'], y=gender_data['MortalityRate'],
                                        mode='lines', name=f'{gender} Mortality'))
            # Calculate and plot gender risk ratio
            

    fig.update_layout(
        title=f"Special Metrics and Mortality Rate Trends for {selected_location}",
        xaxis_title='Date',
        yaxis_title='Rate (%)',
        legend_title='Metric/Category',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig

def plot_mortality_rates(df, fig):
    average_mortality = df.groupby('State')['MortalityRate'].mean().reset_index()
    top5 = average_mortality.nlargest(3, 'MortalityRate')['State']
    bottom5 = average_mortality.nsmallest(3, 'MortalityRate')['State']
    middle5 = average_mortality.iloc[len(average_mortality)//2 - 2:len(average_mortality)//2 + 3]['State']
    states_of_interest = pd.concat([top5, bottom5, middle5])
    df_interest = df[df['State'].isin(states_of_interest)]
    for state in df_interest['State'].unique():
        df_state = df_interest[df_interest['State'] == state]
        fig.add_trace(go.Scatter(x=df_state['RecordDate'], y=df_state['MortalityRate'], mode='lines', name=state))


def plot_age_risk_ratio(df, fig):
    # Combine older age groups and compare to younger groups
    older = df[df['Age'].isin(['50s', '60s', '70s', '80s'])]['MortalityRate'].mean()
    younger = df[df['Age'].isin(['0s', '10s', '20s', '30s', '40s'])]['MortalityRate'].mean()
    risk_ratio = older / younger
    fig.add_trace(go.Scatter(x=df['RecordDate'], y=[risk_ratio]*len(df), mode='lines', name='Age Risk Ratio'))

def plot_gender_risk_ratio(df, fig):
    # Compare mortality rate between genders
    male_rate = df[df['Gender'] == 'Male']['MortalityRate'].mean()
    female_rate = df[df['Gender'] == 'Female']['MortalityRate'].mean()
    risk_ratio = male_rate / female_rate
    fig.add_trace(go.Scatter(x=df['RecordDate'], y=[risk_ratio]*len(df), mode='lines', name='Gender Risk Ratio'))
