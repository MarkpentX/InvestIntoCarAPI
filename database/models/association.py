from sqlalchemy import Table, Column, ForeignKey, Integer
from .base import Base

user_car_association = Table(
    "user_car_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("car_id", Integer, ForeignKey("cars.id"), primary_key=True),
)