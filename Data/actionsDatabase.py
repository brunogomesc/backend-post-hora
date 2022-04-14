from Data.configDatabase import return_connection_pyodbc, return_connection_pandas
import pyodbc
import pandas as pd


def insertUser(user, password, name, email):

    dados_connection = return_connection_pyodbc()

    connection = pyodbc.connect(dados_connection)

    cursor = connection.cursor()

    query = f"""EXEC pr_Create_User @User = '{str(user)}', @Password = '{str(password)}', 
            @Nome_User = '{str(name)}', @Email = '{str(email)}'"""

    cursor.execute(query)

    if cursor.rowcount >= 1:
        status = 1
    else:
        status = 0

    cursor.commit()

    cursor.close()

    json = {"status": status}

    return json


def authLogin():

    connection = return_connection_pandas()

    query = 'EXEC pr_Auth_User'

    df = pd.read_sql(query, connection)

    result_json = df.to_json(orient="records", date_format="json")

    return result_json


def insertUserNetwork(user, password, network, login):

    dados_connection = return_connection_pyodbc()

    connection = pyodbc.connect(dados_connection)

    cursor = connection.cursor()

    query = f"""EXEC pr_Save_User_Social_Network @User = '{str(user)}', @Password = '{str(password)}', 
            @Social_Network = {str(network)}, @Id_Login = {str(login)}"""

    cursor.execute(query)

    if cursor.rowcount >= 1:
        status = 1
    else:
        status = 0

    cursor.commit()

    cursor.close()

    json = {"status": status}

    return json


def authNetworksLogin(id_login):

    connection = return_connection_pandas()

    query = "EXEC pr_Auth_Social_Network_Save @id_login = %s"

    df = pd.read_sql(query, connection, params=[id_login])

    result_json = df.to_json(orient="records", date_format="json")

    return result_json


def savesScheduleDatabase(path, legend, date, time, typeSchedule, networkActive, idLogin, isVideos):
    video = 0

    if isVideos:
        video = 1

    dados_connection = return_connection_pyodbc()

    connection = pyodbc.connect(dados_connection)

    cursor = connection.cursor()

    query = f"""EXEC pr_Save_Schedule @Path = '{str(path)}', @Legend = '{str(legend)}', 
            @Date = '{str(date)} {str(time)}', @TypeSchedule = '{str(typeSchedule)}', @NetworkActive = '{str(networkActive)}',
            @IdLogin = {str(idLogin)}, @IsVideo = {str(video)}"""

    cursor.execute(query)

    cursor.commit()

    cursor.close()


def saveScheduleFiles(id_queue, filename):
    
    dados_connection = return_connection_pyodbc()

    connection = pyodbc.connect(dados_connection)

    cursor = connection.cursor()

    query = f"""EXEC pr_Save_Schedule_Files @Filename = '{str(filename)}', @IdQueue = {str(id_queue)}"""

    cursor.execute(query)

    if cursor.rowcount >= 1:
        status = 1
    else:
        status = 0

    cursor.commit()

    cursor.close()

    json = {"status": status}

    return json


def getIdQueue(idLogin, date, time, networkActive):
    connection = return_connection_pandas()

    query = "SELECT id_queue FROM tb_queue_schedule WHERE id_login = %s and date_schedule = %s and id_rede_social = (select id_rede_social from tb_rede_social (NOLOCK) where nome_rede_social = UPPER(%s))"

    datetime = str(date) + ' ' + str(time)

    df = pd.read_sql(query, connection, params=[((idLogin), (datetime), (networkActive))])

    result_json = df.to_json(orient="records", date_format="json")

    return result_json


def nextSchedules(id_login, network_active):
          
    connection = return_connection_pandas()

    query = """SELECT qs.id_queue, qs.legend, qs.date_schedule, rs.nome_rede_social FROM tb_queue_schedule qs (nolock)
                        inner join tb_rede_social rs (nolock)
                        on qs.id_rede_social = rs.id_rede_social
                        WHERE qs.id_login = %s
                        AND RS.nome_rede_social = UPPER(%s)
                        AND qs.posted = 0
                        ORDER BY qs.date_schedule ASC"""

    df = pd.read_sql(query, connection, params=[((id_login), (network_active))])

    result_json = df.to_json(orient="records", date_format="json")

    return result_json


