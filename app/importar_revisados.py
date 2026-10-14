
from pathlib import Path

import openpyxl
import psycopg

from app.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)

ARQUIVO = Path("data/contatos_para_conferencia.xlsx")


def importar_revisados():
    if not ARQUIVO.exists():
        print(f"Arquivo não encontrado: {ARQUIVO.resolve()}")
        return

    workbook = openpyxl.load_workbook(
        ARQUIVO,
        read_only=True,
        data_only=True,
    )

    planilha = workbook["Contatos"]
    linhas = planilha.iter_rows(values_only=True)

    cabecalho = next(linhas, None)

    if not cabecalho:
        workbook.close()
        print("O arquivo não contém dados.")
        return

    indices = {
        str(nome).strip().lower(): i
        for i, nome in enumerate(cabecalho)
        if nome is not None
    }

    obrigatorias = {"nome", "empresa", "e-mail"}

    if not obrigatorias.issubset(indices):
        workbook.close()
        print("As colunas Nome, Empresa e E-mail são obrigatórias.")
        return

    contatos = {}
    ignorados = 0

    for linha in linhas:
        email = linha[indices["e-mail"]]
        nome = linha[indices["nome"]]
        empresa = linha[indices["empresa"]]

        email = str(email or "").strip().lower()
        nome = str(nome or "").strip()
        empresa = str(empresa or "").strip() or None

        if not email or "@" not in email:
            ignorados += 1
            continue

        # Evita importar duas vezes o mesmo endereço.
        # Se houver repetição no arquivo, mantém o primeiro registro.
        if email in contatos:
            ignorados += 1
            continue

        contatos[email] = (nome, empresa, email)

    workbook.close()

    if not contatos:
        print("Nenhum contato válido para importar.")
        return

    print(f"Contatos preparados: {len(contatos)}")
    print(f"Linhas ignoradas: {ignorados}")
    print()
    print("Nenhum e-mail será enviado.")

    confirmacao = input(
        "Digite IMPORTAR para gravar os contatos no PostgreSQL: "
    ).strip()

    if confirmacao != "IMPORTAR":
        print("Importação cancelada. Nenhum dado foi alterado.")
        return

    try:
        with psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        ) as conexao:
            with conexao.cursor() as cursor:
                cursor.executemany(
                    """
                    INSERT INTO destinatarios (nome, empresa, email)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (email)
                    DO UPDATE SET
                        nome = EXCLUDED.nome,
                        empresa = EXCLUDED.empresa
                    """,
                    list(contatos.values()),
                )

        print("Importação concluída com sucesso!")
        print(f"Contatos processados: {len(contatos)}")

    except Exception as erro:
        print("Erro ao importar contatos:")
        print(erro)


if __name__ == "__main__":
    importar_revisados()