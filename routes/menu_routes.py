from fastapi import APIRouter, Depends
from controllers import menu_controllers
from core.dependences import is_admin
from models.menu_model import MenuCreate, MenuUpdate


router = APIRouter()

# MENÚS 

# GET /menus (público) → listar menús

@router.get("/", status_code=200)
async def get_menus():
    return await menu_controllers.get_menus()


# GET /menus/{fecha} 

@router.get("/{fecha}", status_code=200)
async def get_menus_by_fecha(fecha: str):
    return await menu_controllers.get_menus_by_fecha(fecha)



# POST /menus (admin) → crear menú

@router.post("", status_code=201)
async def create_menu(payload: MenuCreate, admin=Depends(is_admin)):
    return await menu_controllers.create_menu(payload)


# PUT /menus/{id} (admin)

@router.put("/{menu_id}", status_code=200)
async def update_menu(menu_id: str, payload: MenuUpdate, admin=Depends(is_admin)):
    return await menu_controllers.update_menu (int((menu_id)), payload)


# DELETE /menus/{id} (admin)

@router.delete("/{menu_id}", status_code=200)
async def delete_menu(menu_id: int, admin=Depends(is_admin)):
    return await menu_controllers.delete_menu(menu_id)