import json
import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="senhaBoa",
    database="producao_db"
)

cursor = conexao.cursor()


with open("dados_filtrados.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

for d in dados:
    cursor.execute("""
        INSERT INTO producao (ano, estado, bacia, instalacao, oleo)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        d.get("ano"),
        d.get("estado"),
        d.get("bacia"),
        d.get("instalacao"),
        d.get("oleo", 0)
    ))

conexao.commit()
print("Dados inseridos!")
