from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, os, random


def userAutenticate(user, password):
    status = 0

    chrome_options = Options()

    chrome_options.add_argument("--headless")

    navegador = webdriver.Chrome("chromedriver.exe", options=chrome_options)

    navegador.get("https://www.instagram.com/")

    time.sleep(2)

    navegador.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(user)

    navegador.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(password)

    navegador.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()

    time.sleep(2)

    errorAlert = navegador.find_elements_by_xpath('//*[@id="slfErrorAlert"]')

    if len(errorAlert) == 0:
        status = 1

    navegador.close()

    return {"autenticate": status}


def alterFilename(idUser, date, time, networkActive, filename):
    arquivo, extensao = os.path.splitext(filename)
    new_date = ''.join(filter(str.isalnum, date)) 
    new_time = ''.join(filter(str.isalnum, time)) 
    new_filename = str(idUser) + '_' + str(networkActive) +  '_' +  str(new_date) + '_' + str(new_time) + str(extensao)
    return new_filename


def validateIsVideos(filename):
    if filename == '.MP4' or filename == '.mp4':
        return True
    else:
        return False
