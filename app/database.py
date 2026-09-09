import os
import psycopg

def get_connection():
    """
    Abre e retorna uma conexão com o banco de dados PostgreSQL.
    As credenciais e configurações são lidas de variáveis de ambiente:
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD.
    Levanta um erro claro caso alguma variavel obrigatória não esteja definida.
    """ 
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")
    dbname = os.environ.get("DB_NAME")
    user = os.environ.get("DB_USER") 
    password = os.environ.get("DB_PASSWORD")

    obrigatorias = {
        "DB_NAME": dbname,
        "DB_USER": user, 
        "DB_PASSWORD": password,
    }

    faltando = [nome for nome, valor in obrigatorias.items() if not valor]

    if faltando: 
        raise RuntimeError(
            "Variáveis de ambiente obrigatórias não configuradas: "
            + ", ".join(faltando)
        ) 

    return psycopg.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user, 
        password=password,
    )











