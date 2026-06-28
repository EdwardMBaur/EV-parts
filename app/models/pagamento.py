from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class MetodoPagamento:
    CARTAO_CREDITO = "cartao_credito"
    PIX = "pix"
    BOLETO_B2B = "boleto_b2b"


class StatusPagamento:
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    RECUSADO = "recusado"
    ESTORNADO = "estornado"


class Pagamento(Base):
    __tablename__ = "pagamentos"

    id_pagamento = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey("pedidos.id_pedido", ondelete="CASCADE"), nullable=False, unique=True)
    metodo_pagamento = Column(String(30), nullable=False)
    status_pagamento = Column(String(30), nullable=False, default=StatusPagamento.PENDENTE)
    valor = Column(Numeric(10, 2), nullable=False)
    gateway_transaction_id = Column(String(100), nullable=True) 
    gateway_response = Column(String(500), nullable=True)
    data_pagamento = Column(DateTime(timezone=True), nullable=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    pedido = relationship("Pedido", back_populates="pagamento")
