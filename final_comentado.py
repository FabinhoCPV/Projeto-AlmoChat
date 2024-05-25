import mysql.connector  # Biblioteca para conectar ao MySQL
import streamlit as st  # Biblioteca para criar a interface web
import difflib  # Biblioteca para comparar sequências e calcular similaridade

# Variável global para armazenar o ID do componente selecionado
id_componente_global = None

# Função para conectar ao banco de dados MySQL
def conectar_bd():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="0000",
        database="estoque_componentes"
    )
    return conn

# Função para autenticar o usuário
def autenticar_usuario(username, password):
    conn = conectar_bd()  # Conecta ao banco de dados
    cursor = conn.cursor()
    
    # Executa a consulta para verificar o usuário
    cursor.execute("SELECT * FROM usuarios WHERE nome=%s AND senha=%s", (username, password))
    user = cursor.fetchone()  # Obtém o resultado da consulta
    
    conn.close()  # Fecha a conexão com o banco de dados
    
    if user:
        return user[1]  # Retorna o nome do usuário se autenticado
    else:
        return None  # Retorna None se a autenticação falhar

# Função para localizar um componente pelo nome
def localizar_componente_por_nome(nome_componente_procurado):
    conn = conectar_bd()  # Conecta ao banco de dados
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM componentes")  # Seleciona todos os componentes
    rows = cursor.fetchall()  # Obtém todos os resultados da consulta
    conn.close()  # Fecha a conexão com o banco de dados

    # Itera sobre os componentes para encontrar um nome semelhante
    for row in rows:
        nome_componente_planilha = row[2]
        if isinstance(nome_componente_planilha, str):  
            # Calcula a similaridade entre os nomes
            similaridade = difflib.SequenceMatcher(None, nome_componente_procurado.lower(), nome_componente_planilha.lower()).ratio()
            if similaridade > 0.8:  
                return row[4], row[3], row[0]  # Retorna informações do componente se encontrado
    return "Componente não encontrado com esse nome.", None, None

# Função para retirar um componente do estoque
def retirar_componente_do_estoque(id_componente):
    conn = conectar_bd()  # Conecta ao banco de dados
    cursor = conn.cursor()
    
    # Executa a exclusão do componente pelo ID
    cursor.execute("DELETE FROM componentes WHERE id=%s", (id_componente,))
    conn.commit()  # Confirma a transação
    conn.close()  # Fecha a conexão com o banco de dados

# Função para buscar um componente (interface)
def Buscar_Componente(): 
    resultado_busca = localizar_componente_por_nome(nome_componente)
    if resultado_busca[0] == "Componente não encontrado com esse nome.":
        st.error(resultado_busca[0])  # Exibe mensagem de erro
    else:
        global id_componente_global
        id_componente_global = resultado_busca[2]  # Armazena o ID do componente
        st.success(f"Componente: {resultado_busca[0]}")  # Exibe o nome do componente
        st.info(f"Quantidade: {resultado_busca[1]}")  # Exibe a quantidade
        st.button("Retirar Componente do Estoque", on_click=retirar)  # Botão para retirar o componente

# Função para retirar o componente (interface)
def retirar():
    print("Componente retirado do estoque com sucesso!")
    retirar_componente_do_estoque(id_componente_global)  # Chama a função de retirada
    st.success("Componente retirado do estoque com sucesso!")  # Exibe mensagem de sucesso

# Função para buscar transações do banco de dados
def buscar_transacoes():
    conn = conectar_bd()  # Conecta ao banco de dados
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacoes")  # Seleciona todas as transações
    rows = cursor.fetchall()  # Obtém todos os resultados da consulta
    conn.close()  # Fecha a conexão com o banco de dados
    return rows  # Retorna as transações

# Função para adicionar um novo componente ao banco de dados
def adicionar_componente(nome, quantidade):
    conn = conectar_bd()  # Conecta ao banco de dados
    cursor = conn.cursor()
    
    # Executa a inserção do novo componente
    cursor.execute("INSERT INTO componentes (nome, quantidade) VALUES (%s, %s)", (nome, quantidade))
    conn.commit()  # Confirma a transação
    conn.close()  # Fecha a conexão com o banco de dados

# Função de login e funcionalidades da interface após login
def Login_Login():
    user = autenticar_usuario(username, password)  # Autentica o usuário
    if user:
        st.success(f"Login bem-sucedido! Bem-vindo, {user}.")  # Exibe mensagem de sucesso

        if username == "usuario_mestre" and password == "aaaa":  # Verifica se é o usuário mestre
            st.subheader("Tabela de Transações")
            transacoes = buscar_transacoes()  # Busca transações
            for transacao in transacoes:
                st.write(transacao)  # Exibe cada transação
            
            st.subheader("Adicionar Novo Componente")
            nome_componente_novo = st.text_input("Nome do Componente:")
            quantidade_nova = st.number_input("Quantidade:", min_value=1, step=1)
            
            if st.button("Adicionar Componente"):
                adicionar_componente(nome_componente_novo, quantidade_nova)  # Adiciona o novo componente
                st.success("Componente adicionado com sucesso!")
        else:
            st.text("Digite o componente a ser procurado:")
            # Nome do componente para busca
            # nome_componente = st.text_input("Componente:",key="nome_componente")
            # st.button("Buscar Componente",  on_click=Buscar_Componente)
    else:
        st.error("Nome de usuário ou senha incorretos.")  # Exibe mensagem de erro

# Interface do Streamlit
st.title("Autenticação de Usuário")

# Entrada de nome de usuário e senha
username = st.text_input("Nome de usuário:")
password = st.text_input("Senha:", type="password")

# Botões de login e busca de componente
st.button("Login", on_click=Login_Login)
nome_componente = st.text_input("Componente:", key="nome_componente")
st.button("Buscar Componente", on_click=Buscar_Componente)
