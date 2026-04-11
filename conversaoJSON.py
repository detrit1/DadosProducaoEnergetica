import csv
import glob

dados_filtrados = []

arquivos = glob.glob("dados/*.csv")  # pega todos os CSVs da pasta

def converter_numero(valor):
    if valor is None or valor == "":
        return 0.0

    # se já for número, só retorna
    if isinstance(valor, (int, float)):
        return float(valor)

    # se for string, trata
    valor = str(valor)
    valor = valor.replace(".", "").replace(",", ".")

    try:
        return float(valor)
    except:
        return 0.0

for nome_arquivo in arquivos:
    with open(nome_arquivo, newline='', encoding='utf-8-sig') as arquivo:
        leitor = csv.DictReader(arquivo)
        
        for linha in leitor:
            registro = {
                "ano": linha["Ano"],
                "estado": linha["Estado"],
                "bacia": linha["Bacia"],
                "instalacao": linha["Instalação"],
                "oleo": converter_numero(linha["ProducaoOleoMetrosCubicos"] or 0)
            }
            dados_filtrados.append(registro)

print(len(dados_filtrados))

import json

with open("dados_filtrados.json", "w", encoding="utf-8") as f:
    json.dump(dados_filtrados, f, ensure_ascii=False, indent=4)