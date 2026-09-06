from fastapi import FastAPI

from app.routes import veiculos

app = FastAPI()

app.include_router(veiculos.router)


@app.get("/")
def read_root():
    return {"message": "Include API está funcionando!"}