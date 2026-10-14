from pathlib import Path
from html import escape
import webbrowser

from jinja2 import Environment, FileSystemLoader, select_autoescape


# Localiza a pasta principal do projeto
PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_TEMPLATES = PASTA_PROJETO / "templates"

# Configura o carregamento seguro do modelo HTML
ambiente = Environment(
    loader=FileSystemLoader(str(PASTA_TEMPLATES)),
    autoescape=select_autoescape(["html", "xml"]),
)

# Carrega o modelo
modelo = ambiente.get_template("email.html")

# Dados fictícios para o teste
dados = {
    "assunto": "Apresentação dos nossos serviços",
    "nome": "Maria Silva",
    "mensagem": (
        "Gostaríamos de apresentar nossos serviços "
        "e conhecer melhor as necessidades da sua empresa."
        "Se houver interesse, podemos agendar uma conversa."
    ),
    "assinatura": "Equipe Comercial",
}

# Prepara o HTML sem enviar e-mail
html = modelo.render(
    assunto=dados["assunto"],
    nome=dados["nome"],
    mensagem=dados["mensagem"],
    assinatura=dados["assinatura"],
)

# Salva a prévia na pasta principal do projeto
arquivo_saida = PASTA_PROJETO / "previa_email.html"
arquivo_saida.write_text(html, encoding="utf-8")

print("Prévia criada com sucesso!")
print(f"Arquivo: {arquivo_saida}")

# Abre o arquivo no navegador padrão
webbrowser.open(arquivo_saida.resolve().as_uri())