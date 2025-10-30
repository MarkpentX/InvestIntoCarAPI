from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped
from .base import Base

class TransactionModel(Base):
    __tablename__ = 'transaction'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaction_hash: Mapped[str] = mapped_column(String, unique=True, index=True)
