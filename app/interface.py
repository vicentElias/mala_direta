import html
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from app.campanhas import (
    cadastrar_campanha,
    listar_campanhas,
    obter_campanha,
    atualizar_campanha,
    alterar_status_campanha,
)


st.set_page_config(
    page_title="Mala Direta",
    page_icon="✉️",
    layout="wide",
)

st.title("✉️ Sistema de Mala Direta")
st.caption("Gerenciamento de campanhas de e-mail")

st.info(
    "Modo seguro de desenvolvimento: esta interface não envia e-mails."
)

opcao = st.sidebar.radio(
    "Menu principal",
    [
        "Início",
        "Cadastrar campanha",
        "Consultar campanhas",
        "Pré-visualizar e-mail",
        "Editar campanha",
    ],
)


def montar_modelo(assunto, mensagem):
    """Cria um modelo HTML reutilizável para a campanha."""

    assunto_seguro = html.escape(assunto)
    mensagem_segura = html.escape(mensagem).replace("\n", "<br>\n")

    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{assunto_seguro}</title>
    </head>
    <body style="margin:0; padding:24px; background:#f4f6f8;
                 font-family:Arial,sans-serif; color:#333;">
        <div style="max-width:600px; margin:auto; padding:28px;
                    background:#ffffff; border-radius:8px;">
            <h2 style="color:#1f4e79;">Olá, {{{{ nome }}}}!</h2>
            <div style="font-size:15px; line-height:1.7;">
                {mensagem_segura}
            </div>
            <p style="font-size:15px; line-height:1.7;">
                Atenciosamente,<br>
                <strong>Equipe Comercial</strong>
            </p>
        </div>
    </body>
    </html>
    """


if opcao == "Início":
    st.subheader("Painel inicial")
    st.write(
        "Utilize o menu à esquerda para cadastrar campanhas, "
        "consultar os registros ou visualizar um e-mail."
    )

    try:
        campanhas = listar_campanhas()
        st.metric("Campanhas cadastradas", len(campanhas))
    except Exception as erro:
        st.error("Não foi possível consultar o banco de dados.")
        st.code(str(erro))


elif opcao == "Cadastrar campanha":
    st.subheader("Cadastrar nova campanha")

    with st.form("form_campanha"):
        nome = st.text_input(
            "Nome da campanha",
            placeholder="Ex.: Apresentação comercial - outubro",
        )

        assunto = st.text_input(
            "Assunto do e-mail",
            placeholder="Ex.: Conheça nossos serviços",
        )

        mensagem = st.text_area(
            "Conteúdo da mensagem",
            height=220,
            placeholder="Digite aqui o conteúdo do e-mail...",
        )

        confirmar = st.form_submit_button("Salvar campanha")

    if confirmar:
        if not nome.strip() or not assunto.strip() or not mensagem.strip():
            st.warning("Preencha o nome, o assunto e o conteúdo da mensagem.")
        else:
            modelo_html = montar_modelo(assunto, mensagem)

            try:
                campanha = cadastrar_campanha(
                    nome=nome,
                    assunto=assunto,
                    modelo_html=modelo_html,
                )

                st.success(
                    f"Campanha cadastrada! Identificador: {campanha[0]}"
                )
                st.info("Nenhum e-mail foi enviado.")

            except Exception as erro:
                st.error("Não foi possível cadastrar a campanha.")
                st.code(str(erro))


elif opcao == "Consultar campanhas":
    st.subheader("Campanhas cadastradas")

    try:
        campanhas = listar_campanhas()

        if not campanhas:
            st.info("Ainda não há campanhas cadastradas.")
        else:
            st.write(f"Total de campanhas: **{len(campanhas)}**")

            for campanha in campanhas:
                campanha_id, nome, assunto, data_criacao, ativo = campanha

                with st.expander(f"Campanha {campanha_id} — {nome}"):
                    st.write(f"**Assunto:** {assunto}")
                    st.write(f"**Data de criação:** {data_criacao}")
                    st.write(f"**Ativa:** {'Sim' if ativo else 'Não'}")

                    if ativo:                    
                        if st.button(
                            "Desativar campanha",
                            key=f"desativar_{campanha_id}",
                        ):
                            try:
                                alterar_status_campanha(campanha_id, False)
                                st.success("Campanha desativada com sucesso!")
                                st.rerun()
                            except Exception as erro:
                                st.error("Não foi possível desativar a campanha.")
                                st.code(str(erro))
                    else:
                        if st.button(
                            "Ativar campanha",
                            key=f"ativar_{campanha_id}",
                        ):
                            try:
                                alterar_status_campanha(campanha_id, True)
                                st.success("Campanha ativada com sucesso!")
                                st.rerun()
                            except Exception as erro:
                                st.error("Não foi possível ativar a campanha.")
                                st.code(str(erro))

    except Exception as erro:
        st.error("Não foi possível consultar as campanhas.")
        st.code(str(erro))


elif opcao == "Pré-visualizar e-mail":
    st.subheader("Pré-visualizar uma campanha")

    try:
        campanhas = listar_campanhas()

        if not campanhas:
            st.info("Cadastre uma campanha antes de visualizar o e-mail.")
        else:
            opcoes = {
                f"ID {c[0]} — {c[1]}": c
                for c in campanhas
            }

            selecionada = st.selectbox(
                "Selecione a campanha",
                list(opcoes.keys()),
            )

            campanha = opcoes[selecionada]

            st.write(f"**Assunto:** {campanha[2]}")

            with st.form("form_preview"):
                nome_teste = st.text_input(
                    "Nome fictício para a prévia",
                    value="Maria Silva",
                )
                visualizar = st.form_submit_button("Gerar prévia")

            if visualizar:
                with st.spinner("Carregando o modelo da campanha..."):
                    from os import environ

                    caminho_postgres = r"C:\Program Files\PostgreSQL\18\bin"
                    if Path(caminho_postgres).is_dir():
                        environ["PATH"] = (
                            caminho_postgres
                            + __import__("os").pathsep
                            + environ.get("PATH", "")
                        )

                    import psycopg
                    from app.config import (
                        DB_HOST,
                        DB_PORT,
                        DB_NAME,
                        DB_USER,
                        DB_PASSWORD,
                    )

                    with psycopg.connect(
                        host=DB_HOST,
                        port=DB_PORT,
                        dbname=DB_NAME,
                        user=DB_USER,
                        password=DB_PASSWORD,
                    ) as conexao:
                        with conexao.cursor() as cursor:
                            cursor.execute(
                                "SELECT modelo_html FROM campanhas WHERE id = %s",
                                (campanha[0],),
                            )
                            resultado = cursor.fetchone()

                if resultado and resultado[0]:
                    modelo = resultado[0]
                    nome_seguro = html.escape(nome_teste)
                    previa = modelo.replace(
                        "{{ nome }}",
                        nome_seguro,
                    )

                    st.markdown("### Resultado da pré-visualização")
                    components.html(previa, height=500, scrolling=True)
                    st.caption(
                        "Esta é apenas uma prévia local. Nenhum e-mail foi enviado."
                    )
                else:
                    st.warning("Esta campanha não possui um modelo HTML salvo.")

    except Exception as erro:
        st.error("Não foi possível gerar a pré-visualização.")
        st.code(str(erro))


elif opcao == "Editar campanha":
    st.subheader("Editar campanha existente")

    campanhas = listar_campanhas()

    if not campanhas:
        st.info("Não há campanhas cadastradas para editar.")
    else:
        opcoes = {
            f"ID {c[0]} - {c[1]}": c[0]
            for c in campanhas
        }

        selecao = st.selectbox(
            "Selecione a campanha que deseja editar:",
            options=list(opcoes.keys()),
            key="selecao_campanha_editar",
        )

        campanha_id = opcoes[selecao]
        campanha = obter_campanha(campanha_id)

        if campanha is None:
            st.error("Não foi possível localizar essa campanha.")
        else:
            with st.form(key=f"form_editar_campanha_{campanha_id}"):
                novo_nome = st.text_input(
                    "Nome da campanha",
                    value=campanha[1] or "",
                )

                novo_assunto = st.text_input(
                    "Assunto do e-mail",
                    value=campanha[2] or "",
                )

                html_atual = campanha[3] or ""

                novo_html = st.text_area(
                    "Conteúdo HTML da campanha",
                    value=html_atual,
                    height=300,
                )

                confirmar = st.form_submit_button(
                    "Salvar alterações"
                )

            if confirmar:
                try:
                    campanha_atualizada = atualizar_campanha(
                        campanha_id,
                        novo_nome,
                        novo_assunto,
                        novo_html,
                    )

                    st.success(
                        f"Campanha ID {campanha_atualizada[0]} "
                        "atualizada com sucesso!"
                    )

                    st.info(
                        "Nenhum e-mail foi enviado."
                    )

                except ValueError as erro:
                    st.error(str(erro))

                except Exception as erro:
                    st.error(
                        f"Não foi possível atualizar a campanha: {erro}"
                    )
