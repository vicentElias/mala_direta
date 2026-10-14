
from app.campanhas import listar_campanhas, obter_campanha

campanhas = listar_campanhas()

if not campanhas:
    print("Nenhuma campanha cadastrada.")
else:
    print("Campanhas encontradas:")

    for campanha in campanhas:
        print(f"ID: {campanha[0]} | Nome: {campanha[1]}")

    campanha_id = campanhas[0][0]
    campanha = obter_campanha(campanha_id)

    if campanha:
        print("\nDetalhes da campanha selecionada:")
        print(f"ID: {campanha[0]}")
        print(f"Nome: {campanha[1]}")
        print(f"Assunto: {campanha[2]}")
        print(f"Conteúdo HTML cadastrado: {'Sim' if campanha[3] else 'Não'}")

print("\nTeste concluído. Nenhuma campanha foi alterada.")
