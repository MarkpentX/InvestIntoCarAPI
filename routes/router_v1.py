from fastapi import APIRouter

from routes.v1 import user_router, car_router, admin_router

api_v1_router = APIRouter()

api_v1_router.include_router(user_router, prefix='/users', tags=['user'])
api_v1_router.include_router(car_router, prefix='/cars', tags=['car'])
api_v1_router.include_router(admin_router, prefix='/admin', tags=['admin'])
# api_v1_router.include_router(car_router, prefix='/cars', tags=['car'])
