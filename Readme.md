# Include API Veículos
 
API REST para gerenciamento e aluguel de veículos. Projeto desenvolvido em Python como parte de um projeto universitário da UFC Campus Russas CE Feito por Kayky Ruan Alves.

## Tecnologias 

* Python 3.13.7  
* FastAPI 
* Uvicorn
* PostgreSQL
* Psycopg 3 
* PyJWT
* SQL direto, sem ORM

## Estrutura do Projeto 
 
Estrutura do Projeto  

├── app/
│   ├── _init_.py
│   ├── main.py            # Ponto de entrada e inicialização da API
│   ├── database.py        # Gerenciamento de conexão com o PostgreSQL 
│   ├── schemas.py         # Modelos de validação de dados (Pydantic)
│   ├── auth.py            # Regras e utilitários de autenticação JWT 
│   └── routes/            # Endpoints organizados por domínio 
│       ├── _init_.py
│       ├── auth.py        # Rota de login
│       ├── veiculos.py    # Rotas do CRUD de veículos 
│       ├── clientes.py    # Rotas do CRUD de clientes
│       └── aluguels.py    # Rotas de gestão de aluguéis e devolução 
├── database.sql           # Script SQL para criação do banco e tabelas
├── requirements.txt       # Dependências do projeto
├── README.md              # Você esta aqui
└── .gitignore 

## Como rodar
 
É necessário ter o Python, PostgreSQL e um ambiente virtual ("venv") instalados.

Com o PowerShell aberto na pasta do projeto: 

.\venv\Scripts\Activate.ps1 
pip install -r requirements.txt

Se o PowerShell não permitir ativar o ambiente virtual:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass 

Depois disso, configurre as variaveis de ambiente usadas pelo projeto: 

$env:DB_HOST = "localhost" 
$env:DB_PORT = "5432"
$env:DB_NAME = "include_veiculos"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "sua_senha_aqui"

$env:JWT_USERNAME = "admin"
$env:JWT_PASSWORD = "sua_senha_de_login" 
$env:JWT_SECRET_KEY = "sua_chave_secreta_aqui"

As variáveis "DB_NAME", "DB_USER" e "DB_PASSWORD" são necessárias para a conexão com o PostgreSQL. "DB_HOST" e "DB_PORT" podem ser deixadas com os valores padrão.
  
Para o JWT, são necessárias as três variáveis "JWT_USERNAME", "JWT_PASSWORD" e "JWT_SECRET_KEY".

Essas variáveis ficam disponíveis somente na sessão atual do PowerShell.
 
## Banco de dados 

O projeto usa PostgreSQL e o script "database.sql" já contém a criação das tabelas "veiculos", "clientes" e "aluguels".

Primeiro, crie o banco:  

psql -U postgres -c "CREATE DATABASE include_veiculos;"
 
Depois execute o script:

psql -U postgres -d include_veiculos -f database.sql 

Também da para executar o "database.sql" pelo pgAdmin.

Não existe uma tabela de usuarios. O login é feito usando "JWT_USERNAME" e 'JWT_PASSWORD". 

## Executando

Com o ambiente virtual ativado:

uvicorn app.main:app --reload
 
Ou diretamente pelo ambiente virtual:

.\venv\Scripts\uvicorn.exe app.main:app --reload

A API fica disponível em:

http://127.0.0.1:8000

A documentação do Swagger pode ser acessada em: 

http://127.0.0.1:8000/docs

## Autenticação

O endpoint de login é publico:
 
POST /login

Exemplo:

{
  "username": "admin",
  "password": "sua_senha_de_login"
}
 
A resposta retorna um token JWT:

{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}

No Swagger, basta clicar em "Authorize" e informar o token retornado no login.
 
O token expira em 2 horas.

## Endpoints

### Login

POST /login

Faz o login e retorna o token JWT. 

### Veículos

POST   /veiculos
GET    /veiculos
GET    /veiculos/{id}
GET    /veiculos/placa/{placa}
PUT    /veiculos/{id}
DELETE /veiculos/{id} 

O "POST", "PUT" e "DELETE" precisam de autenticcação.

Um veiculo não pode ser excluido caso exista historico de aluguel.

### Clientes

POST /clientes
GET  /clientes  
GET  /clientes/{id}

O cadastro de cliente precisa de autenticação. As consultas são publicas.

### Aluguéis

POST /aluguels 
GET  /aluguels
GET  /aluguels/{id}
POST /aluguels/{id}/devolucao
 
Para criar um aluguel, o veiculo precisa estar disponivel.

O valor total é calculado pela quantidade de dias do aluguel multiplicada pelo valor da diaria.
 
A devolução encerra o aluguel e deixa o veículo disponível novamente. 

O cadastro e a devolução precisam de autenticação. As consultas são publicas.
 
## Exemplo
 
Depois de fazer login, é possivel cadastrar um veículo:

{
  "marca": "Fiat",
  "modelo": "Argo",
  "ano": 2022,
  "placa": "ABC1234",
  "valor_diaria": 120.50
}
 
E um cliente:

{
  "nome": "Maria Silva",
  "cpf": "12345678900",
  "email": "maria@email.com"
}
 
Com os IDs retornados pela API, pode ser criado um aluguel:

{
  "cliente_id": 1, 
  "veiculo_id": 1,
  "data_inicio": "2026-09-10",
  "data_fim": "2026-09-15"
} 

A API retorna o "valor_total" juunto com os dados do aluguel.
 
Para finalizar:
 
POST /aluguels/1/devolucao

## Observações

As informações de acesso ao banco e a chave do JWT não devem ser colocadas diretamente no código nem enviadas para o Git.

O ".gitignore" já inclui "venv/", "__pycache__/" e ".env".

A autenticação usa apenas um usuário definido pelas variáveis de ambiente. Não existe cadastro de usuários, roles ou recuperação de senha.

O projeto usa SQL diretamente com Psycopg, sem SQLAlchemy ou outro ORM.
 



 