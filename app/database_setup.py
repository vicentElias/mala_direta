import psycopg

from app.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


SQL_CRIACAO_TABELAS = """

CREATE TABLE IF NOT EXISTS destinatarios (
    id BIGSERIAL PRIMARY KEY,

    nome VARCHAR(150),

    empresa VARCHAR(200),

    email VARCHAR(255) NOT NULL,

    ativo BOOLEAN NOT NULL DEFAULT TRUE,

    data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uk_destinatarios_email
        UNIQUE (email)
);


CREATE TABLE IF NOT EXISTS campanhas (
    id BIGSERIAL PRIMARY KEY,

    nome VARCHAR(200) NOT NULL,

    assunto VARCHAR(300) NOT NULL,

    modelo_html TEXT,

    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    ativa BOOLEAN NOT NULL DEFAULT TRUE
);


CREATE TABLE IF NOT EXISTS envios (
    id BIGSERIAL PRIMARY KEY,

    campanha_id BIGINT NOT NULL,

    destinatario_id BIGINT NOT NULL,

    data_envio TIMESTAMP,

    status VARCHAR(30) NOT NULL DEFAULT 'PENDENTE',

    erro TEXT,

    message_id VARCHAR(500),

    CONSTRAINT fk_envios_campanha
        FOREIGN KEY (campanha_id)
        REFERENCES campanhas(id),

    CONSTRAINT fk_envios_destinatario
        FOREIGN KEY (destinatario_id)
        REFERENCES destinatarios(id),

    CONSTRAINT uk_envio_campanha_destinatario
        UNIQUE (campanha_id, destinatario_id)
);


CREATE INDEX IF NOT EXISTS idx_envios_status
    ON envios(status);


CREATE INDEX IF NOT EXISTS idx_envios_data_envio
    ON envios(data_envio);


CREATE INDEX IF NOT EXISTS idx_destinatarios_email
    ON destinatarios(email);


ALTER TABLE destinatarios
ADD COLUMN IF NOT EXISTS nome VARCHAR(150);

"""


def criar_tabelas():

    try:

        with psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        ) as conexao:

            with conexao.cursor() as cursor:

                cursor.execute(SQL_CRIACAO_TABELAS)

            conexao.commit()

        print("Tabelas verificadas/criadas com sucesso!")

    except Exception as erro:

        print("Erro ao criar/verificar as tabelas:")
        print(erro)


if __name__ == "__main__":
    criar_tabelas()