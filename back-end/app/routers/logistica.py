from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.peca import Peca
from app.schemas.logistica import FreteRequest, FreteResponse
from app.services.frete_service import calcular_frete
from app.services.cep_service import buscar_cep

router = APIRouter(prefix="/logistica", tags=["Logística"])


@router.post("/frete", response_model=FreteResponse)
async def calcular_frete_endpoint(payload: FreteRequest):
    """
    RF05 — Intelligent freight calculator for heavy/hazardous EV components.
    Returns available shipping modalities with prices and delivery times.
    """
    # Validate both CEPs
    origem = await buscar_cep(payload.cep_origem)
    if not origem:
        raise HTTPException(status_code=400, detail=f"CEP de origem '{payload.cep_origem}' inválido")
    destino = await buscar_cep(payload.cep_destino)
    if not destino:
        raise HTTPException(status_code=400, detail=f"CEP de destino '{payload.cep_destino}' inválido")

    return calcular_frete(
        cep_origem=payload.cep_origem,
        cep_destino=payload.cep_destino,
        peso_kg=payload.peso_kg,
        voltagem=payload.voltagem,
        valor_declarado=payload.valor_declarado,
    )


@router.get("/frete/peca/{id_peca}")
async def frete_por_peca(
    id_peca: int,
    cep_destino: str,
    db: Session = Depends(get_db),
):
    """
    Calculates freight for a specific part to a destination ZIP code.
    Reads weight and voltage directly from the part record.
    """
    peca = db.query(Peca).filter(Peca.id_peca == id_peca, Peca.ativo == "S").first()
    if not peca:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    if not peca.cep_localizacao:
        raise HTTPException(status_code=400, detail="CEP de origem da peça não informado")

    destino = await buscar_cep(cep_destino)
    if not destino:
        raise HTTPException(status_code=400, detail="CEP de destino inválido")

    return calcular_frete(
        cep_origem=peca.cep_localizacao,
        cep_destino=cep_destino,
        peso_kg=peca.peso_kg or 1,
        voltagem=peca.voltagem,
        valor_declarado=peca.preco,
    )
