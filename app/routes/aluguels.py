from fastapi import APIRouter, Depends, HTTPException
import psycopg
from psycopg.rows import dict_row

from app.auth import obter_usuario_atual 
from app.database import get_connection
from app.schemas import AluguelCreate, AluguelResponse

router = APIRouter(tags=["Aluguéis"])
 

@router.post(
    "/aluguels",
    response_model=AluguelResponse, 
    status_code=201,
    summary="Criar um novo aluguel",
)
def criar_aluguel(aluguel: AluguelCreate, usuario_atual: str = Depends(obter_usuario_atual)):
    conn = get_connection()
    try:
        cursor = conn.cursor(row_factory=dict_row)
        try:
            # Verifica se o cliente existe
            cursor.execute(
                "SELECT id FROM clientes WHERE id = %s", 
                (aluguel.cliente_id,),
            )
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Cliente não encontrado.")

            # Verifica se o veiculo existe e trava a linha "FOR UPDATE" para evitar que dois alugueis
            # ativos sejam criados ao mesmo tempo para o mesmo veiculo em requisições concorrentes.
            cursor.execute(
                "SELECT status, valor_diaria FROM veiculos WHERE id = %s FOR UPDATE",
                (aluguel.veiculo_id,),
            ) 
            veiculo = cursor.fetchone()
            if veiculo is None:
                raise HTTPException(status_code=404, detail="Veículo não encontrado.")

            if veiculo["status"] != "DISPONIVEL":
                raise HTTPException(
                    status_code=400,
                    detail="Veículo não está disponível para aluguel.",
                )

            if aluguel.data_fim < aluguel.data_inicio: 
                raise HTTPException(
                    status_code=400,
                    detail="A data de fim não pode ser anterior à data de início.",
                )

            # Cria o aluguel com status "ATIVO" e "data_devolucao" nula
            cursor.execute(
                """
                INSERT INTO aluguels (cliente_id, veiculo_id, data_inicio, data_fim) 
                VALUES (%s, %s, %s, %s)
                RETURNING id, cliente_id, veiculo_id, data_inicio, data_fim, data_devolucao, status
                """, 
                (
                    aluguel.cliente_id,
                    aluguel.veiculo_id,
                    aluguel.data_inicio,
                    aluguel.data_fim,
                ),
            ) 
            novo_aluguel = cursor.fetchone()

            # Marca o veiculo como "ALUGADO", na mesma transação do "INSERT" acima.
            cursor.execute(
                "UPDATE veiculos SET status = 'ALUGADO' WHERE id = %s",
                (aluguel.veiculo_id,), 
            )

            # Calcula o valor total (dias x valor_diaria) usando decimal evitando imprecisões de ponto flutuante nesses valores
            dias = (aluguel.data_fim - aluguel.data_inicio).days
            novo_aluguel["valor_total"] = veiculo["valor_diaria"] * dias 

            conn.commit()
        except psycopg.errors.CheckViolation:
            conn.rollback()
            raise HTTPException(
                status_code=400, 
                detail="Dados inválidos: verifique as datas informadas.",
            )
        finally:
            cursor.close()
    finally:
        conn.close()

    return novo_aluguel
  

@router.get(
    "/aluguels",
    response_model=list[AluguelResponse],
    summary="Listar todos os aluguéis",
)
def listar_aluguels():
    conn = get_connection()
    try: 
        cursor = conn.cursor(row_factory=dict_row)
        try:
            cursor.execute(
                """
                SELECT 
                    a.id, a.cliente_id, a.veiculo_id, a.data_inicio, a.data_fim,
                    a.data_devolucao, a.status,
                    (a.data_fim - a.data_inicio) * v.valor_diaria AS valor_total
                FROM aluguels a
                JOIN veiculos v ON v.id = a.veiculo_id
                ORDER BY a.id ASC 
                """
            )
            aluguels = cursor.fetchall()
        finally:
            cursor.close()
    finally:
        conn.close()

    return aluguels 


@router.get(
    "/aluguels/{id}", 
    response_model=AluguelResponse,
    summary="Buscar aluguel por ID",
)
def buscar_aluguel_por_id(id: int):
    conn = get_connection() 
    try:
        cursor = conn.cursor(row_factory=dict_row)
        try:
            cursor.execute(
                """
                SELECT
                    a.id, a.cliente_id, a.veiculo_id, a.data_inicio, a.data_fim,
                    a.data_devolucao, a.status,
                    (a.data_fim - a.data_inicio) * v.valor_diaria AS valor_total 
                FROM aluguels a
                JOIN veiculos v ON v.id = a.veiculo_id 
                WHERE a.id = %s
                """,
                (id,),
            )
            aluguel = cursor.fetchone()
        finally:
            cursor.close() 
    finally:
        conn.close()

    if aluguel is None:
        raise HTTPException(status_code=404, detail="Aluguel não encontrado.")
 
    return aluguel


@router.post(
    "/aluguels/{id}/devolucao",
    response_model=AluguelResponse,
    status_code=200, 
    summary="Registrar a devolução de um aluguel",
)
def registrar_devolucao(id: int, usuario_atual: str = Depends(obter_usuario_atual)):
    conn = get_connection()
    try:
        cursor = conn.cursor(row_factory=dict_row)
        try:
            # Busca o aluguel e trava a linha "FOR UPDATE" para evitar
            # que a mesma devolução seja feita  duas vezes na mesma tempo  
            cursor.execute(
                "SELECT id, veiculo_id, status FROM aluguels WHERE id = %s FOR UPDATE",
                (id,),
            )
            aluguel = cursor.fetchone()
            if aluguel is None:
                raise HTTPException(status_code=404, detail="Aluguel não encontrado.")

            if aluguel["status"] != "ATIVO": 
                raise HTTPException(
                    status_code=400,
                    detail="Este aluguel já está encerrado.",
                )

            # Encerra o aluguel e registra a data de devolução com a data atual do servidor
            cursor.execute(
                """
                UPDATE aluguels
                SET status = 'ENCERRADO', data_devolucao = CURRENT_DATE
                WHERE id = %s 
                RETURNING id, cliente_id, veiculo_id, data_inicio, data_fim, data_devolucao, status
                """,
                (id,),
            )
            aluguel_atualizado = cursor.fetchone() 
 
            # Libera o veiculo para novos alugueis
            cursor.execute(
                "UPDATE veiculos SET status = 'DISPONIVEL' WHERE id = %s",
                (aluguel["veiculo_id"],),
            )

            conn.commit() 
        finally:
            cursor.close()
    finally:
        conn.close() 

    return aluguel_atualizado









