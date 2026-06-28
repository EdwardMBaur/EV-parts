from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.endereco import Endereco
from app.models.usuario import Usuario
from app.schemas.endereco import EnderecoCreate, EnderecoResponse, EnderecoUpdate, CEPResponse
from app.core.dependencies import get_current_user
from app.services.cep_service import buscar_cep

router = APIRouter(prefix="/enderecos", tags=["Endereços"])


@router.get("/cep/{cep}", response_model=CEPResponse)
async def consultar_cep(cep: str):
    """RF02 — Auto-fill address data from a Brazilian ZIP code (ViaCEP)."""
    data = await buscar_cep(cep)
    if not data:
        raise HTTPException(status_code=404, detail="CEP não encontrado")
    return data


@router.get("/", response_model=List[EnderecoResponse])
def list_enderecos(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(Endereco).filter(Endereco.id_usuario == current_user.id_usuario).all()


@router.post("/", response_model=EnderecoResponse, status_code=201)
def create_endereco(
    payload: EnderecoCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.principal == "S":
        db.query(Endereco).filter(
            Endereco.id_usuario == current_user.id_usuario, Endereco.principal == "S"
        ).update({"principal": "N"})

    endereco = Endereco(id_usuario=current_user.id_usuario, **payload.model_dump())
    db.add(endereco)
    db.commit()
    db.refresh(endereco)
    return endereco


@router.put("/{id_endereco}", response_model=EnderecoResponse)
def update_endereco(
    id_endereco: int,
    payload: EnderecoUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    endereco = db.query(Endereco).filter(
        Endereco.id_endereco == id_endereco,
        Endereco.id_usuario == current_user.id_usuario,
    ).first()
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")

    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(endereco, field, value)
    db.commit()
    db.refresh(endereco)
    return endereco


@router.delete("/{id_endereco}")
def delete_endereco(
    id_endereco: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    endereco = db.query(Endereco).filter(
        Endereco.id_endereco == id_endereco,
        Endereco.id_usuario == current_user.id_usuario,
    ).first()
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    db.delete(endereco)
    db.commit()
    return {"detail": "Endereço removido"}
