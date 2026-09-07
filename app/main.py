from fastapi import FastAPI

from app.routes import veiculos, clientes, aluguels

app = FastAPI()

app.include_router(veiculos.router)
app.include_router(clientes.router)
app.include_router(aluguels.router)


@app.get("/")
def read_root():
    return {"message": "Include API está funcionando!"}





