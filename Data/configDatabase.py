import sqlalchemy as sa


def return_connection_pyodbc():
      
    conexao = (
        "Driver={SQL Server};"
        "Server=BRUNO-COSTA\SQL_PROJECTS;"
        "Database=PostNaHora;"
        "User=sql_app;"
        "Password=2486teste;"
    )

    return conexao


def return_connection_pandas():

    engine = sa.create_engine('mssql+pymssql://sql_app:2486teste@BRUNO-COSTA\SQL_PROJECTS/PostNaHora')
    return engine
