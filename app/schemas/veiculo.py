from pydantic import BaseModel
from typing import Optional


class VeiculoBase(BaseModel):
    montadora: str
    modelo: str
    ano_fabricacao: int
    versao_software: Optional[str] = None
    vin_prefixo: Optional[str] = None


class VeiculoCreate(VeiculoBase):
    pass


class VeiculoResponse(VeiculoBase):
    id_veiculo: int

    model_config = {"from_attributes": True}
