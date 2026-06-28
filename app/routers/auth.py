from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, Token
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.core.security import verify_password, hash_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/cadastro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def cadastrar(payload: UsuarioCreate, db: Session = Depends(get_db)):
    """RF02 — User registration (Comprador / Oficina / Fornecedor)."""
    existente = db.query(Usuario).filter(
        or_(Usuario.email == payload.email, Usuario.cpf_cnpj == payload.cpf_cnpj)
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="E-mail ou CPF/CNPJ já cadastrado")

    usuario = Usuario(
        tipo_perfil=payload.tipo_perfil,
        email=payload.email,
        senha_hash=hash_password(payload.senha),
        nome_razao_social=payload.nome_razao_social,
        cpf_cnpj=payload.cpf_cnpj,
        telefone=payload.telefone,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """RF03 — Login via e-mail or CPF/CNPJ + password."""
    usuario = db.query(Usuario).filter(
        or_(Usuario.email == payload.login, Usuario.cpf_cnpj == payload.login),
        Usuario.ativo == "S",
    ).first()

    if not usuario or not verify_password(payload.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

    token = create_access_token({"sub": str(usuario.id_usuario), "perfil": usuario.tipo_perfil})
    return Token(access_token=token, tipo_perfil=usuario.tipo_perfil)
