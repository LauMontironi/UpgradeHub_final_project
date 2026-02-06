from datetime import datetime
from fastapi import HTTPException 
import aiomysql as aio
from db.config import get_conexion



# get all menues 
async def get_menus():
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM menus")
            menus = await cursor.fetchall()
            return menus
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

# get menu by fecha

async def get_menus_by_fecha(fecha: str):
    conn = None
    try:
        # Validar formato YYYY-MM-DD
        try:
            fecha_valida = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa YYYY-MM-DD")

        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM menus WHERE fecha = %s", (fecha_valida,))
            menu = await cursor.fetchone()

        if not menu:
            raise HTTPException(status_code=404, detail="No hay menú disponible para esa fecha")

        return {"success": True, "menu": menu}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn is not None:
            conn.close()


