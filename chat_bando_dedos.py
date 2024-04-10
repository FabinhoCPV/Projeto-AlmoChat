import streamlit as st
import sqlite3
from streamlit.components.v1 import html
import difflib

# Função para conectar ao banco de dados SQLite
def conectar_bd():
    conn = sqlite3.connect("banco_de_dados.db")  # Nome do arquivo do banco de dados SQLite
    return conn

# Função para localizar o componente pelo nome no banco de dados SQLite
def localizar_componente_por_nome(nome_componente_procurado):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nome_da_tabela")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        nome_componente_planilha = row[2]
        if isinstance(nome_componente_planilha, str):  
            similaridade = difflib.SequenceMatcher(None, nome_componente_procurado.lower(), nome_componente_planilha.lower()).ratio()
            if similaridade > 0.8:  
                return row[4], row[3]  
    return "Componente não encontrado com esse nome.", None

# Função principal
def main():
    st.title("Chatbot para Localização de Componentes")

    # Solicitar ao usuário o nome do componente inicial
    nome_componente_procurado = st.text_input("Digite o nome do componente (ou 'sair' para encerrar): ")

    # Loop principal para receber mensagens do usuário
    while True:
        # Verificar se o usuário deseja sair
        if nome_componente_procurado.lower() == 'sair' or not nome_componente_procurado:
            if nome_componente_procurado.lower() == 'sair':
                st.warning("Encerrando o chat...")
            break

        # Localizar o componente pelo nome
        endereco, quantidade = localizar_componente_por_nome(nome_componente_procurado)

        if quantidade is not None:
            st.success(f"O componente '{nome_componente_procurado}' está localizado em '{endereco}' e a quantidade é {quantidade}.")
        else:
            st.error("Componente não encontrado.")

        # Solicitar ao usuário o nome do próximo componente
        nome_componente_procurado = st.text_input("Digite o nome do próximo componente (ou 'sair' para encerrar): ", key=f"componente-{nome_componente_procurado}")

# Executa a função principal
if __name__ == "__main__":
    main()
