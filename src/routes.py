import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"instant client path")

# Connect to the Oracle database
conn = cx_Oracle.connect(
    user="UF USERNAME",
    password="CISE oracle password",
    dsn=cx_Oracle.makedsn(host = 'oracle.cise.ufl.edu', port = '1521', sid = 'orcl')
)