import mysql.connector
import streamlit as st
import hashlib
import difflib

id_componente_global = None  # Defina a variável global
#resultado_busca[2]  = None

def Buscar_Componente():
    #global id_componente_global 
    resultado_busca = localizar_componente_por_nome(nome_componente)
    if resultado_busca[0] == "Componente não encontrado com esse nome.":
        st.error(resultado_busca[0])
    else:
        #id_componente_global = resultado_busca[2]
        st.success(f"Componente: {resultado_busca[0]}")
        st.info(f"Quantidade: {resultado_busca[1]}")        
        st.button("Retirar Componente do Estoque", on_click= retirar)



def retirar():
    print("Componente retirado do estoque com sucesso!")
    retirar_componente_do_estoque(id_componente_global)
    st.success("Componente retirado do estoque com sucesso!")







# Função para conectar ao banco de dados
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
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM usuarios WHERE nome=%s AND senha=%s", (username, password))
    user = cursor.fetchone()

    if user:
        return True
    else:
        return False

# Função para localizar o componente por nome
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

# Função para retirar o componente do estoque
def retirar_componente_do_estoque(id_componente):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    # Implemente aqui a lógica para retirar o componente do estoque, por exemplo:
    cursor.execute("DELETE FROM componentes WHERE id=%s", (id_componente,))
    conn.commit()
    conn.close()

# Interface do Streamlit
st.title("Autenticação de Usuário")

username = st.text_input("Nome de usuário:")
password = st.text_input("Senha:", type="password")

buscar_componente = False  # Inicializar a variável

if st.button("Login"):
    if autenticar_usuario(username, password):
        st.success("Login bem-sucedido! Você pode agora buscar componentes.")
        #buscar_componente = True  # Definir a variável como True se o botão

        st.text("Digite o componente a ser procurado:")
        nome_componente = st.text_input("Componente:")
        st.button("Buscar Componente", on_click=Buscar_Componente)           




   
            



