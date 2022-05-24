"""
    Este código entra na página da B3 que fala sobre o Índice Ibovespa e baixa o arquivo que contém a composição teórica
"""
"""
    Desenvolvido por: Miguel Abdala
    GitHub: miguel-jar
    Rev: 0
    Data: 24/05/2022
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
var = webdriver.Chrome(options=options)

var.get(r'https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br')
var.maximize_window()
var.implicitly_wait(5)

comp = var.find_element(By.XPATH, '//*[@id="divContainerIframeB3"]/div/div[2]/app-menu-portfolio/div/ul/li[1]/a')
comp.click()

xpath = '//*[@id="divContainerIframeB3"]/div/div[1]/form/div[3]/div/div[2]/div/div/div[1]/div[2]/p/a'
download = var.find_element(By.XPATH, xpath)
download.click()
time.sleep(1.5)
var.quit()

print('O arquivo foi baixado com sucesso !!')
print('Acesse a pasta padrão de donwload do Chrome para encontrar o arquivo.')
