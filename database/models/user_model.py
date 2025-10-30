from sqlalchemy import String, Integer, INTEGER, ForeignKey, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List, Optional

from .base import Base
from .association import user_car_association


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    referal_percent: Mapped[int] = mapped_column(Integer, default=5)
    referrer_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('users.id'),
        nullable=True
    )
    gmail: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[Optional[str]] = mapped_column(String, nullable=True, default=None)
    balance: Mapped[float] = mapped_column(Float, default=0)

    # Self-referential relationship (реферальная система)
    referrer: Mapped[Optional['UserModel']] = relationship(
        'UserModel',
        back_populates='referrals',
        remote_side=[id],
        foreign_keys=[referrer_id]
    )
    referrals: Mapped[list['UserModel']] = relationship(
        'UserModel',
        back_populates='referrer',
        foreign_keys=[referrer_id]
    )

    # many-to-many
    cars: Mapped[List["CarModel"]] = relationship(
        "CarModel",
        secondary=user_car_association,
        back_populates="users"
    )
