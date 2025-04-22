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

# Lista com suas imagens base64
imagens_base64 = [image1, image2, image3, image4, image5, image6, image7]

# Criar PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=10)

for img_b64 in imagens_base64:
    # Decodifica base64 para imagem
    img_bytes = base64.b64decode(img_b64.split(',')[-1])  # remove 'data:image/png;base64,...'
    image = Image.open(BytesIO(img_bytes))

    # Salva imagem temporária em disco para o FPDF ler
    temp_path = 'temp_image.png'
    image.save(temp_path)

    # Adiciona imagem ao PDF
    pdf.add_page()
    pdf.image(temp_path, x=10, y=20, w=180)  # Ajuste w/h conforme o layout

# Salvar PDF final
pdf.output("Output/relatorio_graficos.pdf")

print("✅ PDF gerado com sucesso!")

# CONFIGURAÇÕES
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_REMETENTE = 'gabrielferreira192000@gmail.com'
SENHA = 'bpmv txks vlhu hjha'  # senha de aplicativo
EMAIL_DESTINATARIO = 'gabrielferreira192000@exemplo.com'

# ARQUIVO A SER ENVIADO COMO ANEXO
CAMINHO_ANEXO = 'Output/relatorio_graficos.pdf'
NOME_EXIBIDO_ANEXO = os.path.basename(CAMINHO_ANEXO)

# CRIAR MENSAGEM
msg = MIMEMultipart()
msg['From'] = EMAIL_REMETENTE
msg['To'] = EMAIL_DESTINATARIO
msg['Subject'] = '📎 Relatório em PDF Anexo'

# CORPO DO E-MAIL
mensagem = "Olá! Segue em anexo o relatório com os gráficos da semana. Qualquer dúvida, estou à disposição."
msg.attach(MIMEText(mensagem, 'plain'))

# ANEXAR ARQUIVO
with open(CAMINHO_ANEXO, 'rb') as f:
    parte = MIMEBase('application', 'octet-stream')
    parte.set_payload(f.read())
    encoders.encode_base64(parte)
    parte.add_header('Content-Disposition', f'attachment; filename="{NOME_EXIBIDO_ANEXO}"')
    msg.attach(parte)

# ENVIAR
try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_REMETENTE, SENHA)
    server.send_message(msg)
    server.quit()
    print("✅ E-mail com anexo enviado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao enviar e-mail: {e}")