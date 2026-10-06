"""Testes da leitura de CSVs em src/extract.py."""

from pathlib import Path

import pytest

from extract import _table_name_from_filename, extract_all


def test_nome_da_tabela_a_partir_do_arquivo():
    assert _table_name_from_filename(Path("olist_orders_dataset.csv")) == "orders"
    assert _table_name_from_filename(Path("olist_order_items_dataset.csv")) == "order_items"
    assert (
        _table_name_from_filename(Path("product_category_name_translation.csv"))
        == "product_category_name_translation"
    )


def test_extract_all_le_todos_os_csvs(tmp_path):
    (tmp_path / "olist_customers_dataset.csv").write_text("customer_id,state\n1,SP\n", encoding="utf-8")
    (tmp_path / "olist_sellers_dataset.csv").write_text("seller_id,state\n9,RJ\n", encoding="utf-8")

    tables = extract_all(tmp_path)

    assert set(tables) == {"customers", "sellers"}
    assert tables["customers"].loc[0, "state"] == "SP"


def test_extract_all_aceita_csv_com_bom(tmp_path):
    # O CSV de tradução do Olist vem com BOM; o nome da 1ª coluna não pode ser afetado.
    (tmp_path / "product_category_name_translation.csv").write_bytes(
        b"\xef\xbb\xbfproduct_category_name,product_category_name_english\nbeleza_saude,health_beauty\n"
    )

    tables = extract_all(tmp_path)

    assert "product_category_name" in tables["product_category_name_translation"].columns


def test_extract_all_sem_csv_gera_erro(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract_all(tmp_path)
