import os
from datetime import datetime, timedelta, timezone 

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer 

# Algoritmo simétrico simples (uma unica chave secreta)
ALGORITMO = "HS256"
 
# O token demora 2 horas pra expirar.
EXPIRACAO_TOKEN_MINUTOS = 120

# auto_error=False para que a ausencia de token seja tratada manualmente 
# abaixo e sempre retorne 401 (o padrão do FastAPI para HTTPBearer é 403).
_security = HTTPBearer(auto_error=False)


def _obter_chave_secreta() -> str:
    chave = os.environ.get("JWT_SECRET_KEY")
    if not chave:
        raise RuntimeError(
            "Variável de ambiente obrigatória não configurada: JWT_SECRET_KEY" 
        )
    return chave

 
def verificar_credenciais(username: str, password: str) -> bool:
    """
    Verifica usuário e senha diretamente contra as variaveis de ambiente
    JWT_USERNAME e JWT_PASSWORD (sem tabela de usuários no banco).
    """
    usuario_esperado = os.environ.get("JWT_USERNAME")
    senha_esperada = os.environ.get("JWT_PASSWORD")

    if not usuario_esperado or not senha_esperada: 
        raise RuntimeError(
            "Variáveis de ambiente obrigatórias não configuradas: "
            "JWT_USERNAME, JWT_PASSWORD"
        )
 
    return username == usuario_esperado and password == senha_esperada


def criar_token_acesso(username: str) -> str:
    """
    Cria um JWT identificando o usuario autenticado (claim "sub"),
    com expiração definida em EXPIRACAO_TOKEN_MINUTOS. 
    """
    expira_em = datetime.now(timezone.utc) + timedelta(minutes=EXPIRACAO_TOKEN_MINUTOS)
    payload = {
        "sub": username,
        "exp": expira_em,
    }
    return jwt.encode(payload, _obter_chave_secreta(), algorithm=ALGORITMO)
 

def obter_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(_security),
) -> str:
    """
    Dependancia do FastAPI usada para proteger endpoints.
    Valida o token JWT enviado no header "Authorization: Bearer <token>".
    Levanta 401 se o token estiver ausente, inválido ou expirado.
    """
    if credenciais is None: 
        raise HTTPException(status_code=401, detail="Token não fornecido.")

    token = credenciais.credentials

    try: 
        payload = jwt.decode(token, _obter_chave_secreta(), algorithms=[ALGORITMO])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido.")

    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Token inválido.") 

    return username







