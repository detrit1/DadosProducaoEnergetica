import json
import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="BaconFrito2.0",
    database="producao_db"
)

cursor = conexao.cursor()


cursor.execute("SELECT * FROM producao")

for linha in cursor.fetchall():
    print(linha)