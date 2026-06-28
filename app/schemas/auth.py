from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    login: str 
    senha: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    tipo_perfil: str


class TokenData(BaseModel):
    id_usuario: Optional[int] = None
    tipo_perfil: Optional[str] = None
