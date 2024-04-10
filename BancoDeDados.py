import pandas as pd
import sqlite3

# Ler o arquivo Excel
caminho_arquivo_excel = 'Planilha de Componentes.xlsx'
dados_excel = pd.read_excel(caminho_arquivo_excel)

# Conectar ao banco de dados SQLite
con = sqlite3.connect('seu_banco_de_dados.db')

# Salvar os dados no banco de dados SQLite
dados_excel.to_sql('nome_da_tabela', con, if_exists='replace', index=False)

# Fechar a conexão com o banco de dados
con.close()
