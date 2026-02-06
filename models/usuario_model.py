from pydantic import BaseModel, EmailStr
from typing import Optional

# 📥 Lo que el cliente envía para registrarse
class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr   # valida formato de email automáticamente
    password: str
    rol: Optional[str] = "cliente"


# 📤 Lo que la API devuelve al frontend (sin contraseña)
class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str

    class Config:
        from_attributes = True  


# 🔐 Para login
class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str
