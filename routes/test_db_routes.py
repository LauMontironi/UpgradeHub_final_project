from fastapi import APIRouter, HTTPException
from db.config import get_conexion

router = APIRouter()

@router.get("/test-db")
async def test_db():
    try:
        conn = await get_conexion()
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT 1")
            row = await cursor.fetchone()
        conn.close()
        return {"ok": True, "db_response": row}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
