from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import unicodedata
from pathlib import Path
from typing import Dict, List


def normalize_key(value: str) -> str:
    text = unicodedata.normalize("NFKD", value)
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = text.lower().strip().replace("[", "").replace("]", "")
    return "".join(char for char in text if char.isalnum())


def to_float_ptbr(value: object) -> float:
    if value is None or value == "":
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip().replace(".", "").replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return 0.0


def to_int(value: object) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(str(value).strip())
    except ValueError:
        return None


def extract_record(row: Dict[str, str]) -> Dict[str, object]:
    normalized = {normalize_key(k): v for k, v in row.items()}

    ano = to_int(normalized.get("ano"))
    estado = str(normalized.get("estado", "")).strip()
    bacia = str(normalized.get("bacia", "")).strip()
    instalacao = str(normalized.get("instalacao", "")).strip()

    # O dataset pode trazer cabecalhos em formatos distintos.
    oleo_raw = (
        normalized.get("producaodeoleom3")
        or normalized.get("producaooleometroscubicos")
        or normalized.get("producaodeoleometroscubicos")
        or normalized.get("oleo")
        or 0
    )

    return {
        "ano": ano,
        "estado": estado,
        "bacia": bacia,
        "instalacao": instalacao,
        "oleo": to_float_ptbr(oleo_raw),
    }


def process_csv_files(input_pattern: str) -> List[Dict[str, object]]:
    records: List[Dict[str, object]] = []
    files = sorted(glob.glob(input_pattern))

    for csv_file in files:
        with open(csv_file, newline="", encoding="utf-8-sig") as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                records.append(extract_record(row))

    return records


def save_json(records: List[Dict[str, object]], output_file: Path) -> None:
    with output_file.open("w", encoding="utf-8") as fp:
        json.dump(records, fp, ensure_ascii=False, indent=2)


def print_stats(records: List[Dict[str, object]]) -> None:
    if not records:
        print("Nenhum registro encontrado para calcular estatisticas.")
        return

    import pandas as pd

    df = pd.DataFrame(records)
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
    df["oleo"] = pd.to_numeric(df["oleo"], errors="coerce")

    print("\nEstatisticas de oleo por ano (media, maximo, minimo):")
    print(df.groupby("ano")["oleo"].agg(["mean", "max", "min"]).round(2))

    print("\nEstatisticas de oleo por estado (media, maximo, minimo):")
    print(df.groupby("estado")["oleo"].agg(["mean", "max", "min"]).round(2))

    print("\nEstatisticas de oleo por bacia (media, maximo, minimo):")
    print(df.groupby("bacia")["oleo"].agg(["mean", "max", "min"]).round(2))


def save_plots(records: List[Dict[str, object]], output_dir: Path) -> None:
    if not records:
        print("Nenhum registro encontrado para gerar graficos.")
        return

    import matplotlib.pyplot as plt
    import pandas as pd

    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(records)
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")

    fig = df.groupby("ano").size().plot(kind="bar", title="Registros por Ano").get_figure()
    fig.savefig(output_dir / "registros_por_ano.png", bbox_inches="tight")
    plt.close(fig)

    if "estado" in df.columns:
        fig = df["estado"].value_counts().plot(kind="bar", title="Distribuicao por Estado").get_figure()
        fig.savefig(output_dir / "distribuicao_por_estado.png", bbox_inches="tight")
        plt.close(fig)

    fig = df["bacia"].value_counts().head(10).plot(kind="bar", title="Top 10 Bacias").get_figure()
    fig.savefig(output_dir / "top_10_bacias.png", bbox_inches="tight")
    plt.close(fig)

    fig = df["instalacao"].value_counts().head(10).plot(kind="bar", title="Top 10 Instalacoes").get_figure()
    fig.savefig(output_dir / "top_10_instalacoes.png", bbox_inches="tight")
    plt.close(fig)

    print(f"Graficos gerados em: {output_dir}")


def load_into_mysql(records: List[Dict[str, object]]) -> None:
    import mysql.connector
    from mysql.connector import Error

    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "producao_db")

    try:
        conn = mysql.connector.connect(host=host, user=user, password=password)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        cursor.execute(f"USE {database}")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS producao (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ano INT,
                estado VARCHAR(120),
                bacia VARCHAR(120),
                instalacao VARCHAR(160),
                oleo DOUBLE
            )
            """
        )

        cursor.executemany(
            """
            INSERT INTO producao (ano, estado, bacia, instalacao, oleo)
            VALUES (%s, %s, %s, %s, %s)
            """,
            [
                (
                    row.get("ano"),
                    row.get("estado"),
                    row.get("bacia"),
                    row.get("instalacao"),
                    row.get("oleo", 0.0),
                )
                for row in records
            ],
        )

        conn.commit()
        print(f"Dados inseridos no MySQL: {len(records)} registros.")
    except Error as exc:
        print(f"Falha ao inserir no MySQL: {exc}")
        print("Dica: rode sem --mysql para processar apenas CSV/JSON e estatisticas.")
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pipeline unica: trata CSV, gera JSON, calcula estatisticas e opcionalmente carrega no MySQL."
    )
    parser.add_argument("--input-pattern", default="dados/*.csv", help="Padrao dos CSVs de entrada.")
    parser.add_argument("--output-json", default="dados_filtrados.json", help="Arquivo JSON de saida.")
    parser.add_argument("--plots", action="store_true", help="Gera graficos em PNG na pasta graficos.")
    parser.add_argument("--mysql", action="store_true", help="Carrega os dados no MySQL.")

    args = parser.parse_args()

    records = process_csv_files(args.input_pattern)
    save_json(records, Path(args.output_json))

    print(f"Total de registros processados: {len(records)}")
    print(f"JSON gerado em: {args.output_json}")

    print_stats(records)

    if args.plots:
        save_plots(records, Path("graficos"))

    if args.mysql:
        load_into_mysql(records)


if __name__ == "__main__":
    main()
