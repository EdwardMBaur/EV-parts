from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nome_categoria = Column(String(50), unique=True, nullable=False)
    descricao = Column(String(255), nullable=True)
    icone_url = Column(String(255), nullable=True)

    pecas = relationship("Peca", back_populates="categoria")
