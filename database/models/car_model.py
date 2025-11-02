from typing import List

from sqlalchemy import String, Integer, Float, ARRAY
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .base import Base
from .association import user_car_association
from .image_model import ImageModel

class CarModel(Base):
    __tablename__ = 'cars'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=True)
    roi: Mapped[int] = mapped_column(Integer, nullable=True)
    rent_1_day: Mapped[int] = mapped_column(Integer, nullable=True)
    prodit_15_day: Mapped[int] = mapped_column(Integer, nullable=True)
    year_profit: Mapped[int] = mapped_column(Integer, nullable=True)
    payback: Mapped[int] = mapped_column(Integer, nullable=True)
    annual_profit: Mapped[int] = mapped_column(Integer, nullable=True)
    invested: Mapped[int] = mapped_column(Integer, nullable=True)

    images: Mapped[List[ImageModel]] = relationship(
        "ImageModel",
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    # many-to-many
    users: Mapped[list["UserModel"]] = relationship(
        "UserModel",
        secondary=user_car_association,
        back_populates="cars"
    )
