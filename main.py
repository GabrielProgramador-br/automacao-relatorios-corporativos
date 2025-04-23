from Funções import tratamento_dados
from Funções import funcoes_graficos

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
import base64
from fpdf import FPDF
from PIL import Image
from io import BytesIO

# Configurando o estilo do seaborn
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

file_dialogues = "Dados/Hi_Bot_Whatsapp_-_Homologação_dialogos_2025-03-01_2025-03-29.xlsx"
file_articles = "Dados/Hi_Bot_Whatsapp_-_Homologação_artigos_acessados_01-03-2025_29-03-2025.xlsx"
file_retention = "Dados/Hi_Bot_Whatsapp_-_Homologação_retencao_01-03-2025_29-03-2025.xlsx"

df_dialogues = pd.read_excel(file_dialogues)
df_articles = pd.read_excel(file_articles)
df_retention = pd.read_excel(file_retention)

df_dialogues["Data"] = pd.to_datetime(df_dialogues["Data"])
df_dialogues = df_dialogues.sort_values(by="Data")
df_dialogues["month"] = df_dialogues["Data"].apply(lambda x: str(x.year) + "-" + str(x.month))

df_articles["Data"] = pd.to_datetime(df_articles["Data"])
df_articles = df_articles.sort_values(by="Data")
df_articles["month"] = df_articles["Data"].apply(lambda x: str(x.year) + "-" + str(x.month))

df_retention["Data"] = pd.to_datetime(df_retention["Data"])
df_retention = df_retention.sort_values(by="Data")
df_retention["month"] = df_retention["Data"].apply(lambda x: str(x.year) + "-" + str(x.month))

image1, explicacao1 = funcoes_graficos.plot_chatbot_efficiency(df_dialogues)
image2, explicacao2 = funcoes_graficos.plot_article_popularity(df_articles)
image3, explicacao3 = funcoes_graficos.plot_retention_correlation(df_retention)
image4, explicacao4 = funcoes_graficos.plot_peak_hours(df_dialogues)
image5, explicacao5 = funcoes_graficos.plot_top_questions(df_dialogues)
image6, explicacao6 = funcoes_graficos.plot_avg_conversation_time(df_dialogues)


# Lista com suas imagens e explicações
imagens_base64 = [image1, image2, image3, image4, image5, image6]
explicacoes = [explicacao1, explicacao2, explicacao3, explicacao4, explicacao5, explicacao6]

# Criar PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", size=12)

for idx, (img_b64, explicacao) in enumerate(zip(imagens_base64, explicacoes), start=1):
    # Decodifica base64 para imagem
    img_bytes = base64.b64decode(img_b64.split(',')[-1])
    image = Image.open(BytesIO(img_bytes))

    # Salva imagem temporária com nome único
    temp_path = f'temp_image_{idx}.png'
    image.save(temp_path)

    # Adiciona nova página e insere imagem
    pdf.add_page()

    # Define largura e calcula altura proporcional
    img_width = 180
    image = Image.open(BytesIO(img_bytes))
    aspect = image.height / image.width
    img_height = img_width * aspect

    # Insere imagem
    pdf.image(temp_path, x=10, y=20, w=img_width, h=img_height)

    # Move cursor para logo abaixo da imagem
    pdf.set_xy(10, 20 + img_height + 5)
    pdf.multi_cell(190, 8, explicacao, align='L')

# Salvar PDF final
output_path = "Output/relatorio_graficos.pdf"
pdf.output(output_path)
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

# Após salvar o PDF
for idx in range(1, len(imagens_base64) + 1):
    temp_path = f'temp_image_{idx}.png'
    if os.path.exists(temp_path):
        os.remove(temp_path)
