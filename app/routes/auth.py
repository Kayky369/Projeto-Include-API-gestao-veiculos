from fastapi import APIRouter, HTTPException 
 
from app.auth import criar_token_acesso, verificar_credenciais
from app.schemas import LoginRequest, TokenResponse
 
router = APIRouter(tags=["Autenticação"])

@router.post(
    "/login", 
    response_model=TokenResponse,
    summary="Autenticar e obter um token JWT", 
)
def login(credenciais: LoginRequest): 
    if not verificar_credenciais(credenciais.username, credenciais.password):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos.") 

    token = criar_token_acesso(credenciais.username)
    return TokenResponse(access_token=token) 





