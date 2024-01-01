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
import csv  # Adicionando a importação necessária para manipulação de CSV

# Obter o diretório atual do script
script_dir = os.path.dirname(os.path.realpath(__file__))
log_file_path = os.path.join(script_dir, 'cotacoes.log')

# Configurar o logger para registrar mensagens em um arquivo chamado 'cotacoes.log' e manipular para a exibição no arquivo
if not os.path.exists(log_file_path):
    with open(log_file_path, 'w') as log_file:
        log_file.write(f'Criação do arquivo cotacoes.log em {datetime.now()}\n')

logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatação do LOG
console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)

# Adicionar o manipulador ao LOG
logging.getLogger('').addHandler(console_handler)

# Configuração para navegador Firefox e modo headless
options = webdriver.FirefoxOptions()
options.add_argument('-headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')

# Inicia Firefox em modo headless fora do loop
nav = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)

# Lista de moedas para pesquisar
moedas = ["Euro", "Dolar americano", "Libra esterlina", "Peso argentino"]

# Verificar se a pasta 'cotacoes' existe, se não, criá-la
cotacoes_dir = os.path.join(script_dir, 'cotacoes')
if not os.path.exists(cotacoes_dir):
    os.makedirs(cotacoes_dir)

# Criar o arquivo CSV
filename = os.path.join(cotacoes_dir, 'cotacoes.csv')
if not os.path.exists(filename):
    # Cabeçalho do arquivo CSV
    header = ['Data e Hora', 'Moeda', 'Cotacao']
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow(header)

try:
    while True:  # Inicia um loop infinito
        for moeda in moedas:
            try:
                # Pesquisar pela moeda no Google
                nav.get('https://www.google.com/')
                wait = WebDriverWait(nav, 10)  # Ajuste o tempo limite conforme necessário
                search_box = wait.until(EC.visibility_of_element_located((By.NAME, 'q')))
                search_box.send_keys(f'{moeda} converter Real', Keys.ENTER)

                # Obter informações da moeda a partir do resultado da pesquisa
                resultado_moeda = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.DFlfde.SwHCTb'))).text
                data_moeda = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.k0Rg6d.hqAUc'))).text
                print(moeda, resultado_moeda, data_moeda)

                # Formatando os dados para o formato desejado
                resultado_moeda = resultado_moeda.replace('R$ ', 'R$').replace('.', '').replace(',', '.')

                # Criar um DataFrame com as informações
                data = {'Data e Hora': [data_moeda], 'Moeda': [moeda], 'Cotacao': [resultado_moeda]}
                tabela = pd.DataFrame(data)

                # Salvando o DataFrame como um arquivo CSV na pasta 'cotacoes'
                tabela.to_csv(filename, mode='a', header=not os.path.exists(filename), index=False, sep=';', encoding='utf-8')

            except Exception as e:
                # Registrar erro no log em caso de falha na extração de informações da moeda
                logging.error(f'Erro ao buscar informações de {moeda}: {str(e)}')
                # Imprimir mensagem de erro no console
                print(f'Erro ao buscar informações de {moeda}: {str(e)}')

        # Aguardar 1 hora antes de tentar novamente
        time.sleep(3600)

except Exception as e:
    # Registrar erro no log em caso de falha ao iniciar o navegador
    logging.error(f'Erro ao iniciar o navegador: {str(e)}')
    # Imprimir mensagem de erro no console
    print(f'Erro ao iniciar o navegador: {str(e)}')

finally:
    # Fechar o navegador após o término do loop
    nav.quit()
