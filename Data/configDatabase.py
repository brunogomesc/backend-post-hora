import sqlalchemy as sa


def return_connection_pyodbc():
      
    conexao = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=tcp:localhost,1433;"
        "Database=PostAtAtime;"
        "UID=SA;"
        "PWD=A123456#;"
    )

    return conexao


def return_connection_pandas():

    engine = sa.create_engine('mssql+pymssql://SA:A123456#@localhost/PostAtAtime')
    return engine
