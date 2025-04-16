from Funções import tratamento_dados
from Funções import funcoes_graficos

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

# Configurando o estilo do seaborn
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# Puxando os dados
df_janeiro, df_fevereiro, df_marco = tratamento_dados.carregar_dados([r'Dados/Dados_janeiro_2025.csv', r'Dados/Dados_fevereiro_2025.csv', r'Dados/Dados_marco_2025.csv'], ';', 'ISO-8859-1')

# Concatenando os dados
df = tratamento_dados.junta_dados([df_janeiro, df_fevereiro, df_marco])

# limpando os dados
df_2025 = tratamento_dados.limpar_dados(df)

print(df_2025.columns)

# Convertendo os tipos de dados
df = tratamento_dados.converter_para_datetime(df, 'DATA TRANSACAO')
df = tratamento_dados.converter_para_valor(df, 'VALOR TRANSACAO')
colunas_numericas = ['CODIGO ORGAO SUPERIOR', 'CODIGO ORGAO', 'CODIGO UNIDADE GESTORA', 'MES EXTRATO', 'NUMERO CONVENIO', 'CODIGO CONVENENTE']
df = tratamento_dados.converter_para_int(df, colunas_numericas)

# Convertendo a coluna de data para o formato de ano e mês
df["ANO_MES"] = df["DATA TRANSACAO"].dt.to_period("M")

# Gráfico 1: Total de valor transacionado por mês
df.groupby("ANO_MES")["VALOR TRANSACAO"].sum().plot(kind="bar", title="Total de Valor Transacionado por Mês")
plt.xticks(rotation=45)
image1 = funcoes_graficos.salvando_imagem(plt, "grafico1.png")


# Gráfico 2: Top 10 Unidades Gestoras por valor transacionado
df.groupby("NOME UNIDADE GESTORA")["VALOR TRANSACAO"].sum().sort_values(ascending=False).head(10).plot(kind="bar", title="Top 10 Unidades Gestoras por Valor Transacionado")
plt.xticks(rotation=90)
image2 = funcoes_graficos.salvando_imagem(plt, "grafico2.png")

# Gráfico 3: Top 10 Favorecidos por valor transacionado
df.groupby("NOME FAVORECIDO")["VALOR TRANSACAO"].sum().sort_values(ascending=False).head(10).plot(kind="bar", title="Top 10 Favorecidos por Valor Transacionado")
plt.xticks(rotation=90)
image3 = funcoes_graficos.salvando_imagem(plt, "grafico3.png")

# Gráfico 4: Distribuição dos valores de transação
sns.histplot(df["VALOR TRANSACAO"].dropna(), bins=50, kde=True)
plt.title("Distribuição dos Valores de Transação")
image4 = funcoes_graficos.salvando_imagem(plt, "grafico4.png")

# Gráfico 5: Evolução temporal do valor transacionado
df.groupby("DATA TRANSACAO")["VALOR TRANSACAO"].sum().plot(kind="line", title="Evolução Temporal do Valor Transacionado")
image5 = funcoes_graficos.salvando_imagem(plt, "grafico5.png")

print(image1)
print(image2)
print(image3)
print(image4)
print(image5)