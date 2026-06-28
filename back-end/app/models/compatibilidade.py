from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base


class MatrizCompatibilidade(Base):
    """
    Junction table between pecas and veiculos.
    Stores exact compatibility including software version ranges.
    """
    __tablename__ = "matriz_compatibilidade"

    id_peca = Column(Integer, ForeignKey("pecas.id_peca", ondelete="CASCADE"), primary_key=True)
    id_veiculo = Column(Integer, ForeignKey("veiculos.id_veiculo", ondelete="CASCADE"), primary_key=True)
    versao_sw_min = Column(String(20), nullable=True)   # Minimum compatible software version
    versao_sw_max = Column(String(20), nullable=True)   # Maximum compatible software version
    observacao = Column(String(255), nullable=True)

    peca = relationship("Peca", back_populates="compatibilidades")
    veiculo = relationship("Veiculo", back_populates="compatibilidades")
