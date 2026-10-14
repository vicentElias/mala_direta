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


def cadastrar_campanha(nome, assunto, modelo_html):
    """Cadastra uma campanha no banco, sem enviar e-mails."""

    nome = nome.strip()
    assunto = assunto.strip()

    if not nome:
        raise ValueError("O nome da campanha é obrigatório.")

    if not assunto:
        raise ValueError("O assunto do e-mail é obrigatório.")

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
                INSERT INTO campanhas (nome, assunto, modelo_html)
                VALUES (%s, %s, %s)
                RETURNING id, nome, assunto, data_criacao;
                """,
                (nome, assunto, modelo_html),
            )

            campanha = cursor.fetchone()

    return campanha


def listar_campanhas():
    """Lista as campanhas cadastradas, sem enviar e-mails."""

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
                SELECT id, nome, assunto, data_criacao, ativo
                FROM campanhas
                ORDER BY id DESC;
                """
            )

            return cursor.fetchall()


def obter_campanha(campanha_id):
    """Busca os dados completos de uma campanha pelo ID."""

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
                SELECT id, nome, assunto, modelo_html, data_criacao, ativo
                FROM campanhas
                WHERE id = %s;
                """,
                (campanha_id,),
            )

            campanha = cursor.fetchone()

    return campanha


def atualizar_campanha(campanha_id, nome, assunto, modelo_html):
    """Atualiza uma campanha existente sem criar outra."""

    nome = nome.strip()
    assunto = assunto.strip()

    if not nome:
        raise ValueError("O nome da campanha é obrigatório.")

    if not assunto:
        raise ValueError("O assunto do e-mail é obrigatório.")

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
                UPDATE campanhas
                SET nome = %s,
                    assunto = %s,
                    modelo_html = %s
                WHERE id = %s
                RETURNING id, nome, assunto, data_criacao;
                """,
                (nome, assunto, modelo_html, campanha_id),
            )

            campanha = cursor.fetchone()

    if campanha is None:
        raise ValueError(
            f"Nenhuma campanha encontrada com o ID {campanha_id}."
        )

    return campanha


def alterar_status_campanha(campanha_id, ativo):
    """Ativa ou desativa uma campanha existente."""

    if not isinstance(ativo, bool):
        raise ValueError("O status deve ser True ou False.")

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
                UPDATE campanhas
                SET ativo = %s
                WHERE id = %s
                RETURNING id, nome, ativo;
                """,
                (ativo, campanha_id),
            )

            campanha = cursor.fetchone()

    if campanha is None:
        raise ValueError(
            f"Nenhuma campanha encontrada com o ID {campanha_id}."
        )

    return campanha


if __name__ == "__main__":
    print("Módulo de campanhas preparado.")
    print("Nenhuma campanha foi criada e nenhum e-mail foi enviado.")