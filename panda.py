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

# Loop principal
while True:
    # Solicitar ao usuário o nome do componente
    nome_componente_procurado = input("Digite o nome do componente (ou 'sair' para encerrar): ")

    # Verificar se o usuário deseja sair
    if nome_componente_procurado.lower() == 'sair':
        print("Encerrando o programa...")
        break

    # Localizar o componente pelo nome
    endereco, quantidade = localizar_componente_por_nome(nome_componente_procurado)

    if quantidade is not None:
        print(f"O componente '{nome_componente_procurado}' está localizado em '{endereco}' e a quantidade é {quantidade}.")
    else:
        print(endereco)  # Se o componente não for encontrado, imprime a mensagem de erro
