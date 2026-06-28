from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class StatusPedido:
    AGUARDANDO_PAGAMENTO = "aguardando_pagamento"
    PAGO = "pago"
    EM_SEPARACAO = "em_separacao"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"
    DEVOLVIDO = "devolvido"


class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido = Column(Integer, primary_key=True, index=True)
    id_comprador = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="RESTRICT"), nullable=False)
    id_endereco_entrega = Column(Integer, ForeignKey("enderecos.id_endereco"), nullable=True)

    valor_total = Column(Numeric(10, 2), nullable=False)
    valor_frete = Column(Numeric(10, 2), nullable=False, default=0)
    prazo_entrega = Column(DateTime(timezone=True), nullable=True)
    status_pedido = Column(String(30), nullable=False, default=StatusPedido.AGUARDANDO_PAGAMENTO)
    codigo_rastreio = Column(String(50), nullable=True)
    data_pedido = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())

    modal_frete = Column(String(50), nullable=True) 
    transportadora = Column(String(100), nullable=True)
    observacoes = Column(String(500), nullable=True)

    comprador = relationship("Usuario", back_populates="pedidos", foreign_keys=[id_comprador])
    endereco_entrega = relationship("Endereco", foreign_keys=[id_endereco_entrega])
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")
    pagamento = relationship("Pagamento", back_populates="pedido", uselist=False)
