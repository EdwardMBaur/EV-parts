from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioResponse, UsuarioUpdate
from app.core.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.get("/me", response_model=UsuarioResponse)
def get_me(current_user: Usuario = Depends(get_current_user)):
    """Returns the currently authenticated user's profile."""
    return current_user


@router.put("/me", response_model=UsuarioResponse)
def update_me(
    payload: UsuarioUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/me")
def deactivate_me(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.ativo = "N"
    db.commit()
    return {"detail": "Conta desativada com sucesso"}


# --- Admin-only endpoints ---
@router.get("/", response_model=list[UsuarioResponse])
def list_usuarios(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    return db.query(Usuario).offset(skip).limit(limit).all()


@router.get("/{id_usuario}", response_model=UsuarioResponse)
def get_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario
