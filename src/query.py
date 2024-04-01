import pandas as pd
import numpy as np

class QueryObject:
    def __init__(self):
        self.data = self._generate_dummy_data()

    def _generate_dummy_data(self):
        np.random.seed(0)  # dummy data
        data = {
            'Age': np.random.randint(1, 100, size=100),
            'Country': np.random.choice(['Country A', 'Country B', 'Country C'], size=100),
            'Disease': 'Tuberculosis',
            'Mortality Status': np.random.choice(['Infected', 'Deaths'], size=100),
            'Gender': np.random.choice(['Male', 'Female'], size=100)
        }
        return pd.DataFrame(data)

    def filter_data(self, gender=None, age_range=None, country=None, mortality_status=None):
        df = self.data
        if gender:
            df = df[df['Gender'].isin(gender)]
        if age_range:
            df = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
        if country:
            df = df[df['Country'].isin(country)]
        if mortality_status:
            df = df[df['Mortality Status'].isin(mortality_status)]
        return df
    
    def calculate_average_age(self, df):
        return df['Age'].mean()

    def calculate_complementary_average_age(self, gender=None, country=None, mortality_status=None):
        df = self.data
        if gender:
            complementary_gender = {'Male': 'Female', 'Female': 'Male'}
            df = df[df['Gender'] == complementary_gender[gender[0]]]
        if country:
            df = df[~df['Country'].isin(country)]
        if mortality_status:
            complementary_status = {'Infected': 'Deaths', 'Deaths': 'Infected'}
            df = df[df['Mortality Status'] == complementary_status[mortality_status[0]]]
        return self.calculate_average_age(df)

