# Bibliotecas necessárias
import logging  # Registra mensagens no log
from selenium import webdriver  # Navegação web
from selenium.webdriver.common.keys import Keys  # Interagir com teclas do teclado
from selenium.webdriver.common.by import By  # Para a espera explícita
from selenium.webdriver.support.ui import WebDriverWait  # Para a espera explícita
from selenium.webdriver.support import expected_conditions as EC  # Para a espera explícita
import pandas as pd  # Manipulação de dados em formato CSV
from datetime import datetime  # Manipulação de data e hora
import os  # Biblioteca para interagir com o sistema operacional
import time  # Controle de tempo de execução do código

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
options.headless = True
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')

while True:  # Inicia um loop infinito
    try:
        # Inicia Firefox em modo headless
        nav = webdriver.Firefox(options=options)

        # Lista de moedas para pesquisar
        moedas = ["Euro", "Dolar americano", "Libra esterlina", "Peso argentino"]

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

                # Exportar para CSV na pasta 'cotacoes'
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                cotacoes_dir = os.path.join(script_dir, 'cotacoes')

                # Verificar se a pasta 'cotacoes' existe, se não, criá-la
                if not os.path.exists(cotacoes_dir):
                    os.makedirs(cotacoes_dir)

                filename = os.path.join(cotacoes_dir, 'cotacoes.csv')

                # Formatando os dados para o formato desejado
                resultado_moeda = resultado_moeda.replace('R$ ', 'R$').replace('.', '').replace(',', '.')
                data_moeda = datetime.now().strftime('%d de %b., %H:%M')

                # Criar um DataFrame com as informações
                data = {'Data e Hora': [data_moeda], 'Moeda': [moeda], 'Cotacao': [resultado_moeda], }
                tabela = pd.DataFrame(data)

                # Salvando o DataFrame como um arquivo CSV na pasta 'cotacoes'
                tabela.to_csv(filename, mode='a', header=not os.path.exists(filename), index=False, sep=';')

                # Registrar a criação do arquivo no log
                with open(log_file_path, 'a') as log_file:
                    log_file.write(f'Informações de {moeda} adicionadas ao arquivo em {datetime.now()}\n')

                print(f'Informações de {moeda} adicionadas ao arquivo')

            except Exception as e:
                # Registrar erro no log em caso de falha na extração de informações da moeda
                logging.error(f'Erro ao buscar informações de {moeda}: {str(e)}')

                # Imprimir mensagem de erro no console
                print(f'Erro ao buscar informações de {moeda}: {str(e)}')

        # Fechar o navegador após concluir a extração para economizar recursos
        nav.quit()

    except Exception as e:
        # Registrar erro no log em caso de falha ao iniciar o navegador
        logging.error(f'Erro ao iniciar o navegador: {str(e)}')

        # Imprimir mensagem de erro no console
        print(f'Erro ao iniciar o navegador: {str(e)}')

    # Aguardar 1 hora antes de tentar novamente
    time.sleep(3600)
