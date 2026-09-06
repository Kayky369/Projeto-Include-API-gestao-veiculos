from pydantic import BaseModel, Field


class VeiculoCreate(BaseModel):
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