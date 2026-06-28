from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from app.models.compatibilidade import MatrizCompatibilidade
from app.models.veiculo import Veiculo
from app.models.peca import Peca


def verificar_compatibilidade(
    db: Session,
    id_peca: int,
    id_veiculo: Optional[int] = None,
    montadora: Optional[str] = None,
    modelo: Optional[str] = None,
    ano: Optional[int] = None,
) -> dict:
    """
    Checks whether a part is compatible with a given vehicle.
    Vehicle can be identified by id_veiculo or by montadora+modelo+ano.
    """
    if id_veiculo:
        veiculo = db.query(Veiculo).filter(Veiculo.id_veiculo == id_veiculo).first()
    elif montadora and modelo and ano:
        veiculo = db.query(Veiculo).filter(
            and_(
                Veiculo.montadora.ilike(montadora),
                Veiculo.modelo.ilike(modelo),
                Veiculo.ano_fabricacao == ano,
            )
        ).first()
    else:
        return {"compativel": False, "motivo": "Veículo não identificado"}

    if not veiculo:
        return {"compativel": False, "motivo": "Veículo não encontrado na base"}

    compat = db.query(MatrizCompatibilidade).filter(
        MatrizCompatibilidade.id_peca == id_peca,
        MatrizCompatibilidade.id_veiculo == veiculo.id_veiculo,
    ).first()

    if compat:
        return {
            "compativel": True,
            "veiculo": f"{veiculo.montadora} {veiculo.modelo} {veiculo.ano_fabricacao}",
            "versao_sw_min": compat.versao_sw_min,
            "versao_sw_max": compat.versao_sw_max,
            "observacao": compat.observacao,
        }

    return {
        "compativel": False,
        "veiculo": f"{veiculo.montadora} {veiculo.modelo} {veiculo.ano_fabricacao}",
        "motivo": "Peça não listada como compatível com este veículo",
    }


def buscar_pecas_por_veiculo(
    db: Session,
    montadora: str,
    modelo: str,
    ano: int,
) -> List[int]:
    """Returns list of peca IDs compatible with a given vehicle."""
    veiculo = db.query(Veiculo).filter(
        and_(
            Veiculo.montadora.ilike(f"%{montadora}%"),
            Veiculo.modelo.ilike(f"%{modelo}%"),
            Veiculo.ano_fabricacao == ano,
        )
    ).first()

    if not veiculo:
        return []

    compats = db.query(MatrizCompatibilidade.id_peca).filter(
        MatrizCompatibilidade.id_veiculo == veiculo.id_veiculo
    ).all()
    return [c.id_peca for c in compats]


def buscar_por_vin(db: Session, vin: str) -> Optional[Veiculo]:
    """
    Finds a vehicle by its VIN prefix (first 11 characters identify model/year/manufacturer).
    """
    if len(vin) < 11:
        return None
    prefixo = vin[:11].upper()
    return db.query(Veiculo).filter(Veiculo.vin_prefixo == prefixo).first()
