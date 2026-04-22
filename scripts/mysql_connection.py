from __future__ import annotations

import mysql.connector
from mysql.connector import errorcode

from db_config import DB_CONFIG


def testar_conexao() -> None:
    cnx = None
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        print("Conexao com MySQL estabelecida com sucesso.")
        print(
            f"Servidor: {DB_CONFIG['host']}:{DB_CONFIG['port']} | "
            f"Banco: {DB_CONFIG['database']} | Usuario: {DB_CONFIG['user']}"
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro de usuario ou senha.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Banco de dados nao existe.")
        else:
            print(err)
    finally:
        if cnx is not None and cnx.is_connected():
            cnx.close()


if __name__ == "__main__":
    testar_conexao()