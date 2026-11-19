
import psycopg

from app.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def listar_destinatarios():
    """Consulta os destinatários sem alterar o banco."""

    with psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    ) as conexao:

        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    nome,
                    empresa,
                    email,
                    ativo,
                    data_cadastro
                FROM destinatarios
                ORDER BY id;
                """
            )

            destinatarios = cursor.fetchall()

    return destinatarios
