📘 Proyecto UpgradeFood — Documentación Backend (Paso a Paso)

Este documento explica cómo se construyó el backend desde cero, las decisiones de arquitectura y los siguientes pasos de desarrollo.

1️⃣ Creación del entorno de trabajo:

mkdir ProyectoUpgrade
cd ProyectoUpgrade

2️⃣ Entorno virtual y dependencias

Creamos y activamos un entorno virtual para aislar el proyecto:

python -m venv .venv
source .venv/Scripts/activate # Windows Git Bash

Instalamos dependencias:

pip install "fastapi[standard]"
pip install aiomysql
pip install python-dotenv
pip install "passlib[argon2]"
pip install "python-jose[cryptography]"

Guardamos versiones:

pip freeze > requirements.txt

3️⃣ Base de Datos MySQL (Aiven)

Decidimos que la base de datos no debía estar en localhost para que el sistema funcione en producción y para que todos los integrantes del equipo puedan conectarse.

Además:

✔ Las imágenes de los menús NO se guardan en el frontend
✔ Se almacenan en la nube (Cloudflare R2 / similar)
✔ En la base solo guardamos la URL de la imagen

Proveedor elegido: MySQL en Aiven

📐 Modelo Entidad-Relación

El sistema se diseñó simple pero funcional.

🧑‍🍳 Tabla: usuarios

| Campo    | Tipo                    | Descripción   |
| -------- | ----------------------- | ------------- |
| id       | PK                      | Identificador |
| nombre   | VARCHAR                 | Nombre        |
| email    | VARCHAR UNIQUE          | Login         |
| password | VARCHAR                 | Contraseña    |
| rol      | ENUM('admin','cliente') | Permisos      |

🍽 Tabla: menus ( las fotos guardamos url ahora mimso hay ejemplos sacdos de unsplash- guardamos url de imagenes en el backend para no guardar fotos en assets en el frontedn)

| Campo       | Tipo        | Descripción     |
| ----------- | ----------- | --------------- |
| id          | PK          | Identificador   |
| fecha       | DATE UNIQUE | Un menú por día |
| nombre      | VARCHAR     | Nombre del menú |
| descripcion | TEXT        | Detalles        |
| foto_url    | VARCHAR     | URL imagen      |
| precio      | DECIMAL     | Precio          |

🪑 Tabla: mesas

| Campo       | Tipo       |
| ----------- | ---------- |
| id          | PK         |
| numero_mesa | INT UNIQUE |
| capacidad   | INT        |

📅 Tabla: reservas

| Campo         | Tipo                           |
| ------------- | ------------------------------ |
| id            | PK                             |
| usuario_id    | FK → usuarios                  |
| mesa_id       | FK → mesas                     |
| fecha_reserva | DATE                           |
| estado        | ENUM('confirmada','cancelada') |
| resena        | TEXT                           |

🛍 Tabla: pedidos ( hecha por si hacemos la seccion de pedidos a domicilio)

| Campo             | Tipo                                                                   |
| ----------------- | ---------------------------------------------------------------------- |
| id                | INT (PK, AI)                                                           |
| usuario_id        | INT (FK → usuarios.id)                                                 |
| menu_id           | INT (FK → menus.id)                                                    |
| direccion_entrega | TEXT                                                                   |
| telefono_contacto | VARCHAR(20)                                                            |
| fecha_pedido      | DATETIME                                                               |
| estado            | ENUM('pendiente','en_preparacion','en_camino','entregado','cancelado') |
| cantidad          | INT                                                                    |
| total             | DECIMAL(10,2)                                                          |

4️⃣ Reglas de Negocio:

🔓 Menús públicos: se pueden consultar sin login
🔐 Reservas requieren login
🚫 Antes de reservar una mesa se debe validar que no esté ocupada en esa fecha
👑 Rol admin gestiona menús y mesas
👤 Rol cliente puede reservar y cancelar

