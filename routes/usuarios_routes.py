from fastapi import APIRouter, Depends
from core.dependences import is_admin_or_owner
from controllers import usuarios_controllers  

router = APIRouter()

# 🔍 GET /usuarios/id


@router.get("/{user_id}", status_code=200)
async def get_user_id(user_id: str, current_user=Depends(is_admin_or_owner)):
    return await usuarios_controllers.get_user_id(int(user_id))



# PUT /usuarios/id