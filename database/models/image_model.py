from typing import List
from sqlalchemy import INTEGER, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .base import Base

class ImageModel(Base):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    url: Mapped[str] = mapped_column(String)
    product_id: Mapped[int] = mapped_column(INTEGER, ForeignKey('cars.id'))
    product: Mapped["CarModel"] = relationship(back_populates="images")