from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal


class FreteModalidade(BaseModel):
    nome: str             
    codigo: str          
    prazo_dias: int
    valor: Decimal
    descricao: Optional[str] = None


class FreteRequest(BaseModel):
    cep_origem: str
    cep_destino: str
    peso_kg: Decimal
    dimensoes: Optional[str] = None
    voltagem: Optional[str] = None    
    valor_declarado: Optional[Decimal] = None


class FreteResponse(BaseModel):
    cep_origem: str
    cep_destino: str
    modalidades: List[FreteModalidade]
    aviso_carga_especial: Optional[str] = None  
