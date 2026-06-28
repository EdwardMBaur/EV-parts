from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from typing import List, Optional
from decimal import Decimal

from app.database import get_db
from app.models.peca import Peca
from app.models.compatibilidade import MatrizCompatibilidade
from app.models.categoria import Categoria
from app.models.usuario import Usuario
from app.schemas.peca import PecaCreate, PecaResponse, PecaUpdate, PecaSearchResult, CompatibilidadeCheck
from app.core.dependencies import get_current_user, require_fornecedor
from app.services.compatibilidade_service import (
    verificar_compatibilidade, buscar_pecas_por_veiculo, buscar_por_vin
)

router = APIRouter(prefix="/pecas", tags=["Peças"])


def _build_response(peca: Peca) -> PecaResponse:
    veiculos = []
    for c in peca.compatibilidades:
        v = c.veiculo
        veiculos.append({
            "id_veiculo": v.id_veiculo,
            "montadora": v.montadora,
            "modelo": v.modelo,
            "ano_fabricacao": v.ano_fabricacao,
            "versao_sw_min": c.versao_sw_min,
            "versao_sw_max": c.versao_sw_max,
        })
    return PecaResponse(
        **{col: getattr(peca, col) for col in [
            "id_peca", "id_fornecedor", "id_categoria", "nome_peca", "descricao",
            "preco", "estoque", "codigo_oem", "fabricante", "peso_kg", "dimensoes",
            "voltagem", "estado_saude_soh", "url_laudo_tecnico", "url_imagem",
            "cep_localizacao", "ativo", "data_cadastro",
        ]},
        veiculos_compativeis=veiculos,
        nome_categoria=peca.categoria.nome_categoria if peca.categoria else None,
        nome_fornecedor=peca.fornecedor.nome_razao_social if peca.fornecedor else None,
    )


