import cx_Oracle
import pandas as pd

class OracleDataBase:
    def __init__(self):
        self.conn = self.init_db_connection()
        self.cursor = self.conn.cursor()
        # Initialize data fetch for all countries at once if needed
        self.init_all_data()

    def init_db_connection(self):
        cx_Oracle.init_oracle_client(lib_dir="C:\\Users\\leona\\Downloads\\instantclient-basic-windows.x64-21.13.0.0.0dbru\\instantclient_21_13")
        dsn = cx_Oracle.makedsn("oracle.cise.ufl.edu", 1521, sid="orcl")
        conn = cx_Oracle.connect(user="leonardocobaleda", password="c8UsBv8J4N5eXlDH9fEiaNjz", dsn=dsn)
        print("Database connection initialized successfully.")
        return conn


    def init_all_data(self):
        self.IndiaData = self.fetch_india_data()
        self.USAData = self.fetch_usa_data()
        self.GlobalData = self.fetch_global_data()
        self.ItalyData = self.fetch_italy_data()
        self.SouthKoreaAgeData = self.fetch_skage_data()
        self.SouthKoreaGenderData = self.fetch_skgender_data()
        self.SouthKoreaProvinceData = self.fetch_skgprovince_data()
        #self.BrazilData = self.fetch_brazil_data()

    def fetch_brazil_data(self):
        query = """
        SELECT 
            NAME AS "State",
            RECORDDATE AS "RecordDate",
            SUM(CASES) AS "TotalConfirmed",
            SUM(DEATHS) AS "TotalDeaths",
            CASE 
                WHEN SUM(CASES) = 0 OR SUM(DEATHS) = 0 THEN 0
                ELSE SUM(DEATHS) * 1.0 / SUM(CASES)
            END AS "MortalityRate"
        FROM 
            PhillipsJames.BRAZILCITIESDAILYCOVID19
        GROUP BY 
            NAME, RECORDDATE
        ORDER BY 
            "RecordDate", "State"

        """
        return self.query_data(query)

    def fetch_india_data(self):
        query = """
        SELECT 
            STATEUNIONTERRITORY AS "State",
            RECORDDATE AS "RecordDate",
            SUM(CONFIRMED) AS "TotalConfirmed",
            SUM(DEATHS) AS "TotalDeaths",
            SUM(CURED) AS "TotalRecovered",
            CASE 
                WHEN SUM(CONFIRMED) = 0 OR SUM(DEATHS) = 0 THEN 0
                ELSE SUM(DEATHS) * 1.0 / SUM(CONFIRMED)
            END AS "MortalityRate"
        FROM 
            PhillipsJames.INDIASTATECOVID19
        GROUP BY 
            STATEUNIONTERRITORY, RECORDDATE
        ORDER BY 
            RecordDate, STATEUNIONTERRITORY
        """
        return self.query_data(query)

    def fetch_global_data(self):
        query = """
        SELECT 
            RECORDDATE AS "RecordDate",
            COUNTRYREGION AS "State",
            SUM(CONFIRMED) AS "TotalConfirmed",
            SUM(DEATHS) AS "TotalDeaths",
            SUM(RECOVERED) AS "TotalRecovered",
            CASE 
                WHEN SUM(CONFIRMED) = 0 OR SUM(DEATHS) = 0 THEN 0
                ELSE SUM(DEATHS) * 1.0 / SUM(CONFIRMED)
            END AS "MortalityRate"
        FROM 
            PhillipsJames.GLOBALDAILYCOVID19
        GROUP BY 
            RECORDDATE, COUNTRYREGION
        ORDER BY 
            "RecordDate", "State"

        """
        return self.query_data(query)

    def fetch_skage_data(self):
        # age
        query = """
        SELECT
            RECORDDATE AS "RecordDate",
            AGE AS "Age",
            CONFIRMED AS "TotalConfirmed",
            DECEASED AS "TotalDeaths",
            CASE 
                WHEN CONFIRMED = 0 OR DECEASED = 0 THEN 0
                ELSE DECEASED * 1.0 / CONFIRMED
            END AS "MortalityRate"
        FROM
            PhillipsJames.SouthKoreaTimeAge
        """
        return self.query_data(query)
    def fetch_skgender_data(self):
        query = """
        SELECT
            RECORDDATE AS "RecordDate",
            SEX AS "Gender",
            CONFIRMED AS "TotalConfirmed",
            DECEASED AS "TotalDeaths",
            CASE 
                WHEN CONFIRMED = 0 OR DECEASED = 0 THEN 0
                ELSE DECEASED * 1.0 / CONFIRMED
            END AS "MortalityRate"
        FROM
            PhillipsJames.SouthKoreaTimeGender
        """
        return self.query_data(query)
    
    def fetch_skgprovince_data(self):
        query = """
        SELECT
            RECORDDATE AS "RecordDate",
            PROVINCE AS "State",
            CONFIRMED AS "TotalConfirmed",
            DECEASED AS "TotalDeaths",
            RELEASED AS "TotalRecovered",
            CASE 
                WHEN CONFIRMED = 0 OR DECEASED = 0 THEN 0
                ELSE DECEASED * 1.0 / CONFIRMED
            END AS "MortalityRate"
        FROM
            PhillipsJames.SouthKoreaTimeProvince
        """
        return self.query_data(query)

    def fetch_italy_data(self): 
        query = """
        SELECT 
            TRUNC(TO_DATE(RECORDDATE, 'YYYY-MM-DD"T"HH24:MI:SS')) AS "RecordDate", 
            REGIONNAME AS "State",
            HOSPITALIZEDPATIENTS as "Hospitalized",
            INTENSIVECAREPATIENTS as "IntensiveCare",
            RECOVERED as "TotalRecovered",
            DEATHS as "TotalDeaths",
            TOTALPOSITIVECASES AS "TotalConfirmed",
            CASE 
                WHEN TOTALPOSITIVECASES = 0 OR DEATHS = 0 THEN 0
                ELSE DEATHS * 1.0 / TOTALPOSITIVECASES
            END AS "MortalityRate"
        FROM 
            PhillipsJames.ItalyRegionCovid19
        """
        return self.query_data(query)
    

    def fetch_usa_data(self):
        query = """
        SELECT  
            RECORDDATE AS "RecordDate",
            RECORDSTATE as "State",
            POSITIVECASES AS "TotalConfirmed",
            DEATH AS "TotalDeaths",
            RECOVERED as "TotalRecovered",
            CASE 
                WHEN POSITIVECASES = 0 OR DEATH = 0 THEN 0
                ELSE DEATH * 1.0 / POSITIVECASES
            END AS "MortalityRate"
        FROM 
            PhillipsJames.USSTATESDAILYCOVID19"""""

        return self.query_data(query)


    def query_data(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return pd.DataFrame(rows, columns=[i[0] for i in self.cursor.description]) if rows else pd.DataFrame()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    db = OracleDataBase()
   
    
    print(db.SouthKoreaGenderData.head())
    print(db.SouthKoreaAgeData.head())
    print(db.SouthKoreaProvinceData.head())
    print(db.GlobalData.head())
