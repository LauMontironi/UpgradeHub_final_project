from fastapi import APIRouter
from controllers import auth_controllers
from models.usuario_model import UsuarioCreate, UsuarioLogin


router = APIRouter()

##➕ POST /auth/register

@router.post('/register', status_code=201)
async def register(usuario: UsuarioCreate):
    return await auth_controllers.register(usuario)

##🔑 POST /auth/login

@router.post('/login', status_code=200)
async def login(usuario: UsuarioLogin):
    return await auth_controllers.login(usuario)