from fastapi import APIRouter, Depends
from core.dependences import get_current_user, is_admin
from controllers import reservas_controllers
from models.reserva_model import ReservaCreate, ReservaReview

router = APIRouter()

@router.post("", status_code=201)
async def create_reserva(payload: ReservaCreate, user=Depends(get_current_user)):
    return await reservas_controllers.create_reserva(payload, user)

@router.get("/me", status_code=200)
async def get_my_reservas(user=Depends(get_current_user)):
    return await reservas_controllers.get_my_reservas(user)

@router.patch("/{reserva_id}/cancel", status_code=200)
async def cancel_reserva(reserva_id: int, user=Depends(get_current_user)):
    return await reservas_controllers.cancel_reserva(reserva_id, user)

@router.patch("/{reserva_id}/review", status_code=200)
async def add_review(reserva_id: int, payload: ReservaReview, user=Depends(get_current_user)):
    return await reservas_controllers.add_review(reserva_id, payload, user)

@router.get("", status_code=200)
async def get_all_reservas(admin=Depends(is_admin)):
    return await reservas_controllers.get_all_reservas()
