"""Carga: envia os DataFrames limpos para o BigQuery."""

import logging

import pandas as pd
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

logger = logging.getLogger(__name__)


def _ensure_dataset(client: bigquery.Client, project_id: str, dataset_id: str) -> None:
    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
    try:
        client.get_dataset(dataset_ref)
        logger.info("Dataset '%s' já existe", dataset_id)
    except NotFound:
        logger.info("Criando dataset '%s'", dataset_id)
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        client.create_dataset(dataset)


def load_all(
    tables: dict[str, pd.DataFrame],
    project_id: str,
    dataset_id: str,
) -> None:
    client = bigquery.Client(project=project_id)
    _ensure_dataset(client, project_id, dataset_id)

    for table_name, df in tables.items():
        table_ref = f"{project_id}.{dataset_id}.{table_name}"
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            autodetect=True,
        )

        logger.info("Carregando %d linhas em %s", len(df), table_ref)
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()

        table = client.get_table(table_ref)
        logger.info("Tabela %s agora tem %d linhas", table_ref, table.num_rows)
