from fastapi import FastAPI
from app.routes import auth, veiculos, clientes, aluguels

 #Aqui se começa o projeto inteiro.
 
app = FastAPI(
    title="Include API Veículos",
    description="API REST para gestão e aluguel de veículos - projeto universitário.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(veiculos.router)
app.include_router(clientes.router)
app.include_router(aluguels.router)


@app.get("/")
def read_root():
    return {"message": "Include API está funcionando!"}







