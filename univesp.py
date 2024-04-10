import pandas as pd

# Carregando a planilha e especificando os nomes das colunas
nomes_colunas = ['Descrição', 'Local', 'Quantidade']  # Substitua esses nomes pelos nomes corretos das suas colunas
planilha = pd.read_excel("Planilha de Componentes.xlsx", names=nomes_colunas)

# Definindo a coluna 'Descrição' como índice para facilitar a busca
planilha.set_index('Descrição', inplace=True)

# Função para pesquisar o componente
def encontrar_componente(componente):
    try:
        localizacao = planilha.loc[componente, 'Local']
        quantidade = planilha.loc[componente, 'Quantidade']
        print(f"O componente '{componente}' está localizado em '{localizacao}' e há '{quantidade}' unidades disponíveis.")
    except KeyError:
        print(f"O componente '{componente}' não foi encontrado no estoque.")

# Exemplo de uso
encontrar_componente("resistor de 10R")
