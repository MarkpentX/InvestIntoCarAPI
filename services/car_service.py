import json
from typing import Optional

from repository import CarRepository
from services.base_service import BaseService, ServiceResult

class CarService(BaseService):
    def __init__(self, repository: CarRepository):
        super().__init__()
        self._repository = repository

    async def gat_all_cars(self):
        try:
            result = await self._repository.gat_all_cars()
            return ServiceResult.success(result)
        except Exception as e:
            return ServiceResult.failure(str(e))

    async def get_car_by_id(self, car_id: int):
        try:
            result = await self._repository.get_car_by_id(car_id)
            return ServiceResult.success(result)
        except Exception as e:
            return ServiceResult.failure(str(e))


