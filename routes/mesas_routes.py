from fastapi import APIRouter, Depends
from core.dependences import is_admin
from controllers import mesas_controllers
from models.mesa_model import MesaCreate, MesaUpdate

router = APIRouter()

@router.get("", status_code=200)
async def get_mesas():
    return await mesas_controllers.get_mesas()

@router.post("", status_code=201)
async def create_mesa(payload: MesaCreate, admin=Depends(is_admin)):
    return await mesas_controllers.create_mesa(payload)

@router.put("/{mesa_id}", status_code=200)
async def update_mesa(mesa_id: int, payload: MesaUpdate, admin=Depends(is_admin)):
    return await mesas_controllers.update_mesa(mesa_id, payload)

@router.delete("/{mesa_id}", status_code=200)
async def delete_mesa(mesa_id: int, admin=Depends(is_admin)):
    return await mesas_controllers.delete_mesa(mesa_id)