def allSchedules(id_login, network_active):
          
    connection = return_connection_pandas()

    query = """SELECT qs.id_queue, qs.legend, qs.date_schedule, rs.nome_rede_social FROM tb_queue_schedule qs (nolock)
                        inner join tb_rede_social rs (nolock)
                        on qs.id_rede_social = rs.id_rede_social
                        WHERE qs.id_login = %s
                        AND RS.nome_rede_social = UPPER(%s)
                        AND qs.posted not in (2) 
                        ORDER BY qs.date_schedule ASC"""

    df = pd.read_sql(query, connection, params=[((id_login), (network_active))])

    result_json = df.to_json(orient="records", date_format="json")

    return result_json


def completedSchedules(id_login, network_active):
          
    connection = return_connection_pandas()

    query = """SELECT qs.id_queue, qs.legend, qs.date_schedule, rs.nome_rede_social FROM tb_queue_schedule qs (nolock)
                        inner join tb_rede_social rs (nolock)
                        on qs.id_rede_social = rs.id_rede_social
                        WHERE qs.id_login = %s
                        AND RS.nome_rede_social = UPPER(%s)
                        AND qs.posted in (1,3) 
                        ORDER BY qs.date_schedule ASC"""

    df = pd.read_sql(query, connection, params=[((id_login), (network_active))])

    result_json = df.to_json(orient="records", date_format="json")

    return result_json


def deleteScheduleDatabase(id_queue):
          
    dados_connection = return_connection_pyodbc()

    connection = pyodbc.connect(dados_connection)

    cursor = connection.cursor()

    queryQueue = f"""UPDATE tb_queue_schedule SET posted = 2 WHERE id_queue = {id_queue}"""

    queryFiles = f"""UPDATE tb_schedule_files SET posted = 2 WHERE id_queue = {id_queue}"""

    cursor.execute(queryFiles)

    cursor.execute(queryQueue)

    if cursor.rowcount >= 1:
        status = 1
    else:
        status = 0

    cursor.commit()

    cursor.close()

    json = {"status": status}

    return json


def updateScheduleDatabase(id_queue, date, time, legend):
          
    dados_connection = return_connection_pyodbc()

    connection = pyodbc.connect(dados_connection)

    cursor = connection.cursor()

    queryQueue = f"""UPDATE tb_queue_schedule SET legend = '{str(legend)}', date_schedule = '{str(date)} {str(time)}' WHERE id_queue = {id_queue}"""

    cursor.execute(queryQueue)

    if cursor.rowcount >= 1:
        status = 1
    else:
        status = 0

    cursor.commit()

    cursor.close()

    json = {"status": status}

    return json


def deleteNetworkDatabase(login_user, network):
          
    dados_connection = return_connection_pyodbc()

    connection = pyodbc.connect(dados_connection)

    cursor = connection.cursor()

    queryUser = f"""UPDATE tb_users SET ativo = 0 WHERE login_user = 'str{login_user}' 
                        and id_rede_social = (SELECT id_rede_social FROM tb_rede_social WHERE nome_rede_social = 'str{network}')"""

    cursor.execute(queryUser)

    if cursor.rowcount >= 1:
        status = 1
    else:
        status = 0

    cursor.commit()

    cursor.close()

    json = {"status": status}

    return json


def updateNetworkDatabase(user, network, password):
          
    dados_connection = return_connection_pyodbc()

    connection = pyodbc.connect(dados_connection)

    cursor = connection.cursor()

    queryUser = f"""EXEC pr_Update_Network @Login_User = 'str({user})', @password = 'str({password})', @network = 'str({network})' """

    cursor.execute(queryUser)

    if cursor.rowcount >= 1:
        status = 1
    else:
        status = 0

    cursor.commit()

    cursor.close()

    json = {"status": status}

    return json