5️⃣ 🔌 Conexión Backend ↔ Base de Datos

Creamos .env con credenciales Aiven:

MYSQL_HOST=xxxxx.aivencloud.com
MYSQL_PORT=11862
MYSQL_USER=avnadmin
MYSQL_PASSWORD=xxxxxx
MYSQL_DATABASE=defaultdb
MYSQL_CA_CERT=db/aiven-ca.pem

config.py

import aiomysql
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

async def get_conexion():
ca_path = os.getenv("MYSQL_CA_CERT", "db/aiven-ca.pem")
ssl_context = ssl.create_default_context(cafile=ca_path)

    return await aiomysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DATABASE"),
        ssl=ssl_context
    )

6️⃣ 🧪 Test de conexión

Creamos routes/test_db_routes.py

from fastapi import APIRouter
from config import get_conexion

router = APIRouter()

@router.get("/test-db")
async def test_db():
conn = await get_conexion()
async with conn.cursor() as cursor:
await cursor.execute("SELECT 1")
result = await cursor.fetchone()
conn.close()
return {"db_response": result}

En main.py:

app.include_router(test_db_routes.router, prefix="/debug", tags=["debug"])

Probar en:
http://127.0.0.1:8000/debug/test-db

✔ Si devuelve { "db_response": (1,) } la conexión funciona

#########################################################################

🚀 SIGUIENTE PASO —

🔐 7 AUTENTICACIÓN

Vamos a dividir en AUTH y USUARIOS ( los modelos estan todos en usuario_model.py)

🔐 AUTH (registro y login)

➕ POST /auth/register

Qué hace: crea un usuario (por defecto rol="cliente").
Validación interna: antes de insertar, el backend hace SELECT ... WHERE email = ? para asegurar que no exista.

Body:

{
"nombre": "Juan",
"email": "juan@email.com",
"password": "123456"
}

Response:==> FRONTED ( para que sepamos el tipo en el fronted despues ) TYPE<{register_response: RegisterResponse}>

TYPE : RegisterResponse = {
msg: string;
item: IUsuario;
};

HTTP/1.1 201 Created
date: Fri, 06 Feb 2026 13:38:27 GMT
server: uvicorn
content-length: 126
content-type: application/json
connection: close

{
"msg": "usuario registrado correctamente",
"item": {
"id": 4,
"nombre": "Laura Montironi",
"email": "laura@demo.com",
"rol": "cliente"
}
}

🔑 POST /auth/login

Descripción: Login usuario

Body:

{
"email": "juan@email.com",
"password": "123456"
}

Response: ==> FRONTED ( para que sepamos el tipo en el fronted despues ) type LoginResponse = {
message: string;
token: string;
user:IUsuario;
};

HTTP/1.1 200 OK
date: Fri, 06 Feb 2026 14:02:53 GMT
server: uvicorn
content-length: 324
content-type: application/json
connection: close

{
"msg": "Login correcto",
"Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NCwiZW1haWwiOiJsYXVyYUBkZW1vLmNvbSIsIm5vbWJyZSI6IkxhdXJhIE1vbnRpcm9uaSIsInJvbCI6ImNsaWVudGUiLCJleHAiOjE3NzAzOTAxNzZ9.HGC14Su2dFM_Pa56FYU4-qx_VuUqwgwFDNnsgxagrbQ",
"user": {
"id": 4,
"nombre": "Laura Montironi",
"email": "laura@demo.com",
"rol": "cliente"
}
}

❌ Response (credenciales incorrectas):

HTTP/1.1 500 Internal Server Error
date: Fri, 06 Feb 2026 14:03:49 GMT
server: uvicorn
content-length: 48
content-type: application/json
connection: close

{
"detail": "Error: 401: Credenciales inválidas"
}

👤 USUARIOS (requiere token)

🔍 GET /usuarios/{id} ✅ DONE

Devuelve datos del usuario logueado frontend type == ? es neceario ?

