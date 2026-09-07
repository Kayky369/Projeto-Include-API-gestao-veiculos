from datetime import date
from typing import Optional

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


class AluguelCreate(BaseModel):
    cliente_id: int
    veiculo_id: int
    data_inicio: date
    data_fim: date


class AluguelResponse(BaseModel):
    id: int
    cliente_id: int
    veiculo_id: int
    data_inicio: date
    data_fim: date
    data_devolucao: Optional[date] = None
    status: str










    