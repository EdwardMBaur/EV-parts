from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class TipoPerfil(str, enum.Enum):
    comprador = "comprador"
    oficina = "oficina"
    fornecedor = "fornecedor"
    admin = "admin"


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    tipo_perfil = Column(String(20), nullable=False, default=TipoPerfil.comprador)
    email = Column(String(150), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    nome_razao_social = Column(String(60), nullable=False)
    cpf_cnpj = Column(String(14), unique=True, nullable=False, index=True)
    telefone = Column(String(11), nullable=True)
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now())
    ativo = Column(String(1), default="S")

    # Relationships
    enderecos = relationship("Endereco", back_populates="usuario", cascade="all, delete-orphan")
    pecas_fornecidas = relationship("Peca", back_populates="fornecedor", foreign_keys="Peca.id_fornecedor")
    pedidos = relationship("Pedido", back_populates="comprador", foreign_keys="Pedido.id_comprador")
