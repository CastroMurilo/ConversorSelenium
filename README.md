# Cotações de Moedas
Este script Python realiza a automação da navegação web para obter informações de cotações de moedas em relação ao Real. O código utiliza a biblioteca Selenium para controlar um navegador Firefox em modo headless, permitindo a execução sem interface gráfica. As informações obtidas são registradas em um arquivo CSV e mensagens de log são geradas para monitorar o processo.

# Pré-Requisitos
- **Python 3.10**
- Bibliotecas: **Selenium**, **Pandas**, **webdriver_manager**

# Detalhes do Script
## Bibliotecas Utilizadas
**logging:** Registra mensagens de log para monitorar a execução.
**selenium:** Automatiza a navegação web.
**pandas:** Manipula e analisa dados em formato tabular.
**datetime:** Manipula informações de data e hora.
**os:** Interage com o sistema operacional.
**time:** Controla o tempo de execução.
## Configuração do Logger
O logger é configurado para registrar mensagens em um arquivo chamado 'cotacoes.log'.
Mensagens de log também são exibidas no console.
## Estrutura do Projeto
Um diretório chamado 'cotacoes' é criado para armazenar os resultados em arquivos CSV.
Um loop infinito é iniciado para executar a extração a cada hora.
## Pesquisa no Google
O script realiza pesquisas no Google para obter informações de cotações das moedas desejadas.
As moedas alvo são definidas na lista moedas.
## Manipulação e Exportação de Dados
As informações obtidas são formatadas e armazenadas em um arquivo CSV.
Cada execução adiciona uma nova linha ao arquivo 'cotacoes.csv'.
## Logs e Tratamento de Erros
Erros durante a execução são registrados no arquivo de log e exibidos no console.
Caso ocorra uma falha ao buscar informações de uma moeda específica, o script continua com as outras.
# Observações
- O script faz uso do modo **headless** do navegador para execução sem interface gráfica.
- Caso haja falha na inicialização padrão do navegador, uma tentativa alternativa é realizada.
- O script continuará a executar indefinidamente, coletando informações a cada iteração do loop.
- Certifique-se de configurar corretamente o ambiente e as dependências antes de executar o script.






