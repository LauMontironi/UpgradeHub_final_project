from fastapi import FastAPI
from routes  import mesas_routes, test_db_routes, auth_routes, usuarios_routes, reservas_routes, menu_routes







app = FastAPI()


app.include_router(test_db_routes.router, prefix="/debug", tags=["debug"])

app.include_router(auth_routes.router, prefix='/auth', tags= ['auth'])

app.include_router(usuarios_routes.router, prefix='/usuarios', tags= ['usuarios'])


app.include_router(menu_routes.router, prefix='/menu', tags= ['menu'])


app.include_router(reservas_routes.router, prefix="/reservas", tags=["reservas"])

app.include_router(mesas_routes.router, prefix="/mesas", tags=["mesas"])