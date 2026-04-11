import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="senhaBoa",
    database="producao_db"
)

cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS producao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ano INT,
    estado VARCHAR(50),
    bacia VARCHAR(100),
    instalacao VARCHAR(100),
    oleo DOUBLE
)
""")

print("Tabela criada com sucesso!")
