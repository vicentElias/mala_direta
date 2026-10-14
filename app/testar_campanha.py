from app.campanhas import cadastrar_campanha, listar_campanhas


def main():
    print("=== TESTE DE CADASTRO DE CAMPANHA ===")

    nome = "Campanha de teste - ambiente de desenvolvimento"
    assunto = "Teste de visualização de e-mail"

    modelo_html = """
    <h2>Olá, {{ nome }}!</h2>
    <p>Esta é uma campanha de teste.</p>
    """

    try:
        campanha = cadastrar_campanha(
            nome=nome,
            assunto=assunto,
            modelo_html=modelo_html,
        )

        print("\nCampanha cadastrada com sucesso!")
        print(f"ID: {campanha[0]}")
        print(f"Nome: {campanha[1]}")
        print(f"Assunto: {campanha[2]}")
        print(f"Data de criação: {campanha[3]}")

        print("\n=== CAMPANHAS REGISTRADAS ===")

        for item in listar_campanhas():
            print(
                f"ID: {item[0]} | "
                f"Nome: {item[1]} | "
                f"Assunto: {item[2]} | "
                f"Ativa: {item[4]}"
            )

    except Exception as erro:
        print("\nNão foi possível concluir o teste.")
        print(f"Detalhes: {erro}")


if __name__ == "__main__":
    main()