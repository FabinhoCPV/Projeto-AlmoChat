import mysql.connector

# Função para conectar ao banco de dados MySQL
def conectar_bd():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="0000",  # Senha do seu banco de dados
        database="estoque_componentes"
    )
    return conn

# Função para verificar se um usuário e senha existem na tabela usuarios
def verificar_credenciais(username, password):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nome=%s AND senha=%s", (username, password))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

username = input("Nome de usuário: ").strip()
password = input("Senha: ").strip()


try:
    usuario = verificar_credenciais(username, password)
    if usuario:
        print("Credenciais válidas. O usuário existe na tabela.")
    else:
        print("Credenciais inválidas. O usuário não existe ou a senha está incorreta.")
except mysql.connector.Error as e:
    print(f"Erro ao acessar o banco de dados: {e}")
