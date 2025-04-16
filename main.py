import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

# Puxando os dados
df_janeiro = pd.read_csv(r'Dados/Dados_janeiro_2025.csv', sep=';', encoding='ISO-8859-1')
df_fevereiro = pd.read_csv(r'Dados/Dados_fevereiro_2025.csv', sep=';', encoding='ISO-8859-1')
df_marco = pd.read_csv(r'Dados/Dados_marco_2025.csv', sep=';', encoding='ISO-8859-1')

# Concatenando os dados
df_2025 = pd.concat([df_janeiro, df_fevereiro, df_marco], ignore_index=True)

# Removendo colunas que não são necessárias e limpando os dados
colunas_zeradas = ['REPASSE', 'Cï¿½DIGO ï¿½RGï¿½O SUPERIOR', 'NOME ï¿½RGï¿½O SUPERIOR', 'Cï¿½DIGO ï¿½RGï¿½O', 'NOME ï¿½RGï¿½O', 'Cï¿½DIGO UNIDADE GESTORA', 'Mï¿½S EXTRATO', 'Nï¿½MERO CONVï¿½NIO', 'Cï¿½DIGO CONVENENTE', 'DATA TRANSAï¿½ï¿½O', 'VALOR TRANSAï¿½ï¿½O', 'TRANSAï¿½ï¿½O']
df_2025.drop(columns=colunas_zeradas, inplace=True)
df_2025.drop_duplicates(inplace=True)
df_2025.dropna(inplace=True)

# Convertendo os tipos de dados
df_2025['DATA TRANSAÇÃO'] = pd.to_datetime(df_2025['DATA TRANSAÇÃO'], format='%d/%m/%Y')
df_2025['VALOR TRANSAÇÃO'] = df_2025['VALOR TRANSAÇÃO'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

colunas_numericas = ['CÓDIGO ÓRGÃO SUPERIOR', 'CÓDIGO ÓRGÃO', 'CÓDIGO UNIDADE GESTORA', 'MÊS EXTRATO', 'NÚMERO CONVÊNIO', 'CÓDIGO CONVENENTE']
df_2025[colunas_numericas] = df_2025[colunas_numericas].astype(int)

df = df_2025
df["ANO_MES"] = df["DATA TRANSAÇÃO"].dt.to_period("M")
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# Gráfico 1: Total de valor transacionado por mês
df.groupby("ANO_MES")["VALOR TRANSAÇÃO"].sum().plot(kind="bar", title="Total de Valor Transacionado por Mês")
plt.xticks(rotation=45)
plt.tight_layout()
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
image1 = base64.b64encode(buf.read()).decode('utf-8')
print(image1)
buf.close()

# Gráfico 2: Top 10 Unidades Gestoras por valor transacionado
df.groupby("NOME UNIDADE GESTORA")["VALOR TRANSAÇÃO"].sum().sort_values(ascending=False).head(10).plot(kind="bar", title="Top 10 Unidades Gestoras por Valor Transacionado")
plt.xticks(rotation=90)
plt.tight_layout()
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
image1 = base64.b64encode(buf.read()).decode('utf-8')
print(image1)
buf.close()

# Gráfico 3: Top 10 Favorecidos por valor transacionado
df.groupby("NOME FAVORECIDO")["VALOR TRANSAÇÃO"].sum().sort_values(ascending=False).head(10).plot(kind="bar", title="Top 10 Favorecidos por Valor Transacionado")
plt.xticks(rotation=90)
plt.tight_layout()
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
image1 = base64.b64encode(buf.read()).decode('utf-8')
print(image1)
buf.close()

# Gráfico 4: Distribuição dos valores de transação
sns.histplot(df["VALOR TRANSAÇÃO"].dropna(), bins=50, kde=True)
plt.title("Distribuição dos Valores de Transação")
plt.tight_layout()
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
image1 = base64.b64encode(buf.read()).decode('utf-8')
print(image1)
buf.close()

# Gráfico 5: Evolução temporal do valor transacionado
df.groupby("DATA TRANSAÇÃO")["VALOR TRANSAÇÃO"].sum().plot(kind="line", title="Evolução Temporal do Valor Transacionado")
plt.tight_layout()
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
image1 = base64.b64encode(buf.read()).decode('utf-8')
print(image1)
buf.close()

