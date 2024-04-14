import cx_Oracle
import pandas as pd

def init_oracle_client():
    cx_Oracle.init_oracle_client(lib_dir="location")
    print("Oracle client initialized successfully.")

def get_database_connection():
    dsn = cx_Oracle.makedsn("oracle.cise.ufl.edu", 1521, sid="orcl")
    conn = cx_Oracle.connect(user="user", password="pass", dsn=dsn)
    print("Successfully connected to the database.")
    return conn

def query_data(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()

def get_country_data(cursor, countries):
    frames = []
    base_query = {
        'Switzerland': "SELECT * FROM PhillipsJames.SWITZAGEDISTRIBUTION",  # Updated table name
        'South Korea': "SELECT * FROM PhillipsJames.SouthKoreaTimeAge",
        'India': """
            SELECT RECORDDATE AS "Date", STATE AS "State", TOTALSAMPLES AS "Samples", POSITIVE AS "Positive", 'Testing' AS "Type"
            FROM PhillipsJames.IndiaStateTestingCovid19
            UNION ALL
            SELECT UPDATEDON AS "Date", STATE AS "State", TOTALDOSESADMINISTERED AS "Samples", NULL AS "Positive", 'Vaccination' AS "Type"
            FROM PhillipsJames.IndiaStateVaccineCovid19
        """,
        'Italy': "SELECT * FROM PhillipsJames.ItalyProvinceCovid19",
        'USA': "SELECT * FROM PhillipsJames.USTimeSeriesCovid19",
        'Global': "SELECT * FROM PhillipsJames.GlobalTimeSeriesCovid19"
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
