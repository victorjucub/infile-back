from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    idusuario: Optional[str]
    nombre: str
    usuario: str
    correo: str
    clave: str
    usuario_creo: Optional[str]

class UserUpdateSchema(BaseModel):
    idusuario: Optional[str]
    nombre: str
    correo: str
    usuario: str
    usuario_modifico: str

class UserUpdateSchemaWhitPass(BaseModel):
    idusuario: Optional[str]
    clave: Optional[str]
    clave_ultima: Optional[str]
    usuario_modifico: str

class UserLoginSchema(BaseModel):
    correo: str
    clave: str
    recordarme: str
    process: Optional[str]

class GoogleLoginSchema(BaseModel):
    id_token: str

class ForgotPasswordSchema(BaseModel):
    correo: str

class RestorePasswordSchema(BaseModel):
    correo: str
    clave: str
    process: str

class RefreshTokenSchema(BaseModel):
    refresh_token: str

class RevokeSchema(BaseModel):
    refresh_token: str