@router.get("/", response_model=List[PecaSearchResult])
def listar_pecas(
    # RF04 — Catalog filters
    montadora: Optional[str] = Query(None, description="Filter by vehicle manufacturer"),
    modelo: Optional[str] = Query(None, description="Filter by vehicle model"),
    ano: Optional[int] = Query(None, description="Filter by vehicle year"),
    vin: Optional[str] = Query(None, description="VIN for smart compatibility search"),
    id_categoria: Optional[int] = Query(None),
    codigo_oem: Optional[str] = Query(None),
    preco_min: Optional[Decimal] = Query(None),
    preco_max: Optional[Decimal] = Query(None),
    soh_min: Optional[int] = Query(None, description="Minimum battery SoH %"),
    localizacao_cep: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """RF04 — Smart catalog search with compatibility filtering."""
    query = db.query(Peca).filter(Peca.ativo == "S")

    compatible_ids: Optional[List[int]] = None
    if vin:
        veiculo = buscar_por_vin(db, vin)
        if veiculo:
            compatible_ids = buscar_pecas_por_veiculo(db, veiculo.montadora, veiculo.modelo, veiculo.ano_fabricacao)
    elif montadora and modelo and ano:
        compatible_ids = buscar_pecas_por_veiculo(db, montadora, modelo, ano)

    if compatible_ids is not None:
        query = query.filter(Peca.id_peca.in_(compatible_ids))

    if id_categoria:
        query = query.filter(Peca.id_categoria == id_categoria)
    if codigo_oem:
        query = query.filter(Peca.codigo_oem.ilike(f"%{codigo_oem}%"))
    if preco_min is not None:
        query = query.filter(Peca.preco >= preco_min)
    if preco_max is not None:
        query = query.filter(Peca.preco <= preco_max)
    if soh_min is not None:
        query = query.filter(Peca.estado_saude_soh >= soh_min)
    if localizacao_cep:
        query = query.filter(Peca.cep_localizacao.startswith(localizacao_cep[:5]))

    pecas = query.options(joinedload(Peca.categoria)).offset(skip).limit(limit).all()

    results = []
    for p in pecas:
        results.append(PecaSearchResult(
            id_peca=p.id_peca,
            nome_peca=p.nome_peca,
            preco=p.preco,
            codigo_oem=p.codigo_oem,
            fabricante=p.fabricante,
            estado_saude_soh=p.estado_saude_soh,
            url_imagem=p.url_imagem,
            cep_localizacao=p.cep_localizacao,
            nome_categoria=p.categoria.nome_categoria if p.categoria else None,
            estoque=p.estoque,
            compativel=(compatible_ids is not None),
        ))
    return results


@router.get("/{id_peca}", response_model=PecaResponse)
def detalhe_peca(id_peca: int, db: Session = Depends(get_db)):
    """RF05 — Full part detail including compatibility matrix and technical specs."""
    peca = db.query(Peca).options(
        joinedload(Peca.compatibilidades).joinedload(MatrizCompatibilidade.veiculo),
        joinedload(Peca.categoria),
        joinedload(Peca.fornecedor),
    ).filter(Peca.id_peca == id_peca, Peca.ativo == "S").first()

    if not peca:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    return _build_response(peca)


@router.post("/", response_model=PecaResponse, status_code=201)
def criar_peca(
    payload: PecaCreate,
    current_user: Usuario = Depends(require_fornecedor),
    db: Session = Depends(get_db),
):
    """Create a new part listing (fornecedor only)."""
    ids_veiculos = payload.ids_veiculos_compativeis or []
    peca_data = payload.model_dump(exclude={"ids_veiculos_compativeis"})
    peca = Peca(id_fornecedor=current_user.id_usuario, **peca_data)
    db.add(peca)
    db.flush()  # Get id_peca before adding compatibilities

    for id_veiculo in ids_veiculos:
        db.add(MatrizCompatibilidade(id_peca=peca.id_peca, id_veiculo=id_veiculo))

    db.commit()
    db.refresh(peca)

    peca = db.query(Peca).options(
        joinedload(Peca.compatibilidades).joinedload(MatrizCompatibilidade.veiculo),
        joinedload(Peca.categoria),
        joinedload(Peca.fornecedor),
    ).filter(Peca.id_peca == peca.id_peca).first()
    return _build_response(peca)


@router.put("/{id_peca}", response_model=PecaResponse)
def atualizar_peca(
    id_peca: int,
    payload: PecaUpdate,
    current_user: Usuario = Depends(require_fornecedor),
    db: Session = Depends(get_db),
):
    peca = db.query(Peca).filter(
        Peca.id_peca == id_peca, Peca.id_fornecedor == current_user.id_usuario
    ).first()
    if not peca:
        raise HTTPException(status_code=404, detail="Peça não encontrada")

    update_data = payload.model_dump(exclude_none=True, exclude={"ids_veiculos_compativeis"})
    for field, value in update_data.items():
        setattr(peca, field, value)

    if payload.ids_veiculos_compativeis is not None:
        db.query(MatrizCompatibilidade).filter(MatrizCompatibilidade.id_peca == id_peca).delete()
        for id_veiculo in payload.ids_veiculos_compativeis:
            db.add(MatrizCompatibilidade(id_peca=id_peca, id_veiculo=id_veiculo))

    db.commit()
    db.refresh(peca)
    peca = db.query(Peca).options(
        joinedload(Peca.compatibilidades).joinedload(MatrizCompatibilidade.veiculo),
        joinedload(Peca.categoria),
        joinedload(Peca.fornecedor),
    ).filter(Peca.id_peca == id_peca).first()
    return _build_response(peca)


@router.delete("/{id_peca}")
def desativar_peca(
    id_peca: int,
    current_user: Usuario = Depends(require_fornecedor),
    db: Session = Depends(get_db),
):
    peca = db.query(Peca).filter(
        Peca.id_peca == id_peca, Peca.id_fornecedor == current_user.id_usuario
    ).first()
    if not peca:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    peca.ativo = "N"
    db.commit()
    return {"detail": "Peça desativada"}


@router.post("/compatibilidade/verificar")
def verificar(payload: CompatibilidadeCheck, db: Session = Depends(get_db)):
    """Check if a part is compatible with a given vehicle."""
    result = verificar_compatibilidade(
        db=db,
        id_peca=payload.id_peca,
        id_veiculo=payload.id_veiculo,
        montadora=payload.montadora,
        modelo=payload.modelo,
        ano=payload.ano,
    )
    return result
