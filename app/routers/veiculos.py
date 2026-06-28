from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional

from app.database import get_db
from app.models.veiculo import Veiculo
from app.models.usuario import Usuario
from app.schemas.veiculo import VeiculoCreate, VeiculoResponse
from app.core.dependencies import require_admin

router = APIRouter(prefix="/veiculos", tags=["Veículos"])


@router.get("/", response_model=List[VeiculoResponse])
def listar_veiculos(
    montadora: Optional[str] = Query(None),
    modelo: Optional[str] = Query(None),
    ano: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    """Search vehicles for the compatibility selector."""
    query = db.query(Veiculo)
    if montadora:
        query = query.filter(Veiculo.montadora.ilike(f"%{montadora}%"))
    if modelo:
        query = query.filter(Veiculo.modelo.ilike(f"%{modelo}%"))
    if ano:
        query = query.filter(Veiculo.ano_fabricacao == ano)
    return query.order_by(Veiculo.montadora, Veiculo.modelo, Veiculo.ano_fabricacao).all()


@router.get("/montadoras")
def listar_montadoras(db: Session = Depends(get_db)):
    """Returns list of distinct manufacturers in the database."""
    montadoras = db.query(Veiculo.montadora).distinct().order_by(Veiculo.montadora).all()
    return [m[0] for m in montadoras]


@router.post("/", response_model=VeiculoResponse, status_code=201)
def criar_veiculo(
    payload: VeiculoCreate,
    _: Usuario = Depends(require_admin),
    db: Session = Depends(get_db),
):
    veiculo = Veiculo(**payload.model_dump())
    db.add(veiculo)
    db.commit()
    db.refresh(veiculo)
    return veiculo
