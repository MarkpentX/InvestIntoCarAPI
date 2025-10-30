from pydantic import BaseModel

class CreateCar(BaseModel):
    password: str
    name: str
    img: str
    price: float
    roi: int
    rent_1_day: int
    prodit_15_day: int
    year_profit: int
    payback: int
    annual_profit: int
    invested: int

class EditCar(BaseModel):
    password: str
    id: int

class EditUserBalance(BaseModel):
    password: str
    user_id: int
    isWithdraw: bool
    amount: float

class DeleteCar(BaseModel):
    password: str
    car_id: int

