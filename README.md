# ETL Simples — VENDA → LUCRO

Projeto de estudo de ETL (Extração, Transformação e Carga) usando Python e MySQL. O script lê os dados de vendas da tabela `VENDA`, calcula o valor total de cada venda e carrega o resultado na tabela `LUCRO`.

## 🎯 Objetivo

Praticar um pipeline de ETL simples, do zero: conectar em um banco relacional, extrair dados com SQL, transformar com `pandas` e carregar o resultado em outra tabela do mesmo banco.

## 🗂️ Estrutura do banco de dados

O banco `VENDAS` (script em `BANCO_DADOS_VENDAS.sql`) possui duas tabelas:

**VENDA** — registro bruto de cada venda
| Coluna | Tipo | Descrição |
|---|---|---|
| IDVENDA | INT (PK, auto increment) | Identificador da venda |
| NOME_PRODUTO | VARCHAR(30) | Nome do produto vendido |
| VALOR_UNITARIO | DECIMAL(10,2) | Preço unitário |
| QUANTIDADE | INT | Quantidade vendida |
| DATA_VENDA | DATETIME | Data/hora da venda (padrão: momento do insert) |

**LUCRO** — resultado calculado pelo ETL
| Coluna | Tipo | Descrição |
|---|---|---|
| IDLUCRO | INT (PK, auto increment) | Identificador do registro |
| ID_VENDA | INT (FK → VENDA.IDVENDA) | Venda de origem |
| FATURAMENTO | DECIMAL(10,2) | Campo calculado: `QUANTIDADE * VALOR_UNITARIO` |
| DATA_ATUALIZACAO | DATETIME | Atualizada automaticamente a cada UPDATE |

## ⚙️ Como o ETL funciona (`Etl_Simples.py`)

O script segue três etapas clássicas de ETL:

1. **Extração (`extracao`)** — consulta `IDVENDA`, `QUANTIDADE` e `VALOR_UNITARIO` na tabela `VENDA` e carrega o resultado em um DataFrame do pandas.
2. **Transformação (`tranformar`)** — cria a coluna `VALOR_TOTAL`, multiplicando `QUANTIDADE` por `VALOR_UNITARIO`.
3. **Carga (`carregar`)** — renomeia as colunas para o formato da tabela `LUCRO` (`IDVENDA` → `ID_VENDA`, `VALOR_TOTAL` → `FATURAMENTO`) e insere os dados com `to_sql(if_exists="append")`. Em seguida, lê a tabela `LUCRO` de volta para conferência.

Toda a execução é envolvida em um bloco `try/except` que captura erros de `SQLAlchemyError`.

## 🛠️ Tecnologias usadas

- **Python 3**
- **[pandas](https://pandas.pydata.org/)** — manipulação dos dados em DataFrame
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — conexão com o banco (`create_engine`)
- **[PyMySQL](https://pymysql.readthedocs.io/)** — driver de conexão MySQL usado pela SQLAlchemy (`mysql+pymysql`)
- **pprint** — impressão formatada dos DataFrames no console, para debug

## ▶️ Como executar

1. Crie o banco e as tabelas executando `BANCO_DADOS_VENDAS.sql` no MySQL.
2. Instale as dependências:
   ```bash
   pip install pandas sqlalchemy pymysql
   ```
3. Configure a string de conexão em `Etl_Simples.py`:
   ```python
   banco_dados = create_engine("mysql+pymysql://usuario:senha@host/database")
   ```
4. Rode o script:
   ```bash
   python Etl_Simples.py
   ```
   O script vai extrair os dados de `VENDA`, calcular o faturamento e inserir os resultados em `LUCRO`, exibindo os DataFrames no console em cada etapa.

## 📌 Observações

- O script `BANCO_DADOS_VENDAS.sql` contém um erro de digitação (`CREATE DATABESE` em vez de `CREATE DATABASE`) — corrija antes de executar.
- Rodar o ETL mais de uma vez sobre os mesmos dados vai duplicar os registros em `LUCRO`, pois a carga usa `if_exists="append"` sem checagem de duplicidade.

## 🚧 Próximos passos

- Adicionar uma periodização ao processo de ETL.
- Melhorar a estrutura das tabelas — hoje um "produto" é tratado como se fosse a própria venda; o ideal seria separar em uma tabela de produtos e uma tabela de itens de venda.
- Aproximar o modelo da realidade, considerando custos do produto (ex: impostos) no cálculo do faturamento.