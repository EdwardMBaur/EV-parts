from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


class ItemPedidoCreate(BaseModel):
    id_peca: int
    quantidade: int = 1


class ItemPedidoResponse(BaseModel):
    id_peca: int
    quantidade: int
    preco_unitario: Decimal
    nome_peca: Optional[str] = None

    model_config = {"from_attributes": True}


class PedidoCreate(BaseModel):
    id_endereco_entrega: int
    itens: List[ItemPedidoCreate]
    modal_frete: Optional[str] = None
    observacoes: Optional[str] = None


class PedidoUpdate(BaseModel):
    status_pedido: Optional[str] = None
    codigo_rastreio: Optional[str] = None
    transportadora: Optional[str] = None
    prazo_entrega: Optional[datetime] = None


class PedidoResponse(BaseModel):
    id_pedido: int
    id_comprador: int
    valor_total: Decimal
    valor_frete: Decimal
    status_pedido: str
    codigo_rastreio: Optional[str] = None
    modal_frete: Optional[str] = None
    transportadora: Optional[str] = None
    prazo_entrega: Optional[datetime] = None
    data_pedido: datetime
    itens: List[ItemPedidoResponse] = []

    model_config = {"from_attributes": True}
