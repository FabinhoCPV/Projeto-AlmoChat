import mysql.connector
import streamlit as st
import difflib

id_componente_global = None  # Defina a variável global

def conectar_bd():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="0000",
        database="estoque_componentes"
    )
    return conn

def autenticar_usuario(username, password):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM usuarios WHERE nome=%s AND senha=%s", (username, password))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return user[1]  # Retorna o nome do usuário
    else:
        return None

def localizar_componente_por_nome(nome_componente_procurado):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM componentes")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        nome_componente_planilha = row[2]
        if isinstance(nome_componente_planilha, str):  
            similaridade = difflib.SequenceMatcher(None, nome_componente_procurado.lower(), nome_componente_planilha.lower()).ratio()
            if similaridade > 0.8:  
                return row[4], row[3], row[0]
    return "Componente não encontrado com esse nome.", None, None

def retirar_componente_do_estoque(id_componente):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM componentes WHERE id=%s", (id_componente,))
    conn.commit()
    conn.close()

def Buscar_Componente(): 
    resultado_busca = localizar_componente_por_nome(nome_componente)
    if resultado_busca[0] == "Componente não encontrado com esse nome.":
        st.error(resultado_busca[0])
    else:
        id_componente_global = resultado_busca[2]
        st.success(f"Componente: {resultado_busca[0]}")
        st.info(f"Quantidade: {resultado_busca[1]}")        
        st.button("Retirar Componente do Estoque", on_click=retirar)

def retirar():
    print("Componente retirado do estoque com sucesso!")
    retirar_componente_do_estoque(id_componente_global)
    st.success("Componente retirado do estoque com sucesso!")

def buscar_transacoes():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacoes")
    rows = cursor.fetchall()
    conn.close()
    return rows

def adicionar_componente(nome, quantidade):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO componentes (nome, quantidade) VALUES (%s, %s)", (nome, quantidade))
    conn.commit()
    conn.close()


def Login_Login():
    user = autenticar_usuario(username, password)
    if user:
        st.success(f"Login bem-sucedido! Bem-vindo, {user}.")
        
        if username == "usuario_mestre" and password == "aaaa":
            st.subheader("Tabela de Transações")
            transacoes = buscar_transacoes()
            for transacao in transacoes:
                st.write(transacao)
            
            st.subheader("Adicionar Novo Componente")
            nome_componente_novo = st.text_input("Nome do Componente:")
            quantidade_nova = st.number_input("Quantidade:", min_value=1, step=1)
            
            if st.button("Adicionar Componente"):
                adicionar_componente(nome_componente_novo, quantidade_nova)
                st.success("Componente adicionado com sucesso!")
        else:
            st.text("Digite o componente a ser procurado:")
            #nome_componente = st.text_input("Componente:",key="nome_componente")
            #st.button("Buscar Componente",  on_click=Buscar_Componente)
    else:
        st.error("Nome de usuário ou senha incorretos.")

    

# Interface do Streamlit
st.title("Autenticação de Usuário")

username = st.text_input("Nome de usuário:")
password = st.text_input("Senha:", type="password")

st.button("Login",on_click = Login_Login)
nome_componente = st.text_input("Componente:",key="nome_componente")
st.button("Buscar Componente",  on_click=Buscar_Componente)
  
