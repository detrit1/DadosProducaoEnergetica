from __future__ import annotations

import logging

import mysql.connector
from mysql.connector import errorcode

from db_config import DB_CONFIG, TABLE_NAME


def criar_estrutura() -> None:
    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )
        cursor = conn.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} "
            "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        cursor.execute(f"USE {DB_CONFIG['database']}")
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                ano SMALLINT,
                mes_ano CHAR(7),
                estado VARCHAR(100),
                bacia VARCHAR(100),
                campo VARCHAR(120),
                poco VARCHAR(120),
                ambiente VARCHAR(40),
                instalacao VARCHAR(180),
                producao_oleo_m3 DECIMAL(18,5),
                producao_condensado_m3 DECIMAL(18,5),
                producao_gas_associado_mm3 DECIMAL(18,5),
                producao_gas_nao_associado_mm3 DECIMAL(18,5),
                producao_agua_m3 DECIMAL(18,5),
                injecao_gas_mm3 DECIMAL(18,5),
                injecao_agua_recuperacao_secundaria_m3 DECIMAL(18,5),
                injecao_agua_descarte_m3 DECIMAL(18,5),
                injecao_gas_carbonico_mm3 DECIMAL(18,5),
                injecao_nitrogenio_mm3 DECIMAL(18,5),
                injecao_vapor_agua_t DECIMAL(18,5),
                injecao_polimeros_m3 DECIMAL(18,5),
                injecao_outros_fluidos_m3 DECIMAL(18,5),
                competencia DATE,
                fonte_arquivo VARCHAR(255) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id),
                UNIQUE KEY uk_registro (
                    competencia,
                    estado,
                    bacia,
                    campo,
                    poco,
                    fonte_arquivo
                ),
                INDEX idx_competencia (competencia),
                INDEX idx_localizacao (estado, bacia, campo, poco),
                INDEX idx_fonte_arquivo (fonte_arquivo)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        )

        conn.commit()
        logging.info("Banco e tabela verificados/criados com sucesso.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro de usuario ou senha.")
            logging.error("Erro de usuario ou senha no MySQL.")
        else:
            print("Erro no MySQL ao criar estrutura:", err)
            logging.error("Erro no MySQL ao criar estrutura: %s", err)

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()
