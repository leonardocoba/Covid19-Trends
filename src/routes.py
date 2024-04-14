import cx_Oracle

# Initialize the Oracle client
cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\leona\Downloads\instantclient-basic-windows.x64-21.13.0.0.0dbru\instantclient_21_13")

try:
    # Establish a connection to the Oracle database
    conn = cx_Oracle.connect(
        user="leonardocobaleda",
        password="c8UsBv8J4N5eXlDH9fEiaNjz",
        dsn=cx_Oracle.makedsn(host='oracle.cise.ufl.edu', port='1521', sid='orcl')
    )
    print("Successfully connected to the database.")

    cursor = conn.cursor()

    query = "SELECT * FROM PhillipsJames.BrazilRegionCovid19"

    # Execute the query
    cursor.execute(query)

    for row in cursor:
        print(row)

except cx_Oracle.DatabaseError as e:
    error, = e.args
    print("Database connection failed.")
    print(f"Oracle-Error-Code: {error.code}")
    print(f"Oracle-Error-Message: {error.message}")

finally:
    # Ensure that the connection and cursor are closed
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
        print("Connection closed.")
