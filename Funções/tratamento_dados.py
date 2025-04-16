import pandas as pd
import unicodedata

def carregar_dados(caminhos_arquivos, separador, codificacao):
    dataframes = []
    for caminho_arquivo in caminhos_arquivos:
        df = pd.read_csv(caminho_arquivo, sep=separador, encoding=codificacao)
        dataframes.append(df)
        df.columns = [
        unicodedata.normalize("NFKD", col)
        .encode("ascii", "ignore")
        .decode("utf-8")
        .strip()
        .upper()
        .replace("Ã", "A")
        .replace("¢", "C")
        .replace("¬", " ")
        .replace("I12", "O")  # conserta erros recorrentes específicos
        for col in df.columns
        ]
        mapeamento_colunas = {
            "CODIGO ORGOO SUPERIOR": "CODIGO ORGAO SUPERIOR",
            "NOME ORGOO SUPERIOR": "NOME ORGAO SUPERIOR",
            "CODIGO ORGOO": "CODIGO ORGAO",
            "NOME ORGOO": "NOME ORGAO",
            "MOS EXTRATO": "MES EXTRATO",
            "NOMERO CONVONIO": "NUMERO CONVENIO",
            "TRANSAOOO": "TRANSACAO",
            "DATA TRANSAOOO": "DATA TRANSACAO",
            "VALOR TRANSAOOO": "VALOR TRANSACAO",
        }
        df.rename(columns=mapeamento_colunas, inplace=True)
    return dataframes

def junta_dados(dfs: list):
    return pd.concat(dfs, ignore_index=True)

def limpar_dados(df):
    # Remove linhas com qualquer valor nulo
    df.dropna(how='all', inplace=True)
    
    # Remove duplicatas
    df.drop_duplicates(inplace=True)

    return df

def converter_para_datetime(df, colunas):
    df[colunas] = pd.to_datetime(df[colunas], infer_datetime_format=True, dayfirst=True, errors='coerce')
    return df

def converter_para_valor(df, colunas):
    df[colunas] = df[colunas].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
    return df

def converter_para_int(df, colunas):
    df[colunas] = df[colunas].astype(int)
    return df