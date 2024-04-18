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
                WHEN SUM(CASES) = 0 THEN 0
                ELSE ROUND(SUM(DEATHS) * 1.0 / SUM(CASES), 5)
            END AS "MortalityRate",
            CASE 
                WHEN POPULATION > 0 THEN
                    ROUND(SUM(CASES) * 1.0 / POPULATION, 5)
                ELSE 0
            END AS "InfectionRate"
        FROM 
            PhillipsJames.BRAZILCITIESDAILYCOVID19_P
        GROUP BY 
            NAME, RECORDDATE, POPULATION  
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
                WHEN SUM(CONFIRMED) = 0 THEN 0  
                ELSE SUM(DEATHS) * 1.0 / SUM(CONFIRMED)
            END AS "MortalityRate",
            CASE
                WHEN MAX(COUNTRYPOPULATION) > 0 THEN (SUM(CONFIRMED) * 1.0) / MAX(COUNTRYPOPULATION)
                ELSE 0
            END AS "InfectionRate"
        FROM 
            PhillipsJames.INDIASTATECOVID19_P
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
            END AS "MortalityRate",
            CASE 
                WHEN SUM(CONFIRMED) = 0 OR MAX(POPULATION) = 0 THEN 0
                ELSE SUM(CONFIRMED) * 1.0 / MAX(POPULATION)
            END AS "InfectionRate"
        FROM 
            PhillipsJames.GLOBALDAILYCOVID19_P
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
                WHEN CONFIRMED = 0 THEN 0
                ELSE DECEASED * 1.0 / CONFIRMED
            END AS "MortalityRate",
            CASE
                WHEN POPULATION = 0 OR POPULATION IS NULL THEN 0
                ELSE CONFIRMED * 1.0 / POPULATION
            END AS "InfectionRate"
        FROM
            PhillipsJames.SouthKoreaTimeAge_P

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
            END AS "MortalityRate",
            CASE 
                WHEN CONFIRMED = 0 OR GenderPopulation = 0 THEN 0
                ELSE Confirmed * 1.0 / GenderPopulation
            END AS "InfectionRate"
        FROM
            PhillipsJames.SouthKoreaTimeGender_p
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
            END AS "MortalityRate",
            CASE 
                WHEN CONFIRMED = 0 OR provincepopulation = 0 THEN 0
                ELSE confirmed * 1.0 / provincepopulation
            END AS "InfectionRate"
        FROM
            PhillipsJames.SouthKoreaTimeProvince_p
        """
        return self.query_data(query)

    def fetch_italy_data(self): 
        query = """
        SELECT 
            RECORDDATE AS "RecordDate", 
            REGIONNAME AS "State",
            HOSPITALIZEDPATIENTS as "Hospitalized",
            INTENSIVECAREPATIENTS as "IntensiveCare",
            RECOVERED as "TotalRecovered",
            DEATHS as "TotalDeaths",
            TOTALPOSITIVECASES AS "TotalConfirmed",
            CASE 
                WHEN TOTALPOSITIVECASES = 0 OR DEATHS = 0 THEN 0
                ELSE ROUND((DEATHS * 1.0 / TOTALPOSITIVECASES), 5)
            END AS "MortalityRate",
            CASE 
                WHEN PROVINCEPOPULATION > 0 THEN
                    ROUND((TOTALPOSITIVECASES * 1.0 / PROVINCEPOPULATION), 5)
                ELSE 0
            END AS "InfectionRate"
        FROM 
            PhillipsJames.ItalyRegionCovid19_P

        """
        return self.query_data(query)
    

    def fetch_usa_data(self):
        query = """
       SELECT
            RECORDDATE AS "RecordDate",
            RECORDSTATE as "State",
            POSITIVECASES AS "TotalConfirmed",
            COALESCE(DEATH, 0) AS "TotalDeaths",
            COALESCE(RECOVERED, 0) as "TotalRecovered",
            CASE 
                WHEN COALESCE(POSITIVECASES, 0) = 0 OR COALESCE(DEATH, 0) = 0 THEN 0  
                ELSE COALESCE(DEATH, 0) * 1.0 / COALESCE(POSITIVECASES, 0)  
            END AS "MortalityRate",
            CASE 
                WHEN COALESCE(POSITIVECASES, 0) = 0 OR COALESCE(Population, 0) = 0 THEN 0 
                ELSE COALESCE(POSITIVECASES, 0) * 1.0 / COALESCE(Population, 0)  
            END AS "InfectionRate",
            populationdensity AS "PopulationDensity"
        FROM 
            PhillipsJames.USSTATESDAILYCOVID19_pd

            """""

        return self.query_data(query)
    
    def top_middle_bottom(self, prior_query, start_date, end_date, group_by, comparison_point):
        query = """
            WITH
            ordered_groups AS (
                SELECT sub.*, SUM("{comparison_point}") OVER (PARTITION BY "{group_by}") as total, ROW_NUMBER() OVER (PARTITION BY "{group_by}" ORDER BY total) as row_num
                FROM ({prior_query}) sub
                WHERE RECORDDATE BETWEEN TO_DATE('{start_date}', 'YYYY-MM-DD') AND TO_DATE('{end_date}', 'YYYY-MM-DD')
            ),
            total_rows AS (
                SELECT COUNT(DISTINCT "{group_by}") as cnt FROM ordered_groups
            ),
            bottom_groups AS (
                SELECT * FROM ordered_groups
                WHERE row_num <= 3
            ),
            top_groups AS (
                SELECT * FROM ordered_groups
                WHERE row_num >= (SELECT cnt - 2 FROM total_rows)
            ),
            middle_groups AS (
                SELECT * FROM ordered_groups
                WHERE row_num BETWEEN (SELECT ROUND(cnt/2) - 1 FROM total_rows) AND (SELECT ROUND(cnt/2) + 1 FROM total_rows)
            )
            SELECT * FROM bottom_groups
            UNION ALL
            SELECT * FROM top_groups
            UNION ALL
            SELECT * FROM middle_groups
            ORDER BY total ASC
        """
        return self.query_data(query.format(prior_query=prior_query, start_date=start_date, end_date=end_date, group_by=group_by, comparison_point=comparison_point))
    
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
    
    
    print(db.IndiaData)
    print(db.USAData)
    print(db.GlobalData)
    print(db.ItalyData)
    print(db.SouthKoreaAgeData)
    print(db.SouthKoreaGenderData)
    print(db.SouthKoreaProvinceData)
    print(db.BrazilData)