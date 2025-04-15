import pandas as pd

# Puxando os dados
dt_janeiro = pd.read_csv(r'Dados\Dados_janeiro_2025.csv', sep=';', encoding='ISO-8859-1')
dt_fevereiro = pd.read_csv(r'Dados\Dados_fevereiro_2025.csv', sep=';', encoding='ISO-8859-1')
dt_marco = pd.read_csv(r'Dados\Dados_marco_2025.csv', sep=';', encoding='ISO-8859-1')

# Concatenando os dados
dt_2025 = pd.concat([dt_janeiro, dt_fevereiro, dt_marco], ignore_index=True)

# Removendo colunas que não são necessárias e limpando os dados
colunas_zeradas = ['REPASSE', 'Cï¿½DIGO ï¿½RGï¿½O SUPERIOR', 'NOME ï¿½RGï¿½O SUPERIOR', 'Cï¿½DIGO ï¿½RGï¿½O', 'NOME ï¿½RGï¿½O', 'Cï¿½DIGO UNIDADE GESTORA', 'Mï¿½S EXTRATO', 'Nï¿½MERO CONVï¿½NIO', 'Cï¿½DIGO CONVENENTE', 'DATA TRANSAï¿½ï¿½O', 'VALOR TRANSAï¿½ï¿½O', 'TRANSAï¿½ï¿½O']
dt_2025.drop(columns=colunas_zeradas, inplace=True)
dt_2025.drop_duplicates(inplace=True)
dt_2025.dropna(inplace=True)

# Convertendo os tipos de dados
dt_2025['DATA TRANSAÇÃO'] = pd.to_datetime(dt_2025['DATA TRANSAÇÃO'], format='%d/%m/%Y')
dt_2025['VALOR TRANSAÇÃO'] = dt_2025['VALOR TRANSAÇÃO'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

colunas_numericas = ['CÓDIGO ÓRGÃO SUPERIOR', 'CÓDIGO ÓRGÃO', 'CÓDIGO UNIDADE GESTORA', 'MÊS EXTRATO', 'NÚMERO CONVÊNIO', 'CÓDIGO CONVENENTE']
dt_2025[colunas_numericas] = dt_2025[colunas_numericas].astype(int)



print(dt_2025.info())
