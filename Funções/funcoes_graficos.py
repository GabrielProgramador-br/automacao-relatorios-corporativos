import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import plotly.express as px
import plotly.io as pio
from scipy.stats import pearsonr

def salvando_imagem(fig):
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)
    return img_base64

def explicar_chatbot_efficiency(df):
    misunderstood = df[df['Resposta'].str.contains("não entendi|não consegui", case=False, na=False)]
    total = len(df)
    misunderstood_rate = len(misunderstood) / total * 100
    understood_rate = 100 - misunderstood_rate

    return (
        f"O chatbot conseguiu entender corretamente {understood_rate:.1f}% das interações, "
        f"enquanto {misunderstood_rate:.1f}% não foram compreendidas. "
        f"Isso mostra um desempenho razoável, mas há espaço para melhorar a clareza das respostas ou expandir a base de conhecimento."
    )

def plot_chatbot_efficiency(df):
    misunderstood = df[df['Resposta'].str.contains("não entendi|não consegui", case=False, na=False)]
    total = len(df)
    misunderstood_rate = len(misunderstood) / total * 100
    understood_rate = 100 - misunderstood_rate

    labels = ['Entendidos', 'Não Entendidos']
    sizes = [understood_rate, misunderstood_rate]
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title("Eficiência do Chatbot")

    return salvando_imagem(fig), explicar_chatbot_efficiency(df)

def explicar_article_popularity(df):
    top_article = df.groupby("Artigo")["Acessos"].sum().sort_values(ascending=False).head(1)
    artigo = top_article.index[0]
    acessos = top_article.iloc[0]

    return (
        f"O artigo mais acessado foi '{artigo}', com um total de {acessos} visualizações. "
        f"Esse dado pode indicar um tema de alto interesse ou um tópico com dúvidas frequentes."
    )

def plot_article_popularity(df):
    top_articles = df.groupby("Artigo")["Acessos"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.bar(top_articles.index, top_articles.values)
    ax.set_title("Top 10 Artigos Mais Acessados")
    ax.set_xlabel("Artigos")
    ax.set_ylabel("Acessos")
    plt.xticks(rotation=45, ha='right')

    return salvando_imagem(fig), explicar_article_popularity(df)



def explicar_retention_correlation(df):
    df['Retidos'] = df['Retidos'].astype(float)
    df['Quantidade de Atendimentos'] = df['Quantidade de Atendimentos'].astype(float)
    corr, _ = pearsonr(df['Quantidade de Atendimentos'], df['Retidos'])

    if corr > 0.5:
        tendencia = "quanto mais atendimentos, maior a retenção"
    elif corr < -0.5:
        tendencia = "mais atendimentos estão associados a menor retenção"
    else:
        tendencia = "não há uma correlação significativa entre as variáveis"

    return f"A correlação entre quantidade de atendimentos e retenção foi de {corr:.2f}, indicando que {tendencia}."

def plot_retention_correlation(df):
    df['Retidos'] = df['Retidos'].astype(int)
    df['Quantidade de Atendimentos'] = df['Quantidade de Atendimentos'].astype(int)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['Quantidade de Atendimentos'], df['Retidos'], alpha=0.6, s=60, color='#1f77b4')
    ax.set_title("Correlação entre Retenção e Atendimentos")
    ax.set_xlabel("Quantidade de Atendimentos")
    ax.set_ylabel("Retidos")
    ax.grid(True, linestyle='--', alpha=0.5)

    return salvando_imagem(fig), explicar_retention_correlation(df)

def explicar_peak_hours(df):
    df['Hora'] = pd.to_datetime(df['Data']).dt.hour
    pico = df['Hora'].value_counts().idxmax()
    atendimentos_pico = df['Hora'].value_counts().max()

    return (
        f"O maior volume de atendimentos ocorreu às {pico}h, com {atendimentos_pico} interações registradas. "
        f"Esse horário pode indicar o melhor momento para reforçar a atuação da equipe ou do chatbot."
    )

def plot_peak_hours(df):
    df['Hora'] = pd.to_datetime(df['Data']).dt.hour
    hourly_counts = df['Hora'].value_counts().sort_index()

    fig, ax = plt.subplots()
    ax.plot(hourly_counts.index, hourly_counts.values, marker='o')
    ax.set_title("Horários de Pico de Atendimento")
    ax.set_xlabel("Hora do Dia")
    ax.set_ylabel("Número de Atendimentos")
    ax.grid(True)

    return salvando_imagem(fig), explicar_peak_hours(df)

def explicar_top_questions(df):
    pergunta_top = df['Pergunta'].value_counts().idxmax()
    freq = df['Pergunta'].value_counts().max()

    return f"A pergunta mais frequente foi: '{pergunta_top}', com um total de {freq} ocorrências. Ela pode indicar uma dúvida recorrente entre os usuários."

def plot_top_questions(df):
    top_questions = df['Pergunta'].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.bar(top_questions.index, top_questions.values)
    ax.set_title("Top 10 Perguntas Mais Feitas")
    ax.set_xlabel("Perguntas")
    ax.set_ylabel("Frequência")
    plt.xticks(rotation=45, ha='right')

    return salvando_imagem(fig), explicar_top_questions(df)

def explicar_avg_conversation_time(df):
    df['Data'] = pd.to_datetime(df['Data'])
    df['Tempo Atendimento'] = df.groupby("Id. Atendimento")['Data'].transform(lambda x: (x.max() - x.min()).seconds)
    avg_time = df.groupby("Id. Atendimento")["Tempo Atendimento"].mean()
    tempo_medio = avg_time.mean()

    return f"O tempo médio de atendimento foi de aproximadamente {int(tempo_medio)} segundos por sessão. Isso indica a média de duração entre o início e o fim das conversas com os usuários."

def plot_avg_conversation_time(df):
    df['Data'] = pd.to_datetime(df['Data'])
    df['Tempo Atendimento'] = df.groupby("Id. Atendimento")['Data'].transform(lambda x: (x.max() - x.min()).seconds)
    avg_time = df.groupby("Id. Atendimento")["Tempo Atendimento"].mean()

    fig, ax = plt.subplots()
    ax.hist(avg_time, bins=20, edgecolor='black')
    ax.set_title("Distribuição do Tempo Médio de Atendimento")
    ax.set_xlabel("Tempo (segundos)")
    ax.set_ylabel("Frequência")

    return salvando_imagem(fig), explicar_avg_conversation_time(df)