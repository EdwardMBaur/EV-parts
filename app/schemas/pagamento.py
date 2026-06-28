from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


class PagamentoCreate(BaseModel):
    id_pedido: int
    metodo_pagamento: str 


class PagamentoResponse(BaseModel):
    id_pagamento: int
    id_pedido: int
    metodo_pagamento: str
    status_pagamento: str
    valor: Decimal
    gateway_transaction_id: Optional[str] = None
    data_pagamento: Optional[datetime] = None
    data_criacao: datetime

    model_config = {"from_attributes": True}


class PagamentoWebhook(BaseModel):
    """Payload from payment gateway webhook"""
    gateway_transaction_id: str
    status: str         
    gateway_response: Optional[str] = None
