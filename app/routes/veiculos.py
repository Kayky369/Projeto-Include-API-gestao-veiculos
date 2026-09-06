from fastapi import APIRouter, HTTPException
import psycopg
from psycopg.rows import dict_row

from app.database import get_connection
from app.schemas import VeiculoCreate, VeiculoResponse

router = APIRouter()


@router.post("/veiculos", response_model=VeiculoResponse, status_code=201)
def criar_veiculo(veiculo: VeiculoCreate):
    conn = get_connection()
    try:
        cursor = conn.cursor(row_factory=dict_row)
        try:
            # Verifica se já existe um veículo com a mesma placa
            cursor.execute(
                "SELECT id FROM veiculos WHERE placa = %s",
                (veiculo.placa,),
            )
            if cursor.fetchone() is not None:
                raise HTTPException(
                    status_code=400,
                    detail="Já existe um veículo cadastrado com essa placa.",
                )

            # Insere o veículo; o banco define status = 'DISPONIVEL' automaticamente
            cursor.execute(
                """
                INSERT INTO veiculos (marca, modelo, ano, placa, valor_diaria)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, marca, modelo, ano, placa, valor_diaria, status
                """,
                (
                    veiculo.marca,
                    veiculo.modelo,
                    veiculo.ano,
                    veiculo.placa,
                    veiculo.valor_diaria,
                ),
            )
            novo_veiculo = cursor.fetchone()
            conn.commit()
        except psycopg.errors.UniqueViolation:
            # Proteção extra contra condição de corrida na verificação de placa duplicada
            conn.rollback()
            raise HTTPException(
                status_code=400,
                detail="Já existe um veículo cadastrado com essa placa.",
            )
        finally:
            cursor.close()
    finally:
        conn.close()

    return novo_veiculo


@router.get("/veiculos", response_model=list[VeiculoResponse])
def listar_veiculos():
    conn = get_connection()
    try:
        cursor = conn.cursor(row_factory=dict_row)
        try:
            cursor.execute(
                """
                SELECT id, marca, modelo, ano, placa, valor_diaria, status
                FROM veiculos
                ORDER BY id ASC
                """
            )
            veiculos = cursor.fetchall()
        finally:
            cursor.close()
    finally:
        conn.close()

    return veiculos