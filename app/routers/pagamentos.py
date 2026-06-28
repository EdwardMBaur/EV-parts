from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database import get_db
from app.models.pagamento import Pagamento, StatusPagamento, MetodoPagamento
from app.models.pedido import Pedido, StatusPedido
from app.models.usuario import Usuario
from app.schemas.pagamento import PagamentoCreate, PagamentoResponse, PagamentoWebhook
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])

METODOS_VALIDOS = {MetodoPagamento.CARTAO_CREDITO, MetodoPagamento.PIX, MetodoPagamento.BOLETO_B2B}


@router.post("/", response_model=PagamentoResponse, status_code=201)
def iniciar_pagamento(
    payload: PagamentoCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """RF05 — Initiates payment for an order. Integrates with payment gateway."""
    if payload.metodo_pagamento not in METODOS_VALIDOS:
        raise HTTPException(status_code=400, detail=f"Método de pagamento inválido. Use: {', '.join(METODOS_VALIDOS)}")

    pedido = db.query(Pedido).filter(
        Pedido.id_pedido == payload.id_pedido,
        Pedido.id_comprador == current_user.id_usuario,
    ).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if pedido.status_pedido != StatusPedido.AGUARDANDO_PAGAMENTO:
        raise HTTPException(status_code=400, detail=f"Pedido já em status '{pedido.status_pedido}'")

    existente = db.query(Pagamento).filter(Pagamento.id_pedido == pedido.id_pedido).first()
    if existente:
        raise HTTPException(status_code=400, detail="Pagamento já iniciado para este pedido")

    pagamento = Pagamento(
        id_pedido=pedido.id_pedido,
        metodo_pagamento=payload.metodo_pagamento,
        status_pagamento=StatusPagamento.PENDENTE,
        valor=pedido.valor_total + pedido.valor_frete,
        gateway_transaction_id=f"SIM-{pedido.id_pedido}-{payload.metodo_pagamento[:3].upper()}",
    )
    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)
    return pagamento


@router.post("/webhook")
def gateway_webhook(payload: PagamentoWebhook, db: Session = Depends(get_db)):
    """
    Webhook endpoint for payment gateway callbacks.
    Updates order and payment status based on gateway notification.
    """
    pagamento = db.query(Pagamento).filter(
        Pagamento.gateway_transaction_id == payload.gateway_transaction_id
    ).first()
    if not pagamento:
        raise HTTPException(status_code=404, detail="Transação não encontrada")

    status_map = {
        "approved": StatusPagamento.APROVADO,
        "refused": StatusPagamento.RECUSADO,
        "refunded": StatusPagamento.ESTORNADO,
    }

    novo_status = status_map.get(payload.status)
    if not novo_status:
        raise HTTPException(status_code=400, detail="Status desconhecido")

    pagamento.status_pagamento = novo_status
    pagamento.gateway_response = payload.gateway_response
    if novo_status == StatusPagamento.APROVADO:
        pagamento.data_pagamento = datetime.now(timezone.utc)
        pedido = db.query(Pedido).filter(Pedido.id_pedido == pagamento.id_pedido).first()
        if pedido:
            pedido.status_pedido = StatusPedido.PAGO

    db.commit()
    return {"detail": "Webhook processado"}


@router.get("/{id_pedido}", response_model=PagamentoResponse)
def get_pagamento(
    id_pedido: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pedido = db.query(Pedido).filter(
        Pedido.id_pedido == id_pedido,
        Pedido.id_comprador == current_user.id_usuario,
    ).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    pagamento = db.query(Pagamento).filter(Pagamento.id_pedido == id_pedido).first()
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return pagamento
