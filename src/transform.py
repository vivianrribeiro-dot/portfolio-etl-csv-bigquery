"""Transformação/limpeza dos dados antes da carga no BigQuery."""

import logging

import pandas as pd

logger = logging.getLogger(__name__)

DATE_COLUMN_HINTS = ("_date", "_timestamp", "_at")


def _clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().lower() for c in df.columns]
    return df


def _strip_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    object_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in object_cols:
        df[col] = df[col].str.strip()
    return df


def _parse_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if any(hint in col for hint in DATE_COLUMN_HINTS):
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def clean_table(name: str, df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Limpando tabela '%s' (%d linhas, %d colunas)", name, len(df), df.shape[1])

    df = _clean_column_names(df)
    df = _strip_string_columns(df)
    df = _parse_date_columns(df)

    before = len(df)
    df = df.drop_duplicates()
    if len(df) != before:
        logger.info("Tabela '%s': removidas %d linhas duplicadas", name, before - len(df))

    return df


def clean_all(tables: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    return {name: clean_table(name, df) for name, df in tables.items()}
