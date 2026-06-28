from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Veiculo(Base):
    __tablename__ = "veiculos"

    id_veiculo = Column(Integer, primary_key=True, index=True)
    montadora = Column(String(50), nullable=False)
    modelo = Column(String(100), nullable=False)
    ano_fabricacao = Column(Integer, nullable=False)
    versao_software = Column(String(30), nullable=True)
    vin_prefixo = Column(String(11), nullable=True)  

    compatibilidades = relationship("MatrizCompatibilidade", back_populates="veiculo")
