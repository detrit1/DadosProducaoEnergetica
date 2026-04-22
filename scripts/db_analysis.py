from __future__ import annotations

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def calcular_estatisticas(df: pd.DataFrame, pasta_saida: Path) -> None:
    try:
        col = "producao_oleo_m3"
        stats = df[col].describe()

        print("\nESTATISTICAS (producao_oleo_m3):")
        print(stats)

        caminho_stats = pasta_saida / "estatisticas_producao_oleo.txt"
        with caminho_stats.open("w", encoding="utf-8") as file:
            file.write("ESTATISTICAS DE PRODUCAO DE OLEO (m3)\n\n")
            file.write(str(stats))

        logging.info("Estatisticas calculadas e salvas com sucesso.")

    except Exception as err:
        logging.error("Erro ao calcular estatisticas: %s", err)
        print("Erro ao calcular estatisticas:", err)


def grafico_barras(df: pd.DataFrame, pasta_saida: Path) -> None:
    try:
        vendas_ano = df.groupby("ano")["producao_oleo_m3"].sum(min_count=1)

        plt.figure(figsize=(10, 6))
        plt.bar(vendas_ano.index.astype(str), vendas_ano.values)
        plt.title("Total de Producao de Oleo por Ano")
        plt.xlabel("Ano")
        plt.ylabel("Producao Total (m3)")
        plt.xticks(rotation=45)
        plt.tight_layout()

        caminho = pasta_saida / "grafico_barras_producao_ano.png"
        plt.savefig(caminho)
        plt.close()

        logging.info("Grafico de barras gerado com sucesso.")

    except Exception as err:
        logging.error("Erro ao gerar grafico de barras: %s", err)
        print("Erro ao gerar grafico de barras:", err)


def grafico_area_empilhada(df: pd.DataFrame, pasta_saida: Path) -> None:
    try:
        tabela = df.pivot_table(
            index="ano",
            columns="estado",
            values="producao_oleo_m3",
            aggfunc="sum",
            fill_value=0,
        )

        plt.figure(figsize=(11, 6))
        plt.stackplot(tabela.index, tabela.T.values, labels=tabela.columns)
        plt.title("Evolucao da Producao de Oleo por Estado")
        plt.xlabel("Ano")
        plt.ylabel("Producao (m3)")
        plt.legend(title="Estado", loc="upper left")
        plt.tight_layout()

        caminho = pasta_saida / "grafico_area_estados.png"
        plt.savefig(caminho)
        plt.close()

        logging.info("Grafico de area empilhada gerado com sucesso.")

    except Exception as err:
        logging.error("Erro ao gerar grafico de area empilhada: %s", err)
        print("Erro ao gerar grafico de area empilhada:", err)
