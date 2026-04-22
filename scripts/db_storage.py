from __future__ import annotations

import logging
from typing import Any

import mysql.connector
import pandas as pd
from mysql.connector import errorcode

from db_config import DB_CONFIG, TABLE_NAME


UPSERT_SQL = f"""
INSERT INTO {TABLE_NAME} (
    ano,
    mes_ano,
    estado,
    bacia,
    campo,
    poco,
    ambiente,
    instalacao,
    producao_oleo_m3,
    producao_condensado_m3,
    producao_gas_associado_mm3,
    producao_gas_nao_associado_mm3,
    producao_agua_m3,
    injecao_gas_mm3,
    injecao_agua_recuperacao_secundaria_m3,
    injecao_agua_descarte_m3,
    injecao_gas_carbonico_mm3,
    injecao_nitrogenio_mm3,
    injecao_vapor_agua_t,
    injecao_polimeros_m3,
    injecao_outros_fluidos_m3,
    competencia,
    fonte_arquivo
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON DUPLICATE KEY UPDATE
    ano = VALUES(ano),
    mes_ano = VALUES(mes_ano),
    ambiente = VALUES(ambiente),
    instalacao = VALUES(instalacao),
    producao_oleo_m3 = VALUES(producao_oleo_m3),
    producao_condensado_m3 = VALUES(producao_condensado_m3),
    producao_gas_associado_mm3 = VALUES(producao_gas_associado_mm3),
    producao_gas_nao_associado_mm3 = VALUES(producao_gas_nao_associado_mm3),
    producao_agua_m3 = VALUES(producao_agua_m3),
    injecao_gas_mm3 = VALUES(injecao_gas_mm3),
    injecao_agua_recuperacao_secundaria_m3 = VALUES(injecao_agua_recuperacao_secundaria_m3),
    injecao_agua_descarte_m3 = VALUES(injecao_agua_descarte_m3),
    injecao_gas_carbonico_mm3 = VALUES(injecao_gas_carbonico_mm3),
    injecao_nitrogenio_mm3 = VALUES(injecao_nitrogenio_mm3),
    injecao_vapor_agua_t = VALUES(injecao_vapor_agua_t),
    injecao_polimeros_m3 = VALUES(injecao_polimeros_m3),
    injecao_outros_fluidos_m3 = VALUES(injecao_outros_fluidos_m3)
"""


def _to_record(row: pd.Series) -> tuple[Any, ...]:
    competencia = pd.to_datetime(row.get("competencia"), errors="coerce")
    competencia_out = None if pd.isna(competencia) else competencia.date()

    return (
        None if pd.isna(row.get("ano")) else int(row["ano"]),
        None if pd.isna(row.get("mes_ano")) else str(row["mes_ano"]),
        None if pd.isna(row.get("estado")) else str(row["estado"]),
        None if pd.isna(row.get("bacia")) else str(row["bacia"]),
        None if pd.isna(row.get("campo")) else str(row["campo"]),
        None if pd.isna(row.get("poco")) else str(row["poco"]),
        None if pd.isna(row.get("ambiente")) else str(row["ambiente"]),
        None if pd.isna(row.get("instalacao")) else str(row["instalacao"]),
        None if pd.isna(row.get("producao_oleo_m3")) else float(row["producao_oleo_m3"]),
        None if pd.isna(row.get("producao_condensado_m3")) else float(row["producao_condensado_m3"]),
        None if pd.isna(row.get("producao_gas_associado_mm3")) else float(row["producao_gas_associado_mm3"]),
        None if pd.isna(row.get("producao_gas_nao_associado_mm3")) else float(row["producao_gas_nao_associado_mm3"]),
        None if pd.isna(row.get("producao_agua_m3")) else float(row["producao_agua_m3"]),
        None if pd.isna(row.get("injecao_gas_mm3")) else float(row["injecao_gas_mm3"]),
        None if pd.isna(row.get("injecao_agua_recuperacao_secundaria_m3")) else float(row["injecao_agua_recuperacao_secundaria_m3"]),
        None if pd.isna(row.get("injecao_agua_descarte_m3")) else float(row["injecao_agua_descarte_m3"]),
        None if pd.isna(row.get("injecao_gas_carbonico_mm3")) else float(row["injecao_gas_carbonico_mm3"]),
        None if pd.isna(row.get("injecao_nitrogenio_mm3")) else float(row["injecao_nitrogenio_mm3"]),
        None if pd.isna(row.get("injecao_vapor_agua_t")) else float(row["injecao_vapor_agua_t"]),
        None if pd.isna(row.get("injecao_polimeros_m3")) else float(row["injecao_polimeros_m3"]),
        None if pd.isna(row.get("injecao_outros_fluidos_m3")) else float(row["injecao_outros_fluidos_m3"]),
        competencia_out,
        None if pd.isna(row.get("fonte_arquivo")) else str(row["fonte_arquivo"]),
    )


def salvar_no_mysql(df: pd.DataFrame) -> None:
    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        registros = [_to_record(row) for _, row in df.iterrows()]
        cursor.executemany(UPSERT_SQL, registros)

        conn.commit()
        logging.info("Dados salvos no MySQL com sucesso. Registros processados: %s", len(registros))

    except mysql.connector.Error as err:
        if conn is not None:
            conn.rollback()

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro de usuario ou senha.")
            logging.error("Erro de usuario ou senha.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Banco de dados nao existe.")
            logging.error("Banco de dados nao existe.")
        else:
            print("Erro no MySQL:", err)
            logging.error("Erro ao salvar no MySQL: %s", err)

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()


def consultar_dados() -> pd.DataFrame | None:
    conn = None

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        query = f"SELECT * FROM {TABLE_NAME}"
        df = pd.read_sql(query, conn)
        logging.info("Consulta ao banco executada com sucesso.")
        return df

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro de usuario ou senha.")
            logging.error("Erro de usuario ou senha.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Banco de dados nao existe.")
            logging.error("Banco de dados nao existe.")
        else:
            print("Erro no MySQL:", err)
            logging.error("Erro ao consultar dados: %s", err)
        return None

    except Exception as err:
        print("Erro ao consultar dados:", err)
        logging.error("Erro geral ao consultar dados: %s", err)
        return None

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
