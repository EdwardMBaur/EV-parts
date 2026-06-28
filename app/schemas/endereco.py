from pydantic import BaseModel, field_validator
from typing import Optional
import re


class EnderecoBase(BaseModel):
    cep: str
    logradouro: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    estado: str
    principal: str = "N"

    @field_validator("cep")
    @classmethod
    def validate_cep(cls, v: str) -> str:
        digits = re.sub(r"\D", "", v)
        if len(digits) != 8:
            raise ValueError("CEP deve ter 8 dígitos")
        return digits

    @field_validator("estado")
    @classmethod
    def validate_estado(cls, v: str) -> str:
        valid = {
            "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS",
            "MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC",
            "SP","SE","TO"
        }
        if v.upper() not in valid:
            raise ValueError("Estado inválido")
        return v.upper()


class EnderecoCreate(EnderecoBase):
    pass


class EnderecoUpdate(BaseModel):
    numero: Optional[str] = None
    complemento: Optional[str] = None
    principal: Optional[str] = None


class EnderecoResponse(EnderecoBase):
    id_endereco: int
    id_usuario: int

    model_config = {"from_attributes": True}


class CEPResponse(BaseModel):
    """Response from ViaCEP API"""
    cep: str
    logradouro: str
    bairro: str
    cidade: str
    estado: str
    ibge: Optional[str] = None
    ddd: Optional[str] = None
