from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
import re


class UsuarioBase(BaseModel):
    tipo_perfil: str
    email: EmailStr
    nome_razao_social: str
    cpf_cnpj: str
    telefone: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    senha: str

    @field_validator("nome_razao_social")
    @classmethod
    def validate_nome(cls, v: str) -> str:
        if len(v) < 2 or len(v) > 60:
            raise ValueError("Nome deve ter entre 2 e 60 caracteres")
        return v

    @field_validator("cpf_cnpj")
    @classmethod
    def validate_cpf_cnpj(cls, v: str) -> str:
        digits = re.sub(r"\D", "", v)
        if len(digits) not in (11, 14):
            raise ValueError("CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos")
        return digits

    @field_validator("telefone")
    @classmethod
    def validate_telefone(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        digits = re.sub(r"\D", "", v)
        if len(digits) not in (10, 11):
            raise ValueError("Telefone deve ter 10 ou 11 dígitos")
        return digits

    @field_validator("senha")
    @classmethod
    def validate_senha(cls, v: str) -> str:
        if len(v) < 8 or len(v) > 20:
            raise ValueError("Senha deve ter entre 8 e 20 caracteres")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Senha deve conter ao menos uma letra maiúscula")
        if not re.search(r"\d", v):
            raise ValueError("Senha deve conter ao menos um número")
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", v):
            raise ValueError("Senha deve conter ao menos um caractere especial")
        return v

    @field_validator("tipo_perfil")
    @classmethod
    def validate_perfil(cls, v: str) -> str:
        allowed = {"comprador", "oficina", "fornecedor"}
        if v not in allowed:
            raise ValueError(f"tipo_perfil deve ser um de: {', '.join(allowed)}")
        return v


class UsuarioUpdate(BaseModel):
    nome_razao_social: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None


class UsuarioResponse(UsuarioBase):
    id_usuario: int
    data_cadastro: datetime
    ativo: str

    model_config = {"from_attributes": True}
