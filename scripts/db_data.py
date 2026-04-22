from __future__ import annotations

import logging

import pandas as pd

from db_config import CSV_PATH


def carregar_dados() -> pd.DataFrame | None:
    try:
        # A limpeza ja foi executada em processar_dados.py; aqui so carregamos o resultado tratado.
        df = pd.read_csv(CSV_PATH, encoding="utf-8")
        logging.info("Dados tratados carregados com sucesso: %s", CSV_PATH)
        return df

    except FileNotFoundError:
        logging.error("Arquivo tratado nao encontrado: %s", CSV_PATH)
        print(f"Erro: arquivo tratado nao encontrado em {CSV_PATH}")
        return None

    except pd.errors.EmptyDataError:
        logging.error("Arquivo tratado esta vazio: %s", CSV_PATH)
        print("Erro: arquivo tratado esta vazio.")
        return None

    except Exception as err:
        logging.error("Erro ao carregar dados tratados: %s", err)
        print("Erro ao carregar dados tratados:", err)
        return None


def filtrar_ultimos_10_anos(df: pd.DataFrame) -> pd.DataFrame | None:
    try:
        anos = sorted(df["ano"].dropna().astype(int).unique().tolist())
        if not anos:
            return df

        ultimos = anos[-10:]
        filtrado = df[df["ano"].isin(ultimos)].copy()
        logging.info("Filtragem dos ultimos 10 anos concluida: %s", ultimos)
        return filtrado

    except Exception as err:
        logging.error("Erro ao filtrar ultimos anos: %s", err)
        print("Erro ao filtrar dados:", err)
        return None
