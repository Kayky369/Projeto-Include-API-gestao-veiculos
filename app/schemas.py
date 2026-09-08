from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_serializer


class VeiculoCreate(BaseModel):
    marca: str = Field(..., min_length=1, max_length=50)
    modelo: str = Field(..., min_length=1, max_length=50)
    ano: int
    placa: str = Field(..., min_length=1, max_length=10)
    valor_diaria: float = Field(..., gt=0)


class VeiculoUpdate(BaseModel):
    marca: str = Field(..., min_length=1, max_length=50)
    modelo: str = Field(..., min_length=1, max_length=50)
    ano: int
    placa: str = Field(..., min_length=1, max_length=10)
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
    nome: str = Field(..., min_length=1, max_length=150)
    cpf: str = Field(..., min_length=1, max_length=14)
    email: str = Field(..., min_length=1, max_length=150)


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
    valor_total: Optional[Decimal] = None

    @field_serializer("valor_total")
    def serializar_valor_total(self, valor: Optional[Decimal]) -> Optional[float]:
        # O cálculo interno usa Decimal (evita erro de arredondamento);
        # aqui convertemos só para exibição, já com o valor final já calculado.
        return float(valor) if valor is not None else None


    






