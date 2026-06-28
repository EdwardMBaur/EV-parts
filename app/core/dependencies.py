from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import decode_access_token
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(Usuario).filter(
        Usuario.id_usuario == int(user_id),
        Usuario.ativo == "S",
    ).first()
    if user is None:
        raise credentials_exception
    return user


def require_fornecedor(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    if current_user.tipo_perfil not in ("fornecedor", "admin"):
        raise HTTPException(status_code=403, detail="Acesso restrito a fornecedores")
    return current_user


def require_admin(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    if current_user.tipo_perfil != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return current_user
