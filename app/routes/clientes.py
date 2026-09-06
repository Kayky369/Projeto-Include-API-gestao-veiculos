from fastapi import APIRouter, HTTPException
import psycopg
from psycopg.rows import dict_row

from app.database import get_connection
from app.schemas import ClienteCreate, ClienteResponse

router = APIRouter()


@router.post("/clientes", response_model=ClienteResponse, status_code=201)
def criar_cliente(cliente: ClienteCreate):
    conn = get_connection()
    try:
        cursor = conn.cursor(row_factory=dict_row)
        try:
            # Verifica se já existe um cliente com o mesmo CPF
            cursor.execute(
                "SELECT id FROM clientes WHERE cpf = %s",
                (cliente.cpf,),
            )
            if cursor.fetchone() is not None:
                raise HTTPException(
                    status_code=400,
                    detail="Já existe um cliente cadastrado com esse CPF.",
                )

            cursor.execute(
                """
                INSERT INTO clientes (nome, cpf, email)
                VALUES (%s, %s, %s)
                RETURNING id, nome, cpf, email
                """,
                (cliente.nome, cliente.cpf, cliente.email),
            )
            novo_cliente = cursor.fetchone()
            conn.commit()
        except psycopg.errors.UniqueViolation:
            # Proteção extra contra condição de corrida na verificação de CPF duplicado
            conn.rollback()
            raise HTTPException(
                status_code=400,
                detail="Já existe um cliente cadastrado com esse CPF.",
            )
        finally:
            cursor.close()
    finally:
        conn.close()

    return novo_cliente


@router.get("/clientes", response_model=list[ClienteResponse])
def listar_clientes():
    conn = get_connection()
    try:
        cursor = conn.cursor(row_factory=dict_row)
        try:
            cursor.execute(
                """
                SELECT id, nome, cpf, email
                FROM clientes
                ORDER BY id ASC
                """
            )
            clientes = cursor.fetchall()
        finally:
            cursor.close()
    finally:
        conn.close()

    return clientes


@router.get("/clientes/{id}", response_model=ClienteResponse)
def buscar_cliente_por_id(id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor(row_factory=dict_row)
        try:
            cursor.execute(
                """
                SELECT id, nome, cpf, email
                FROM clientes
                WHERE id = %s
                """,
                (id,),
            )
            cliente = cursor.fetchone()
        finally:
            cursor.close()
    finally:
        conn.close()

    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    return cliente





