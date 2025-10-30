import logging
from abc import ABC
from typing import Optional

from pydantic import BaseModel
from typing_extensions import Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class BaseService(ABC, Generic[T, U]):
    def __init__(self):
        self._logger = logging.getLogger(name=self.__class__.__name__)


class ServiceResult(BaseModel, Generic[T]):
    is_success: bool
    data: Optional[T] = None
    error: Optional[str] = None

    @classmethod
    def success(cls, data: T):
        return cls(is_success=True, data=data)

    @classmethod
    def failure(cls, error: str):
        return cls(is_success=False, error=error)
