from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


class PecaBase(BaseModel):
    id_categoria: Optional[int] = None
    nome_peca: str
    descricao: Optional[str] = None
    preco: Decimal
    estoque: int = 1
    codigo_oem: Optional[str] = None
    fabricante: Optional[str] = None
    peso_kg: Optional[Decimal] = None
    dimensoes: Optional[str] = None
    voltagem: Optional[str] = None
    estado_saude_soh: Optional[int] = None
    url_laudo_tecnico: Optional[str] = None
    url_imagem: Optional[str] = None
    cep_localizacao: Optional[str] = None


class PecaCreate(PecaBase):
    ids_veiculos_compativeis: Optional[List[int]] = []


class PecaUpdate(BaseModel):
    nome_peca: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[Decimal] = None
    estoque: Optional[int] = None
    estado_saude_soh: Optional[int] = None
    url_laudo_tecnico: Optional[str] = None
    url_imagem: Optional[str] = None
    ativo: Optional[str] = None
    ids_veiculos_compativeis: Optional[List[int]] = None


class VeiculoCompativel(BaseModel):
    id_veiculo: int
    montadora: str
    modelo: str
    ano_fabricacao: int
    versao_sw_min: Optional[str] = None
    versao_sw_max: Optional[str] = None

    model_config = {"from_attributes": True}


class PecaResponse(PecaBase):
    id_peca: int
    id_fornecedor: Optional[int] = None
    ativo: str
    data_cadastro: datetime
    veiculos_compativeis: List[VeiculoCompativel] = []
    nome_categoria: Optional[str] = None
    nome_fornecedor: Optional[str] = None

    model_config = {"from_attributes": True}


class PecaSearchResult(BaseModel):
    """Lightweight response for catalog listing"""
    id_peca: int
    nome_peca: str
    preco: Decimal
    codigo_oem: Optional[str] = None
    fabricante: Optional[str] = None
    estado_saude_soh: Optional[int] = None
    url_imagem: Optional[str] = None
    cep_localizacao: Optional[str] = None
    nome_categoria: Optional[str] = None
    estoque: int
    compativel: Optional[bool] = None 

    model_config = {"from_attributes": True}


class CompatibilidadeCheck(BaseModel):
    """Request to verify compatibility of a part with a vehicle"""
    id_peca: int
    id_veiculo: Optional[int] = None
    vin: Optional[str] = None 
    montadora: Optional[str] = None
    modelo: Optional[str] = None
    ano: Optional[int] = None
