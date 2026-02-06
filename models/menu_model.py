from pydantic import BaseModel

class MenuCreate(BaseModel):
    fecha: str
    nombre: str
    descripcion: str | None = None
    foto_url: str | None = None
    precio: float

class MenuUpdate(BaseModel):
    nombre: str
    descripcion: str | None = None
    foto_url: str | None = None
    precio: float
