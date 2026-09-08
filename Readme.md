# Include API Veículos

API REST para gerenciamento e aluguel de veiculos desenvolvida para um projeto universitário Include da UFC campus russas CE.

O projeto cobre o cadastro de clientes e veiculos, além de todo o fluxo de aluguel (criação consulta e devolução). Para a persistência de dados, foi utilizado PostgreSQL com SQL puro (sem uso de ORM).

## Tecnologias

* Python 3.13
* FastAPI
* Uvicorn
* PostgreSQL
* Psycopg 3

## Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina:

* Python 3.13
* PostgreSQL rodando localmente

## Configuração do Projeto

**1. Instalar as dependências**

Com o seu ambiente virtual (venv) criado na raiz do projeto, ative-o e instale os pacotes:

No PowerShell:

.\venv\Scripts\Activate.ps1
pip install -r requirements.txt


*(Caso o PowerShell de erro de permissão ao ativar o venv, rode Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass na sessão atual).*

Ou rode o pip direto sem precisar ativar:

.\venv\Scripts\pip.exe install -r requirements.txt


**2. Variáveis de ambiente**

As credenciais do banco precisam ser passadas via variaveis de ambiente. Defina no terminal antes de rodar o projeto:

$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"
$env:DB_NAME = "include_veiculos"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "sua_senha_aqui"


**3. Criar o banco de dados**

O projeto Inclui o o arquivo database.sql com o script de criação das tabelas (veiculos, clientes e aluguels).

Você pode rodar direto pelo terminal:

psql -U postgres -c "CREATE DATABASE include_veiculos;"
psql -U postgres -d include_veiculos -f database.sql


Ou, se preferir usar o pgAdmin: crie o banco include_veiculos e execute o conteúdo do arquivo database.sql na Query Tool.

## Como Executar

Com as variaveis de ambiente configuradas no terminal, rode:

uvicorn app.main:app --reload


Acesse [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para testar as rotas pela interface interativa do Swagger.

## Endpoints da API

**Veículos**

* POST /veiculos - Cadastra um novo veiculo
* GET /veiculos - Lista todos os veiculos
* GET /veiculos/{id} - Busca veiculo por ID
* GET /veiculos/placa/{placa} - Busca veiculo por placa
* PUT /veiculos/{id} - Atualiza dados do veiculo
* DELETE /veiculos/{id} - Remove um veiculo (bloqueado se houver histórico de aluguel)

**Clientes**

* POST /clientes - Cadastra um cliente
* GET /clientes - Lista todos os clientes
* GET /clientes/{id} - Busca cliente por ID

**Aluguéis**

* POST /aluguels - Abre um novo aluguel (o veiculo precisa estar com status DISPONIVEL)
* GET /aluguels - Lista os aluguéis
* GET /aluguels/{id} - Busca aluguel por ID
* POST /aluguels/{id}/devolucao - Registra a devolução e libera o veiculo novamente

## Fluxo de Teste (Ezemplo)

1. Cadastrar um veiculo (POST /veiculos):

{
"marca": "Fiat",
"modelo": "Argo",
"ano": 2022,
"placa": "ABC1234",
"valor_diaria": 120.50
}

2. Cadastrrar um cliente (POST /clientes):

{
"nome": "Maria Silva",
"cpf": "12345678900",
"email": "maria@email.com"
}

3. Criar o aluguel (POST /aluguels):

{
"cliente_id": 1,
"veiculo_id": 1,
"data_inicio": "2026-09-10",
"data_fim": "2026-09-15"
}

4. Encerrar o aluguel (POST /aluguels/1/devolucao).