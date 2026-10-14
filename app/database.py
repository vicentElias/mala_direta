
import os

# Disponibiliza as bibliotecas do PostgreSQL antes de importar psycopg.
CAMINHO_POSTGRESQL = r"C:\Program Files\PostgreSQL\18\bin"

if os.path.isdir(CAMINHO_POSTGRESQL):
    os.environ["PATH"] = (
        CAMINHO_POSTGRESQL
        + os.pathsep
        + os.environ.get("PATH", "")
    )

import psycopg

from app.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def testar_conexao():
    try:
        with psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        ) as conexao:

            print("Conexão com PostgreSQL realizada com sucesso!")

            with conexao.cursor() as cursor:
                cursor.execute("SELECT version();")
                resultado = cursor.fetchone()

                print("PostgreSQL:")
                print(resultado[0])

    except Exception as erro:
        print("Erro ao conectar ao PostgreSQL:")
        print(erro)


if __name__ == "__main__":
    testar_conexao()