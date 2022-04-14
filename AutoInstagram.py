from distutils.log import error
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, os, json

from sqlalchemy import false
from Data.configDatabase import return_connection_pyodbc
import pandas as pd
import pyodbc
from datetime import datetime


def postScheduleInstagramUnique(idQueue, user, password, fileName, legend):

      isVideo = false;

      status = 0

      #chrome_options = Options()

      #chrome_options.add_argument("--headless") , chrome_options=chrome_options

      navegador = webdriver.Chrome("chromedriver.exe")

      navegador.get("https://www.instagram.com/")

      time.sleep(2)

      navegador.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(user)

      navegador.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(password)

      navegador.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()

      time.sleep(10)

      errorAlert = navegador.find_elements_by_xpath('//*[@id="slfErrorAlert"]')

      if len(errorAlert) == 0:
            status = 1

            # não salvar infos de login
            navegador.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()

            time.sleep(10)

            # não salvar notificação
            navegador.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]/button[2]').click()

            time.sleep(10)

            # clicar no botão de postagem
            navegador.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/div/button/div').click()

            time.sleep(10)

            # faz upload do arquivo 
            navegador.find_element_by_xpath('/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/form/input').send_keys(os.path.abspath('./temp/' + str(fileName)))

            time.sleep(5)

            # da next no redimensionamento do arquivo
            navegador.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[3]/div/button').click()

            time.sleep(5)

            # da next nos filtros
            navegador.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[3]/div/button').click()

            time.sleep(5)

            # clica na textarea
            navegador.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea').click()

            # escreve a legenda
            navegador.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea').send_keys(legend)

            # da next nas legendas
            navegador.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[3]/div/button').click()

            if isVideo:
                  time.sleep(30)
            else:
                  time.sleep(10)

            status = updateSchedulesDatabase(idQueue=idQueue)

      
      else:
            print("Erro localizado - " + str(error))

      navegador.close()

      return {"autenticate": status}


def searchSchedules():

      dados_connection = return_connection_pyodbc()

      connection = pyodbc.connect(dados_connection)

      cursor = connection.cursor()

      query = "EXEC pr_Search_Schedules"

      cursor.execute(query)

      result = cursor.fetchall()

      return result


def updateSchedulesDatabase(idQueue):

      dados_connection = return_connection_pyodbc()

      connection = pyodbc.connect(dados_connection)

      cursor = connection.cursor()

      query = f"""EXEC pr_Update_Schedules @idQueue = {idQueue}"""

      cursor.execute(query)

      if cursor.rowcount >= 1:
            status = 1
      else:
            status = 0

      cursor.commit()

      cursor.close()

      return status


def home():
      result = searchSchedules()

      contador = 0

      while contador < len(result):
            if result[contador][1] <= str(datetime.today()):
                  if result[contador][5] == 'unique':
                        postScheduleInstagramUnique(idQueue=result[contador][0], user=result[contador][7],password=result[contador][8], fileName=result[contador][6], legend=result[contador][2])
                  else:
                        print("Postagem carousel")
            
            contador+=1
