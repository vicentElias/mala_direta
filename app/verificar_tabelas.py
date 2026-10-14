
import psycopg

from app.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def verificar_tabelas():
    with psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    ) as conexao:

        with conexao.cursor() as cursor:
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)

            tabelas = cursor.fetchall()

            print("Tabelas encontradas no PostgreSQL:")
            print()

            for tabela in tabelas:
                print(f"- {tabela[0]}")

            esperadas = {
                "destinatarios",
                "campanhas",
                "envios",
            }

            encontradas = {tabela[0] for tabela in tabelas}
            faltantes = esperadas - encontradas

            print()

            if not faltantes:
                print("Sucesso! As três tabelas esperadas existem.")
            else:
                print("Atenção! Tabelas não encontradas:")
                for tabela in sorted(faltantes):
                    print(f"- {tabela}")


if __name__ == "__main__":
    verificar_tabelas()