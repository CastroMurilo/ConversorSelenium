# Bibliotecas necessárias
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
import os
import time
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import csv  

script_dir = os.path.dirname(os.path.realpath(__file__))
log_file_path = os.path.join(script_dir, 'cotacoes.log')

if not os.path.exists(log_file_path):
    with open(log_file_path, 'w') as log_file:
        log_file.write(f'Criação do arquivo cotacoes.log em {datetime.now()}\n')

logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)

logging.getLogger('').addHandler(console_handler)

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')

nav = webdriver.Firefox(options=options)

moedas = ["Euro", "Dolar americano", "Libra esterlina", "Peso argentino"]

cotacoes_dir = os.path.join(script_dir, 'cotacoes')
if not os.path.exists(cotacoes_dir):
    os.makedirs(cotacoes_dir)

filename = os.path.join(cotacoes_dir, 'cotacoes.csv')
if not os.path.exists(filename):
    
    header = ['Data e Hora', 'Moeda', 'Cotacao']
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow(header)

try:
    while True:  
        for moeda in moedas:
            try:
                nav.get('https://www.google.com/')
                wait = WebDriverWait(nav, 10)  
                search_box = wait.until(EC.visibility_of_element_located((By.NAME, 'q')))
                search_box.send_keys(f'{moeda} converter Real', Keys.ENTER)
                
                resultado_moeda = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.DFlfde.SwHCTb'))).text
                data_moeda = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.k0Rg6d.hqAUc'))).text
                print(moeda, resultado_moeda, data_moeda)
                
                resultado_moeda = resultado_moeda.replace('R$ ', 'R$').replace('.', '').replace(',', '.')
                
                data = {'Data e Hora': [data_moeda], 'Moeda': [moeda], 'Cotacao': [resultado_moeda]}
                tabela = pd.DataFrame(data)
               
                tabela.to_csv(filename, mode='a', header=not os.path.exists(filename), index=False, sep=';', encoding='utf-8')

            except Exception as e:
                logging.error(f'Erro ao buscar informações de {moeda}: {str(e)}')
                print(f'Erro ao buscar informações de {moeda}: {str(e)}')
        
        time.sleep(3600)

except Exception as e:
    logging.error(f'Erro ao iniciar o navegador: {str(e)}')
    print(f'Erro ao iniciar o navegador: {str(e)}')
finally:
    nav.quit()
