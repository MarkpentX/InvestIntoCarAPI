import json
from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext

from core.auth import JWTManager
from repository import UserRepository
from schemas.routes import PaymentRequest, SignInOrSignUpResponse
from services.base_service import BaseService, ServiceResult

pwd_context = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])

class UserService(BaseService):
    def __init__(self, repository: UserRepository):
        super().__init__()
        self._repository = repository
        self._jwt_manager = JWTManager()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def get_user_id_by_token(self, token: str) -> Optional[int]:
        try:
            print('token:', token)
            user_id = self._jwt_manager.verify_token(token)
            return user_id
        except ValueError:
            return None

    async def sign_in(self, gmail: str, password: str):
        try:
            user = await self._repository.get_user_by_email(gmail)
            if not user or not self.verify_password(password, user.password):
                return ServiceResult.failure("Invalid credentials")
            token_data = {
                'sub': str(user.id),
            }
            access_token = self._jwt_manager.create_access_token(token_data)
            return ServiceResult.success(access_token)
        except Exception as e:
            return ServiceResult.failure(str(e))

    async def sign_up(self, gmail: str, password: str, author_code: Optional[int] = None):
        hashed_password = self._hash_password(password)
        try:
            result = await self._repository.sign_up(
                gmail=gmail,
                password=hashed_password,
                author_code=author_code
            )
            response = SignInOrSignUpResponse(
                gmail=result.gmail,
                referrer_id=result.referrer_id,
                id=result.id,
                referal_percent=result.referal_percent,
                balance=result.balance,
            )
            return ServiceResult.success(response)
        except Exception as e:
            return ServiceResult.failure(str(e))

    async def get_user(self, user_id: int):
        try:
            result = await self._repository.get_user(user_id)

            return ServiceResult.success(result)
        except Exception as e:
            return ServiceResult.failure(str(e))

    async def invest(self, user_id: int, car_id: int, amount: int):
        try:
            result = await self._repository.invest(user_id, car_id, amount)
            return ServiceResult.success(result)
        except Exception as e:
            return ServiceResult.failure(str(e))

    async def payment(self, request):
        try:
            result = await self._repository.payment(request)
            return ServiceResult.success(result)
        except Exception as e:
            return ServiceResult.failure(str(e))

    async def withdraw(self, request):
        try:
            result = await self._repository.withdraw(request)
            return ServiceResult.success(result)
        except Exception as e:
            return ServiceResult.failure(str(e))