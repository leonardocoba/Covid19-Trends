import cx_Oracle
import pandas as pd

def init_oracle_client():
    cx_Oracle.init_oracle_client(lib_dir="C:\\Users\\leona\\Downloads\\instantclient-basic-windows.x64-21.13.0.0.0dbru\\instantclient_21_13")   
    print("Oracle client initialized successfully.")

def get_database_connection():
    dsn = cx_Oracle.makedsn("oracle.cise.ufl.edu", 1521, sid="orcl")
    conn = cx_Oracle.connect(user="leonardocobaleda", password="c8UsBv8J4N5eXlDH9fEiaNjz", dsn=dsn)
    print("Successfully connected to the database.")
    return conn

def query_data(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()

def get_country_data(cursor, countries):
    frames = []
    base_query = {
        'Switzerland': "SELECT * FROM PhillipsJames.SWITZAGEDISTRIBUTION",  # Updated table name
        'South Korea': """SELECT 
        RECORDDATE, TIME, AGE, CONFIRMED AS TotalConfirmed, 
        DECEASED AS TotalDeaths
        FROM PhillipsJames.SouthKoreaTimeAge""",
        'India': """
        SELECT 
            STATE_UNIONTERRITORY AS "State",
            RECORDDATE AS "RecordDate",
            SUM(CONFIRMED) AS "TotalConfirmed",
            SUM(DEATHS) AS "TotalDeaths",
            SUM(CURED) AS "TotalRecovered"
        FROM 
            PhillipsJames.INDIASTATECOVID19
        GROUP BY 
            STATE_UNIONTERRITORY, RECORDDATE
        ORDER BY 
            RecordDate, STATE_UNIONTERRITORY
        """,
        'Italy': """
            SELECT 
                TO_DATE(RECORDDATE, 'YYYY-MM-DD"T"HH24:MI:SS') AS "RecordDate", 
                REGIONNAME AS "State", 
                TOTALPOSITIVECASES AS "TotalConfirmed"
            FROM 
                PhillipsJames.ItalyProvinceCovid19
        """,

        'USA': "SELECT * FROM PhillipsJames.USTimeSeriesCovid19",
        'Global': """
    SELECT 
        RecordDate AS "RecordDate",
        SUM(Confirmed) AS "TotalConfirmed",
        SUM(Deaths) AS "TotalDeaths",
        SUM(Recovered) AS "TotalRecovered"
    FROM 
        PhillipsJames.GLOBALDAILYCOVID19
    GROUP BY 
        RecordDate
    ORDER BY 
        RecordDate
    """,
    }
    for country in countries:
        print(f"Fetching data for {country}")
        rows = query_data(cursor, base_query[country])
        df = pd.DataFrame(rows, columns=[i[0] for i in cursor.description]) if rows else pd.DataFrame()
        frames.append(df)
    return frames

def main():
    init_oracle_client()
    conn = get_database_connection()
    cursor = conn.cursor()
    countries_input = input("Enter countries separated by comma (e.g., Switzerland, India): ")
    countries = [country.strip() for country in countries_input.split(',')]
    
    data_frames = get_country_data(cursor, countries)
    combined_df = pd.concat(data_frames, ignore_index=True, sort=False) if data_frames else pd.DataFrame()
    print("Combined DataFrame:")
    print(combined_df)
    
    cursor.close()
    conn.close()
    print("Database connection closed.")

if __name__ == "__main__":
    main()
