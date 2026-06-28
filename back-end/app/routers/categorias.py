from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.models.categoria import Categoria
from app.models.peca import Peca
from app.models.usuario import Usuario
from app.schemas.categoria import CategoriaCreate, CategoriaResponse
from app.core.dependencies import require_admin

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    """RF01 — List featured categories for the home page."""
    cats = db.query(
        Categoria,
        func.count(Peca.id_peca).label("total_pecas")
    ).outerjoin(Peca, (Peca.id_categoria == Categoria.id_categoria) & (Peca.ativo == "S")
    ).group_by(Categoria.id_categoria).all()

    return [
        CategoriaResponse(
            id_categoria=c.id_categoria,
            nome_categoria=c.nome_categoria,
            descricao=c.descricao,
            icone_url=c.icone_url,
            total_pecas=total,
        )
        for c, total in cats
    ]


@router.post("/", response_model=CategoriaResponse, status_code=201)
def criar_categoria(
    payload: CategoriaCreate,
    _: Usuario = Depends(require_admin),
    db: Session = Depends(get_db),
):
    existente = db.query(Categoria).filter(Categoria.nome_categoria == payload.nome_categoria).first()
    if existente:
        raise HTTPException(status_code=400, detail="Categoria já existe")
    cat = Categoria(**payload.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return CategoriaResponse(**cat.__dict__, total_pecas=0)
