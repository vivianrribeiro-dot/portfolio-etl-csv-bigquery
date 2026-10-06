"""Orquestra o pipeline ETL: extract -> transform -> load."""

import argparse
import logging

from config import BQ_DATASET, GCP_PROJECT_ID, RAW_DATA_DIR
from extract import extract_all
from transform import clean_all
from load import load_all

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def run(dry_run: bool) -> None:
    logger.info("Iniciando pipeline (dry_run=%s)", dry_run)

    raw_tables = extract_all(RAW_DATA_DIR)
    clean_tables = clean_all(raw_tables)

    if dry_run:
        logger.info("Dry-run ativado: pulando carga no BigQuery")
        for name, df in clean_tables.items():
            logger.info("  %-12s %6d linhas  %2d colunas", name, len(df), df.shape[1])
        return

    if not GCP_PROJECT_ID:
        raise RuntimeError("GCP_PROJECT_ID não configurado. Preencha o arquivo .env.")

    load_all(clean_tables, project_id=GCP_PROJECT_ID, dataset_id=BQ_DATASET)
    logger.info("Pipeline finalizado com sucesso")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline ETL CSV -> BigQuery (dataset Olist)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Executa extract + transform e mostra o resumo, sem carregar no BigQuery",
    )
    args = parser.parse_args()
    run(dry_run=args.dry_run)
