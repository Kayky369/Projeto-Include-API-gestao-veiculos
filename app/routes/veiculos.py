from fastapi import APIRouter, HTTPException
import psycopg
from psycopg.rows import dict_row

from app.database import get_connection
from app.schemas import VeiculoCreate, VeiculoUpdate, VeiculoResponse

router = APIRouter()


@router.post("/veiculos", response_model=VeiculoResponse, status_code=201)
def criar_veiculo(veiculo: VeiculoCreate):
    conn = get_connection()
    try:
        cursor = conn.cursor(row_factory=dict_row)
        try:
            cursor.execute(
                "SELECT id FROM veiculos WHERE placa = %s",
                (veiculo.placa,),
            )
            if cursor.fetchone() is not None:
                raise HTTPException(
                    status_code=400,
                    detail="Já existe um veículo cadastrado com essa placa.",
                )

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


@router.get("/veiculos/placa/{placa}", response_model=VeiculoResponse)
def buscar_veiculo_por_placa(placa: str):
    conn = get_connection()
    try:
        cursor = conn.cursor(row_factory=dict_row)
        try:
            cursor.execute(
                """
                SELECT id, marca, modelo, ano, placa, valor_diaria, status
                FROM veiculos
                WHERE placa = %s
                """,
                (placa,),
            )
            veiculo = cursor.fetchone()
        finally:
            cursor.close()
    finally:
        conn.close()

    if veiculo is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")

    return veiculo


@router.get("/veiculos/{id}", response_model=VeiculoResponse)
def buscar_veiculo_por_id(id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor(row_factory=dict_row)
        try:
            cursor.execute(
                """
                SELECT id, marca, modelo, ano, placa, valor_diaria, status
                FROM veiculos
                WHERE id = %s
                """,
                (id,),
            )
            veiculo = cursor.fetchone()
        finally:
            cursor.close()
    finally:
        conn.close()

    if veiculo is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado.")

    return veiculo


@router.put("/veiculos/{id}", response_model=VeiculoResponse)
def atualizar_veiculo(id: int, veiculo: VeiculoUpdate):
    conn = get_connection()
    try:
        cursor = conn.cursor(row_factory=dict_row)
        try:
            # Verifica se o veículo existe
            cursor.execute("SELECT id FROM veiculos WHERE id = %s", (id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Veículo não encontrado.")

            # Verifica se a nova placa já pertence a outro veículo
            cursor.execute(
                "SELECT id FROM veiculos WHERE placa = %s AND id != %s",
                (veiculo.placa, id),
            )
            if cursor.fetchone() is not None:
                raise HTTPException(
                    status_code=400,
                    detail="Já existe outro veículo cadastrado com essa placa.",
                )

            cursor.execute(
                """
                UPDATE veiculos
                SET marca = %s, modelo = %s, ano = %s, placa = %s, valor_diaria = %s
                WHERE id = %s
                RETURNING id, marca, modelo, ano, placa, valor_diaria, status
                """,
                (
                    veiculo.marca,
                    veiculo.modelo,
                    veiculo.ano,
                    veiculo.placa,
                    veiculo.valor_diaria,
                    id,
                ),
            )
            veiculo_atualizado = cursor.fetchone()
            conn.commit()
        except psycopg.errors.UniqueViolation:
            # Proteção extra contra condição de corrida na verificação de placa duplicada
            conn.rollback()
            raise HTTPException(
                status_code=400,
                detail="Já existe outro veículo cadastrado com essa placa.",
            )
        except psycopg.errors.CheckViolation:
            # Cobre o caso de "ano" fora do intervalo aceito pelo banco (1900-2100)
            conn.rollback()
            raise HTTPException(
                status_code=400,
                detail="Dados inválidos: verifique o ano informado (deve estar entre 1900 e 2100).",
            )
        finally:
            cursor.close()
    finally:
        conn.close()

    return veiculo_atualizado


@router.delete("/veiculos/{id}", status_code=204)
def excluir_veiculo(id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor(row_factory=dict_row)
        try:
            # Verifica se o veículo existe
            cursor.execute("SELECT id FROM veiculos WHERE id = %s", (id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Veículo não encontrado.")

            # Verifica se existe algum aluguel relacionado a esse veículo
            cursor.execute(
                "SELECT id FROM aluguels WHERE veiculo_id = %s LIMIT 1",
                (id,),
            )
            if cursor.fetchone() is not None:
                raise HTTPException(
                    status_code=400,
                    detail="Não é possível excluir o veículo: existe histórico de aluguel associado.",
                )

            cursor.execute("DELETE FROM veiculos WHERE id = %s", (id,))
            conn.commit()
        except psycopg.errors.ForeignKeyViolation:
            # Proteção extra contra condição de corrida (aluguel criado entre a checagem e o DELETE)
            conn.rollback()
            raise HTTPException(
                status_code=400,
                detail="Não é possível excluir o veículo: existe histórico de aluguel associado.",
            )
        finally:
            cursor.close()
    finally:
        conn.close()

    return None







