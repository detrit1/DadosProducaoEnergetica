from __future__ import annotations

import logging

from db_analysis import calcular_estatisticas, grafico_area_empilhada, grafico_barras
from db_config import PASTA_SAIDA
from db_data import carregar_dados, filtrar_ultimos_10_anos
from db_schema import criar_estrutura
from db_storage import consultar_dados, salvar_no_mysql

logging.basicConfig(
    filename=PASTA_SAIDA / "pipeline_mysql.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main() -> None:
    try:
        logging.info("Iniciando pipeline MySQL")

        df = carregar_dados()
        if df is None:
            return

        df_filtrado = filtrar_ultimos_10_anos(df)
        if df_filtrado is None or df_filtrado.empty:
            print("Erro: nao ha dados validos para processar.")
            logging.warning("DataFrame vazio apos filtragem.")
            return

        criar_estrutura()
        salvar_no_mysql(df_filtrado)

        df_db = consultar_dados()
        if df_db is None or df_db.empty:
            print("Erro: nao foi possivel consultar dados do banco.")
            logging.warning("Consulta retornou vazia.")
            return

        calcular_estatisticas(df_db, PASTA_SAIDA)
        grafico_barras(df_db, PASTA_SAIDA)
        grafico_area_empilhada(df_db, PASTA_SAIDA)

        logging.info("Pipeline executado com sucesso.")
        print("Pipeline MySQL executado com sucesso.")
        print(f"Resultados salvos em: {PASTA_SAIDA}")

    except Exception as err:
        logging.error("Erro geral no pipeline: %s", err)
        print("Erro:", err)


if __name__ == "__main__":
    main()
