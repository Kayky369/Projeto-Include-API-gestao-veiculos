-- =========================================================
-- database.sql
-- Estrutura inicial do banco de dados para a API de
-- Gestão e Aluguel de Veículos
-- Fase 2.1 - Estrutura do banco PostgreSQL
-- =========================================================

-- Tabela de veículos disponíveis para aluguel
CREATE TABLE veiculos (
    id            SERIAL PRIMARY KEY,
    marca         VARCHAR(50)    NOT NULL,
    modelo        VARCHAR(50)    NOT NULL,
    ano           INTEGER        NOT NULL CHECK (ano BETWEEN 1900 AND 2100),
    placa         VARCHAR(10)    NOT NULL UNIQUE,
    valor_diaria  NUMERIC(10,2)  NOT NULL CHECK (valor_diaria > 0),
    status        VARCHAR(20)    NOT NULL DEFAULT 'DISPONIVEL'
                  CHECK (status IN ('DISPONIVEL', 'ALUGADO'))
);

-- Tabela de clientes que podem alugar veículos
CREATE TABLE clientes (
    id     SERIAL PRIMARY KEY,
    nome   VARCHAR(150) NOT NULL,
    cpf    VARCHAR(14)  NOT NULL UNIQUE,
    email  VARCHAR(150) NOT NULL
);

-- Tabela de aluguéis, ligando um cliente a um veículo
-- Um veículo pode aparecer em vários aluguéis ao longo do tempo;
-- a regra "somente um aluguel ATIVO por veículo" será validada pela aplicação
CREATE TABLE aluguels (
    id              SERIAL PRIMARY KEY,
    cliente_id      INTEGER     NOT NULL REFERENCES clientes(id) ON DELETE RESTRICT,
    veiculo_id      INTEGER     NOT NULL REFERENCES veiculos(id) ON DELETE RESTRICT,
    data_inicio     DATE        NOT NULL,
    data_fim        DATE        NOT NULL,
    data_devolucao  DATE,
    status          VARCHAR(20) NOT NULL DEFAULT 'ATIVO'
                    CHECK (status IN ('ATIVO', 'ENCERRADO')),
    CHECK (data_fim >= data_inicio));


    