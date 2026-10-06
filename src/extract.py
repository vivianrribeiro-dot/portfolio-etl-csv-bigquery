"""Extração: lê os CSVs brutos do Olist e devolve um dict {nome_tabela: DataFrame}."""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def _table_name_from_filename(path: Path) -> str:
    name = path.stem
    name = name.removeprefix("olist_")
    name = name.removesuffix("_dataset")
    return name


def extract_all(raw_dir: Path) -> dict[str, pd.DataFrame]:
    csv_files = sorted(raw_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(
            f"Nenhum CSV encontrado em {raw_dir}. "
            "Baixe o dataset do Kaggle (olistbr/brazilian-ecommerce) e extraia os CSVs nessa pasta."
        )

    tables: dict[str, pd.DataFrame] = {}
    for csv_path in csv_files:
        table_name = _table_name_from_filename(csv_path)
        logger.info("Lendo %s -> tabela '%s'", csv_path.name, table_name)
        tables[table_name] = pd.read_csv(csv_path)

    return tables
