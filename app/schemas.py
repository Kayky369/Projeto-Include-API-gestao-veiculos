from pydantic import BaseModel, Field


class VeiculoCreate(BaseModel):
    marca: str = Field(..., min_length=1)
    modelo: str = Field(..., min_length=1)
    ano: int
    placa: str = Field(..., min_length=1)
    valor_diaria: float = Field(..., gt=0)


class VeiculoUpdate(BaseModel):
    marca: str = Field(..., min_length=1)
    modelo: str = Field(..., min_length=1)
    ano: int
    placa: str = Field(..., min_length=1)
    valor_diaria: float = Field(..., gt=0)


class VeiculoResponse(BaseModel):
    id: int
    marca: str
    modelo: str
    ano: int
    placa: str
    valor_diaria: float
    status: str


class ClienteCreate(BaseModel):
    nome: str = Field(..., min_length=1)
    cpf: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)


class ClienteResponse(BaseModel):
    id: int
    nome: str
    cpf: str
    email: str





    