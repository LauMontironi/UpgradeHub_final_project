import os
import ssl
import aiomysql
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

async def get_conexion():
    ca_rel = os.getenv("MYSQL_CA_CERT", "./db/aiven-ca.pem")
    ca_path = Path(ca_rel).resolve()

    ssl_context = ssl.create_default_context(cafile=str(ca_path))

    return await aiomysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DATABASE"),
        autocommit=True,
        ssl=ssl_context,
    )
