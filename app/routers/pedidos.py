from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from decimal import Decimal
from datetime import datetime, timedelta, timezone

from app.database import get_db
from app.models.pedido import Pedido, StatusPedido
from app.models.item_pedido import ItemPedido
from app.models.peca import Peca
from app.models.endereco import Endereco
from app.models.usuario import Usuario
from app.schemas.pedido import PedidoCreate, PedidoResponse, PedidoUpdate
from app.core.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/", response_model=PedidoResponse, status_code=201)
def criar_pedido(
    payload: PedidoCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """RF05 — Create an order from cart items."""
    endereco = db.query(Endereco).filter(
        Endereco.id_endereco == payload.id_endereco_entrega,
        Endereco.id_usuario == current_user.id_usuario,
    ).first()
    if not endereco:
        raise HTTPException(status_code=400, detail="Endereço de entrega inválido")

    if not payload.itens:
        raise HTTPException(status_code=400, detail="Pedido deve conter ao menos um item")

    valor_total = Decimal("0")
    itens_para_criar = []

    for item in payload.itens:
        peca = db.query(Peca).filter(Peca.id_peca == item.id_peca, Peca.ativo == "S").first()
        if not peca:
            raise HTTPException(status_code=404, detail=f"Peça {item.id_peca} não encontrada")
        if peca.estoque < item.quantidade:
            raise HTTPException(
                status_code=400,
                detail=f"Estoque insuficiente para '{peca.nome_peca}' (disponível: {peca.estoque})",
            )
        valor_total += peca.preco * item.quantidade
        itens_para_criar.append((peca, item.quantidade))

    pedido = Pedido(
        id_comprador=current_user.id_usuario,
        id_endereco_entrega=payload.id_endereco_entrega,
        valor_total=valor_total,
        valor_frete=Decimal("0"),
        status_pedido=StatusPedido.AGUARDANDO_PAGAMENTO,
        modal_frete=payload.modal_frete,
        observacoes=payload.observacoes,
        prazo_entrega=datetime.now(timezone.utc) + timedelta(days=10),
    )
    db.add(pedido)
    db.flush()

    for peca, quantidade in itens_para_criar:
        db.add(ItemPedido(
            id_pedido=pedido.id_pedido,
            id_peca=peca.id_peca,
            quantidade=quantidade,
            preco_unitario=peca.preco,
        ))
        peca.estoque -= quantidade

    db.commit()
    db.refresh(pedido)

    pedido = db.query(Pedido).options(joinedload(Pedido.itens).joinedload(ItemPedido.peca)).filter(
        Pedido.id_pedido == pedido.id_pedido
    ).first()
    return _to_response(pedido)


@router.get("/", response_model=List[PedidoResponse])
def listar_pedidos(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all orders for the current user."""
    pedidos = db.query(Pedido).options(
        joinedload(Pedido.itens).joinedload(ItemPedido.peca)
    ).filter(Pedido.id_comprador == current_user.id_usuario).order_by(Pedido.data_pedido.desc()).all()
    return [_to_response(p) for p in pedidos]


@router.get("/{id_pedido}", response_model=PedidoResponse)
def detalhe_pedido(
    id_pedido: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pedido = db.query(Pedido).options(
        joinedload(Pedido.itens).joinedload(ItemPedido.peca)
    ).filter(Pedido.id_pedido == id_pedido, Pedido.id_comprador == current_user.id_usuario).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return _to_response(pedido)


@router.put("/{id_pedido}", response_model=PedidoResponse)
def atualizar_pedido(
    id_pedido: int,
    payload: PedidoUpdate,
    current_user: Usuario = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Admin-only: update order status and tracking info."""
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(pedido, field, value)
    db.commit()
    db.refresh(pedido)
    pedido = db.query(Pedido).options(joinedload(Pedido.itens).joinedload(ItemPedido.peca)).filter(
        Pedido.id_pedido == id_pedido
    ).first()
    return _to_response(pedido)


def _to_response(pedido: Pedido) -> PedidoResponse:
    from app.schemas.pedido import ItemPedidoResponse
    itens = [
        ItemPedidoResponse(
            id_peca=i.id_peca,
            quantidade=i.quantidade,
            preco_unitario=i.preco_unitario,
            nome_peca=i.peca.nome_peca if i.peca else None,
        )
        for i in pedido.itens
    ]
    return PedidoResponse(
        id_pedido=pedido.id_pedido,
        id_comprador=pedido.id_comprador,
        valor_total=pedido.valor_total,
        valor_frete=pedido.valor_frete,
        status_pedido=pedido.status_pedido,
        codigo_rastreio=pedido.codigo_rastreio,
        modal_frete=pedido.modal_frete,
        transportadora=pedido.transportadora,
        prazo_entrega=pedido.prazo_entrega,
        data_pedido=pedido.data_pedido,
        itens=itens,
    )
