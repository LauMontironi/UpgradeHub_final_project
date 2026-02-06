from pydantic import BaseModel

class ReservaCreate(BaseModel):
    mesa_id: int
    fecha_reserva: str  # YYYY-MM-DD

class ReservaReview(BaseModel):
    resena: str
