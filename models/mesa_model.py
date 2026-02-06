from pydantic import BaseModel

class MesaCreate(BaseModel):
    numero_mesa: int
    capacidad: int

class MesaUpdate(BaseModel):
    numero_mesa: int
    capacidad: int
