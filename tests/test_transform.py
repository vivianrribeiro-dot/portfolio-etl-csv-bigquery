"""Testes das funções de limpeza em src/transform.py."""

import pandas as pd

from transform import clean_all, clean_table


def test_normaliza_nomes_de_colunas():
    df = pd.DataFrame({" Order_ID ": ["a"], "Customer_State": ["SP"]})

    out = clean_table("t", df)

    assert list(out.columns) == ["order_id", "customer_state"]


def test_remove_espacos_das_strings():
    df = pd.DataFrame({"customer_city": ["  sao paulo ", "rio "]})

    out = clean_table("t", df)

    assert out["customer_city"].tolist() == ["sao paulo", "rio"]


def test_converte_colunas_de_data():
    df = pd.DataFrame(
        {
            "order_purchase_timestamp": ["2017-10-02 10:56:33"],
            "shipping_limit_date": ["2017-10-06 11:07:15"],
            "order_approved_at": ["2017-10-02 11:07:15"],
        }
    )

    out = clean_table("orders", df)

    for col in df.columns:
        assert pd.api.types.is_datetime64_any_dtype(out[col]), col


def test_data_invalida_vira_nat():
    df = pd.DataFrame(
        {
            "order_id": ["a", "b", "c"],
            "order_approved_at": ["2017-10-02 11:07:15", "nao e data", None],
        }
    )

    out = clean_table("orders", df)

    assert out["order_approved_at"].isna().tolist() == [False, True, True]


def test_nao_converte_colunas_que_nao_sao_data():
    df = pd.DataFrame(
        {
            "order_status": ["delivered"],
            "product_category_name": ["beleza_saude"],
            "geolocation_lat": [-23.5],
        }
    )

    out = clean_table("t", df)

    for col in ("order_status", "product_category_name"):
        assert not pd.api.types.is_datetime64_any_dtype(out[col]), col
        assert pd.api.types.is_string_dtype(out[col]), col
    assert out["geolocation_lat"].dtype == float


def test_remove_linhas_duplicadas():
    df = pd.DataFrame({"zip": ["01", "01", "02"], "city": ["sp", "sp", "rj"]})

    out = clean_table("geolocation", df)

    assert len(out) == 2


def test_clean_all_processa_todas_as_tabelas():
    tables = {"a": pd.DataFrame({" X ": [1]}), "b": pd.DataFrame({"Y": [2, 2]})}

    out = clean_all(tables)

    assert set(out) == {"a", "b"}
    assert list(out["a"].columns) == ["x"]
    assert len(out["b"]) == 1
