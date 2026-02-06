from fastapi import HTTPException 
import aiomysql as aio
from core.security import create_token, hash_password, verify_password
from db.config import get_conexion
from models.usuario_model import UsuarioCreate, UsuarioLogin


###necesito la funcion get_user_by id para poder obtener el last row id- no lo quiero como ruta porque no me sirve pero si necesitamos la funcion : 

async def get_user_by_id(usuario_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT id, nombre, email, rol FROM usuarios WHERE id = %s",
                (usuario_id,)
            )
            return await cursor.fetchone()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")    
    finally:
        conn.close()


##➕ POST /auth/register

async def register(usuario: UsuarioCreate):

    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            #verificamos que no exista le email :
            await cursor.execute('SELECT * FROM usuarios WHERE email = %s', (usuario.email,))

            existing = await cursor.fetchone()

            if existing:
                raise HTTPException(status_code=400, detail="El usuario ya existe")

            hashed_pass = hash_password(usuario.password)
            await cursor.execute(
                'INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)',
                (usuario.nombre, usuario.email, hashed_pass, usuario.rol)
            )
            await conn.commit()

            new_id= cursor.lastrowid

            usuario_creado = await get_user_by_id(new_id)
            return {
                'msg': 'usuario registrado correctamente', 
                'item': usuario_creado
                }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


##🔑 POST /auth/login

async def login(usuario: UsuarioLogin):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                'SELECT id, nombre, email, password, rol FROM usuarios WHERE email = %s',
                (usuario.email,)
            )
            user = await cursor.fetchone()

            if user is None:
                raise HTTPException(status_code=404, detail="Credenciales invalidas")
            
            if not verify_password(usuario.password, user["password"]):

                raise HTTPException(status_code=401, detail="Credenciales inválidas")
       
        token_data = {
            "id": user["id"],
            "email": user["email"],
            "nombre": user["nombre"],
            "rol": user["rol"]
        }

        token=create_token(token_data)

        return {
            "msg": "Login correcto",
            "Token":token,
            "user": {
                "id": user["id"],
                "nombre": user["nombre"],
                "email": user["email"],
                "rol": user["rol"]

            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
        
       
            
    