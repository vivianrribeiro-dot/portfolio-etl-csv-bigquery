# Pipeline ETL: CSV → BigQuery (Olist Brazilian E-Commerce)

Projeto de portfólio: pipeline ETL que extrai dados de arquivos CSV públicos,
limpa e transforma com Python/Pandas, e carrega o resultado no Google BigQuery.

## Dataset

[Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
(Kaggle) — pedidos reais de um marketplace brasileiro entre 2016 e 2018,
dividido em 9 CSVs relacionados (clientes, pedidos, itens, pagamentos,
avaliações, produtos, vendedores, geolocalização).

Por que esse dataset: é real, tem múltiplas tabelas relacionadas (exercita
limpeza e modelagem, não só um CSV solto), e é um case bem conhecido no
mercado de dados — fácil de explicar numa entrevista.

## Arquitetura

```
CSV (Kaggle)  →  Extract (pandas.read_csv)  →  Transform (limpeza)  →  Load (BigQuery)
data/raw/*.csv        src/extract.py            src/transform.py       src/load.py
```

- **Extract**: lê todos os CSVs em `data/raw/` e mapeia cada arquivo para o
  nome da tabela (ex.: `olist_orders_dataset.csv` → `orders`).
- **Transform**: normaliza nomes de colunas, remove espaços em strings,
  converte colunas de data, remove duplicatas exatas.
- **Load**: cria o dataset no BigQuery (se não existir) e carrega cada tabela
  com `WRITE_TRUNCATE` (pipeline idempotente — pode rodar de novo sem duplicar
  dados).

## Pré-requisitos

- Python 3.11+
- Conta Google com acesso ao Google Cloud
- Conta Kaggle (para baixar o dataset)

## Setup

### 1. Ambiente Python

```powershell
cd portfolio-etl-csv-bigquery
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Baixar o dataset

Opção A (recomendada) — via `kagglehub`, já incluso no `requirements.txt`:

```powershell
cd src
python download_data.py
```

Na primeira execução, se você não tiver um `kaggle.json` configurado, o
`kagglehub` abre o navegador para você logar e autorizar o acesso à sua conta
Kaggle. Depois disso, o script copia os CSVs automaticamente para
`data/raw/`.

Opção B — manual: baixe o .zip em
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce e extraia todos
os CSVs em `data/raw/`.

Opção C — via Kaggle CLI:

```powershell
pip install kaggle
# coloque seu token em %USERPROFILE%\.kaggle\kaggle.json (gerado em kaggle.com/settings)
kaggle datasets download -d olistbr/brazilian-ecommerce -p data/raw --unzip
```

### 3. Configurar o Google Cloud / BigQuery

Como é a primeira vez usando o BigQuery, o caminho mais simples é o
**BigQuery Sandbox**, que não exige cartão de crédito/billing (tem limites de
uso, mas são suficientes para este projeto):

1. Acesse https://console.cloud.google.com/ e crie um projeto novo.
2. No menu, abra o **BigQuery** — ao entrar pela primeira vez sem billing
   configurado, o Google ativa automaticamente o modo *Sandbox*.
3. Habilite a API: **APIs & Services → Enable APIs → BigQuery API**.
4. Crie credenciais para o Python acessar o projeto. Duas opções:
   - **Mais simples (recomendado para começar)**: instale o
     [gcloud CLI](https://cloud.google.com/sdk/docs/install) e rode:
     ```powershell
     gcloud auth application-default login
     gcloud config set project SEU_PROJECT_ID
     ```
   - **Service account** (mais parecido com produção): em
     **IAM & Admin → Service Accounts**, crie uma conta com os papéis
     `BigQuery Data Editor` e `BigQuery Job User`, gere uma chave JSON e baixe
     o arquivo.
5. Copie `.env.example` para `.env` e preencha:
   ```
   GCP_PROJECT_ID=seu-project-id
   BQ_DATASET=olist_ecommerce
   GOOGLE_APPLICATION_CREDENTIALS=caminho\para\sua-chave.json   # deixe vazio se usou application-default login
   ```

## Rodando o pipeline

Testar extração e transformação sem tocar no BigQuery:

```powershell
python src\main.py --dry-run
```

Rodar o pipeline completo (carrega no BigQuery):

```powershell
python src\main.py
```

Conferir no BigQuery (console ou `bq` CLI):

```sql
SELECT COUNT(*) FROM `seu-project-id.olist_ecommerce.orders`;
```

## Estrutura do projeto

```
portfolio-etl-csv-bigquery/
├── data/
│   ├── raw/          # CSVs originais (não versionados)
│   └── processed/    # saídas intermediárias opcionais (não versionados)
├── src/
│   ├── config.py      # variáveis de ambiente
│   ├── extract.py      # leitura dos CSVs
│   ├── transform.py    # limpeza/normalização
│   ├── load.py         # carga no BigQuery
│   └── main.py         # orquestração + CLI
├── requirements.txt
├── .env.example
└── README.md
```

## Habilidades demonstradas

- Extração de dados de múltiplos CSVs com Pandas
- Limpeza e padronização de dados (tipos, datas, duplicatas, strings)
- Modelagem de um pipeline ETL idempotente e parametrizável
- Integração com um data warehouse em nuvem (BigQuery) via API Python
- Boas práticas de projeto: variáveis de ambiente, `.gitignore`, documentação

## Possíveis melhorias futuras

- Orquestrar com Airflow ou Dagster
- Modelar um star schema (dbt) em vez de carregar as tabelas "como estão"
- Testes automatizados para as funções de transformação
- CI/CD (GitHub Actions) rodando o `--dry-run` a cada push
