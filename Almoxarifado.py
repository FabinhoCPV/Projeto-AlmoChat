#VERSÃO PRÉVIA

import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html
import pandas as pd
import difflib

# Carregar a planilha do Excel
planilha = pd.read_excel("Planilha de Componentes.xlsx", header=None)

def localizar_componente_por_nome(nome_componente_procurado):
    for nome_componente_planilha in planilha[2]:
        if isinstance(nome_componente_planilha, str):  # Verifica se é uma string
            similaridade = difflib.SequenceMatcher(None, nome_componente_procurado.lower(), nome_componente_planilha.lower()).ratio()
            if similaridade > 0.8:  # Ajuste este valor conforme necessário
                componente = planilha[planilha[2] == nome_componente_planilha]
                if not componente.empty:
                    return componente.iloc[0][4], componente.iloc[0][3]  # Retorna o endereço e a quantidade do primeiro componente encontrado
    return "Componente não encontrado com esse nome.", None

# Função principal
def main():
    st.title("Almochat")

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
#if _name_ == "_main_":
main()