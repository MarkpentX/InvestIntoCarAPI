from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from repository import CarRepository
# from schemas.routes.car_req import CrateCarRequest
from services import CarService

car_router = APIRouter()

async def get_car_service(session: AsyncSession = Depends(get_db)) -> CarService:
    return CarService(CarRepository(session))

def handle_service_result(result):
    if result.is_success:
        return result.data
    # status_code = USER_ERROR_STATUS_MAP.get(result.error, status.HTTP_500_INTERNAL_SERVER_ERROR)
    raise HTTPException(status_code=500, detail=result.error)

@car_router.get("/")
async def gat_all_cars(service: CarService = Depends(get_car_service)):
    result = await service.gat_all_cars()
    return handle_service_result(result)

@car_router.get("/{car_id}")
async def gat_car_by_id(car_id: int, service: CarService = Depends(get_car_service)):
    result = await service.get_car_by_id(car_id)
    return handle_service_result(result)

# /CARS
# POST /car - create a new car
# GET /car -> get all cars
# GET /car/{car_id} -> get info about the specific car
