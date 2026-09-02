import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import  SQLAlchemyError
import pprint


banco_dados = create_engine("mysql+pymysql://User:password@host/database")

def extracao(local_extracao):
    query = """
   SELECT IDVENDA, QUANTIDADE, VALOR_UNITARIO 
   FROM VENDA 
    
    """
    df = pd.read_sql(query,local_extracao)
    pprint.pprint(df)
    return df


def tranformar(df):
    df["VALOR_TOTAL"] = df["QUANTIDADE"]*df["VALOR_UNITARIO"]
    pprint.pprint(df[["IDVENDA","VALOR_TOTAL","QUANTIDADE","VALOR_UNITARIO"]])
    return df

def carregar(df,local_carregar):
    df_para_carregar = df[["IDVENDA","VALOR_TOTAL"]].rename(columns={
        "IDVENDA": "ID_VENDA",
        "VALOR_TOTAL":"FATURAMENTO"
    })
    df_para_carregar.to_sql('LUCRO', local_carregar,if_exists="append",index=False)
    minha_query = """
    SELECT * FROM LUCRO
    """
    df_tabela_carregada = pd.read_sql(minha_query,local_carregar)
    pprint.pprint(df_tabela_carregada)


try:
    df_bruto = extracao(banco_dados)
    df_relatorio = tranformar(df_bruto)
    carregar(df_relatorio,banco_dados)
except SQLAlchemyError as erro:
    print(f"O erro foi:{erro}")

# Adicionar uma periodização
# melhorar a estrutura de tabelas, já que o produto é apenas uma venda (tabela de produtos, e referencial item_vendas)
# Adequar mais a realidade, (custo_produto(impostos)).