"""
    O objetivo deste código é criar 2 arquivos de texto. Um contendo o nome das ações
    que fazem parte do índice Ibovespa e outro contendo as respectivas participações teóricas,
    tomando como base os dados atuais disponíveis no site da B3.
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

caminho = input('Onde deseja salvar os arquivos? ')

# abre o navegador
options = webdriver.ChromeOptions()
navegador = webdriver.Chrome(options=options)
navegador.minimize_window()

# pesquisa o site
navegador.get(r'https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br')
navegador.implicitly_wait(5)  # espera um tempo pra garantir que o site já foi carregado

# muda para a tabela com a porcentagem teórica
xpath1 = '//*[@id="divContainerIframeB3"]/div/div[2]/app-menu-portfolio/div/ul/li[1]/a'
teorica = navegador.find_element(By.XPATH, xpath1)  # acha o botão que muda pra tabela com a porcentagem teórica
teorica.click()  # muda a página para a tabela com a porcentagem teórica

# muda o número de linhas da tabela para 120
ide = 'selectPage'
muda_tamanho = navegador.find_element(By.ID, ide)  # encontra o botão de seleção da quantidade de linhas da tabela
seleciona_120 = Select(muda_tamanho)  # diz que o botão é uma lista de seleção
seleciona_120.select_by_visible_text('120')  # seleciona a opção 120
time.sleep(2)

# copia os elementos da tabela
xpath2 = '//*[@id="divContainerIframeB3"]/div/div[1]/form/div[3]/div/table'
tabela = navegador.find_element(By.XPATH, xpath2)  # pega os elementos da tabela
tabela_html = tabela.get_attribute('outerHTML')  # converte a tabela no formato X para uma estrutura html

df = pd.read_html(tabela_html)[0]  # cria um dataFrame a partir do html da tabela
navegador.quit()  # fecha o navegador

df.columns = ['ticker', 'acao', 'tipo', 'qtd', 'percent']  # altera o nome das colunas

try:  # se já não existir um arquivo no diretório com o nome desejado
    empresas = open(fr'{caminho}\acoes.txt', 'x')  # criar um arquivo chamado acoes.txt

except FileExistsError:  # se existir
    empresas = open(fr'{caminho}\acoes.txt', 'w')  # abre o arquivo acoes.txt para escrita

for c in df['ticker'][:len(df['ticker'])-2]:
    empresas.write(f'{c}\n')  # escreve as ações do Ibovespa no arquivo, uma em cada linha
empresas.close()  # fecha o arquivo

try:  # se já não existir um arquivo no diretório com o nome desejado
    por_teorica = open(fr'{caminho}\porcentagem_teorica.txt', 'x')   # criar um arquivo chamado porcentagem_teorica.txt

except FileExistsError:  # se existir
    por_teorica = open(fr'{caminho}\porcentagem_teorica.txt', 'w')  # abre arquivo porcentagem_teorica.txt para escrita

for c in df['percent'][:len(df['ticker'])-2]:
    por_teorica.write(f'{str(c/1000).replace(".", ",")}\n')  # escreve as porcentagens no arquivo, uma em cada linha
por_teorica.close()  # fecha o arquivo

print('\nNome dos arquivos: acoes.txt e porcentagem_teorica.txt')
print('Obs: os valores no porcentagem_teorica.txt já "estão em porcentagem"')
