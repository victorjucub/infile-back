from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    idusuario: Optional[str]
    nombre: str
    usuario: str
    correo: str
    clave: str
    usuario_creo: str

class UserUpdateSchema(BaseModel):
    idusuario: Optional[str]
    nombre: str
    correo: str
    usuario: str
    clave: Optional[str]
    clave_ultima: Optional[str]
    usuario_modifico: str

class UserLoginSchema(BaseModel):
    correo: str
    clave: str