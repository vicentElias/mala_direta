from app.campanhas import listar_campanhas

if __name__ == "__main__":
    campanhas = listar_campanhas()

    print("=== CAMPANHAS CADASTRADAS ===")

    if not campanhas:
        print("Nenhuma campanha encontrada.")
    else:
        for campanha in campanhas:
            print(f"ID: {campanha[0]}")
            print(f"Nome: {campanha[1]}")
            print(f"Assunto: {campanha[2]}")
            print(f"Data de criação: {campanha[3]}")
            print(f"Ativa: {campanha[4]}")
            print("-" * 40)