HTTP/1.1 200 OK
date: Fri, 06 Feb 2026 14:52:52 GMT
server: uvicorn
content-length: 76
content-type: application/json
connection: close

{
"id": 4,
"nombre": "Laura Montironi",
"email": "laura@demo.com",
"rol": "cliente"
}

🍽 MENÚS (públicos)
🔍 GET /menu/ ✅ DONE (all)

Devuelve array de objetos.
Frontend type: IMenu[] que tendra que tener en nuestra interfaz id, fecha, nombre, descripcion, foto_url, precio

HTTP/1.1 200 OK
date: Fri, 06 Feb 2026 15:03:06 GMT
server: uvicorn
content-length: 736
content-type: application/json
connection: close

ejemplo de respuesta :

{
"id": 1,
"fecha": "2024-05-22",
"nombre": "Menú del Día: Pasta",
"descripcion": "Espaguetis al pesto, ensalada caprese y bebida.",
"foto_url": "https://images.unsplash.com/photo-1473093226795-af9932fe5856?auto=format&fit=crop&w=600",
"precio": 12.5
},

🔍 GET /menu/{fecha} ✅ DONE (por fecha)

response :

HTTP/1.1 200 OK
date: Fri, 06 Feb 2026 15:40:33 GMT
server: uvicorn
content-length: 265
content-type: application/json
connection: close

{
"success": true,
"menu": {
"id": 1,
"fecha": "2024-05-22",
"nombre": "Menú del Día: Pasta",
"descripcion": "Espaguetis al pesto, ensalada caprese y bebida.",
"foto_url": "https://images.unsplash.com/photo-1473093226795-af9932fe5856?auto=format&fit=crop&w=600",
"precio": 12.5
}
}

🔒 ADMIN — CRUD MENÚS

| Método | Ruta               | Descripción   |
| ------ | ------------------ | ------------- |
| POST   | `/menus`           | Crear menú    |
| PUT    | `/menus/{menu_id}` | Editar menú   |
| DELETE | `/menus/{menu_id}` | Eliminar menú |

Validación obligatoria:
✔ Solo admin
✔ Fecha no duplicada (control BD + validación)

(Opcional)
POST /menus/{menu_id}/duplicate

🪑 11. MESAS

| Método | Ruta               | Acceso  |
| ------ | ------------------ | ------- |
| GET    | `/mesas`           | Público |
| POST   | `/mesas`           | Admin   |
| PUT    | `/mesas/{mesa_id}` | Admin   |
| DELETE | `/mesas/{mesa_id}` | Admin   |

📅 12. RESERVAS
🔒 Cliente

| Método | Ruta                      | Descripción      |
| ------ | ------------------------- | ---------------- |
| POST   | `/reservas`               | Crear reserva    |
| GET    | `/reservas/me`            | Ver MIS reservas |
| PUT    | `/reservas/{id}/cancelar` | Cancelar reserva |
| PUT    | `/reservas/{id}/resena`   | Escribir reseña  |

Validaciones backend obligatorias:
✔ Mesa disponible en esa fecha
✔ Solo dueño puede cancelar o reseñar
✔ Solo si estado = confirmada

👑 Admin

| Método | Ruta                          | Descripción          |
| ------ | ----------------------------- | -------------------- |
| GET    | `/reservas`                   | Ver TODAS            |
| GET    | `/reservas?with_reviews=true` | Ver solo con reseñas |

✅ ESTADO ACTUAL DEL PROYECTO

✔ Entorno configurado
✔ Conexión MySQL (Aiven)
✔ Modelo de datos definido
✔ Test DB funcionando
✔ Auth (register/login)
✔ GET usuario
✔ GET menús

🟡 Falta implementar (solo controllers y peticiones.rest):

CRUD MENÚS (admin)

CRUD MESAS (admin)

POST RESERVA

GET RESERVAS usuario

CANCELAR RESERVA

RESEÑA

GET RESERVAS admin
