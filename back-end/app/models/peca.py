from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Peca(Base):
    __tablename__ = "pecas"

    id_peca = Column(Integer, primary_key=True, index=True)
    id_fornecedor = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="SET NULL"), nullable=True)
    id_categoria = Column(Integer, ForeignKey("categorias.id_categoria", ondelete="SET NULL"), nullable=True)

    nome_peca = Column(String(150), nullable=False)
    descricao = Column(String(500), nullable=True)
    preco = Column(Numeric(10, 2), nullable=False)
    estoque = Column(Integer, default=1)
    codigo_oem = Column(String(50), nullable=True, index=True)
    fabricante = Column(String(100), nullable=True)

    # Physical attributes
    peso_kg = Column(Numeric(8, 2), nullable=True)
    dimensoes = Column(String(50), nullable=True)
    voltagem = Column(String(30), nullable=True)

    # Battery-specific
    estado_saude_soh = Column(Integer, nullable=True)  
    url_laudo_tecnico = Column(String(255), nullable=True)

    # Media & Location
    url_imagem = Column(String(255), nullable=True)
    cep_localizacao = Column(String(8), nullable=True)

    # Metadata
    ativo = Column(String(1), default="S")
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    fornecedor = relationship("Usuario", back_populates="pecas_fornecidas", foreign_keys=[id_fornecedor])
    categoria = relationship("Categoria", back_populates="pecas")
    compatibilidades = relationship("MatrizCompatibilidade", back_populates="peca", cascade="all, delete-orphan")
    itens_pedido = relationship("ItemPedido", back_populates="peca")
