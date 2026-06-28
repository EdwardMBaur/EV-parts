from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ItemPedido(Base):
    __tablename__ = "item_pedido"

    id_pedido = Column(Integer, ForeignKey("pedidos.id_pedido", ondelete="CASCADE"), primary_key=True)
    id_peca = Column(Integer, ForeignKey("pecas.id_peca", ondelete="RESTRICT"), primary_key=True)
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario = Column(Numeric(10, 2), nullable=False) 

    pedido = relationship("Pedido", back_populates="itens")
    peca = relationship("Peca", back_populates="itens_pedido")
