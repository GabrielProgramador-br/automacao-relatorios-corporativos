import pandas as pd

dt_janeiro = pd.read_csv(r'Dados\Dados_janeiro_2025.csv', sep=';', encoding='ISO-8859-1')
dt_fevereiro = pd.read_csv(r'Dados\Dados_fevereiro_2025.csv', sep=';', encoding='ISO-8859-1')
dt_marco = pd.read_csv(r'Dados\Dados_marco_2025.csv', sep=';', encoding='ISO-8859-1')

dt_2025 = pd.concat([dt_janeiro, dt_fevereiro, dt_marco], ignore_index=True)

colunas_zeradas = ['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5']
dt_2025.drop(columns=colunas_zeradas, inplace=True)
print(dt_2025.head())