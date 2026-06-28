from pydantic import BaseModel
from typing import Optional


class CategoriaBase(BaseModel):
    nome_categoria: str
    descricao: Optional[str] = None
    icone_url: Optional[str] = None


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaResponse(CategoriaBase):
    id_categoria: int
    total_pecas: Optional[int] = 0

    model_config = {"from_attributes": True}
