from database.models import CarModel
from .base_repo import BaseRepo
from sqlalchemy import select


class CarRepository(BaseRepo):
    def __init__(self, db_session):
        super().__init__(db_session)

    async def gat_all_cars(self):
        cars = await self._db_session.execute(
            select(CarModel)
        )
        cars = cars.scalars().all()
        return cars

    async def get_car_by_id(self, car_id: int):
        car = await self._db_session.get(CarModel, car_id)
        if car:
            return car
        raise ValueError(f"Car {car_id} not found")








