from Funções import tratamento_dados
from Funções import funcoes_graficos

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import FileSystemLoader, Environment

# Configurando o estilo do seaborn
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# Puxando os dados
df_1_semestre, df_2_semestre = tratamento_dados.carregar_dados([r'Dados/glp-2023-01.csv', r'Dados/glp-2023-02.csv'], ';', 'ISO-8859-1')

# Concatenando os dados
df = tratamento_dados.junta_dados([df_1_semestre, df_2_semestre])

# limpando os dados
#df = tratamento_dados.limpar_dados(df)
print(df.columns)

# Convertendo os tipos de dados
df = tratamento_dados.converter_para_datetime(df, 'DATA DA COLETA')
df = tratamento_dados.converter_para_valor(df, 'VALOR DE VENDA')

# 1. Evolução do preço médio diário
preco_diario = df.groupby("DATA DA COLETA")["VALOR DE VENDA"].mean()
preco_diario.plot(marker='o', title="Preço Médio Diário do GLP - Janeiro 2023")
plt.ylabel("Valor de Venda (R$)")
plt.grid(True)
plt.tight_layout()
image1 = funcoes_graficos.salvando_imagem(plt, "grafico1.png")

# 2. Preço médio por estado
preco_estado = df.groupby("ESTADO - SIGLA")["VALOR DE VENDA"].mean().sort_values()
preco_estado.plot(kind='bar', color='skyblue', title="Preço Médio do GLP por Estado - Janeiro 2023")
plt.ylabel("Valor de Venda (R$)")
plt.xticks(rotation=45)
plt.tight_layout()
image2 = funcoes_graficos.salvando_imagem(plt, "grafico2.png")

# 3. Distribuição dos preços
sns.histplot(df["VALOR DE VENDA"].dropna(), bins=40, kde=True, color='green')
plt.title("Distribuição dos Valores de Venda do GLP")
plt.xlabel("Valor de Venda (R$)")
plt.tight_layout()
image3 = funcoes_graficos.salvando_imagem(plt, "grafico3.png")

# 4. Boxplot por estado
plt.figure(figsize=(16, 6))
sns.boxplot(data=df, x="ESTADO - SIGLA", y="VALOR DE VENDA")
plt.title("Distribuição de Preços do GLP por Estado")
plt.xticks(rotation=45)
plt.tight_layout()
image4 = funcoes_graficos.salvando_imagem(plt, "grafico4.png")

# 5. Top 10 municípios com maior e menor preço médio
preco_municipio = df.groupby("MUNICIPIO")["VALOR DE VENDA"].mean()
top10_maior = preco_municipio.sort_values(ascending=False).head(10)
top10_menor = preco_municipio.sort_values().head(10)

# Maiores
top10_maior.plot(kind="bar", color="red", title="Top 10 Municípios com Maior Preço Médio de GLP")
plt.ylabel("Valor de Venda (R$)")
plt.xticks(rotation=45)
plt.tight_layout()
image5 = funcoes_graficos.salvando_imagem(plt, "grafico5.png")

# Menores
top10_menor.plot(kind="bar", color="blue", title="Top 10 Municípios com Menor Preço Médio de GLP")
plt.ylabel("Valor de Venda (R$)")
plt.xticks(rotation=45)
plt.tight_layout()
image6 = funcoes_graficos.salvando_imagem(plt, "grafico6.png")

# 6. Preço médio por bandeira (Top 10)
preco_bandeira = df.groupby("BANDEIRA")["VALOR DE VENDA"].mean().sort_values(ascending=False).head(10)
preco_bandeira.plot(kind="bar", color="purple", title="Preço Médio do GLP por Bandeira (Top 10)")
plt.ylabel("Valor de Venda (R$)")
plt.xticks(rotation=45)
plt.tight_layout()
image7 = funcoes_graficos.salvando_imagem(plt, "grafico7.png")

loader = FileSystemLoader('Templates')
env = Environment(loader=loader)
template = env.get_template('template1.html')

file = open('Output/index.html', 'w')

render = template.render(plot_data1 = image1, plot_data2 = image2, plot_data3 = image3, plot_data4 = image4, plot_data5 = image5, plot_data6 = image6, plot_data7 = image7)

file.write(render)
file.close()