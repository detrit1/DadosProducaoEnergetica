from __future__ import annotations

import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT_DIR / "saida" / "producao_maritima_tratada.csv"
PASTA_SAIDA = ROOT_DIR / "resultados_mysql"
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "password"),
    "database": os.getenv("MYSQL_DATABASE", "producao_energetica"),
}

TABLE_NAME = os.getenv("MYSQL_TABLE", "producao_maritima")
