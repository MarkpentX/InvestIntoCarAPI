from repository import CarRepository, AdminRepository
from services.base_service import BaseService, ServiceResult



class AdminService(BaseService):
    def __init__(self, repository: AdminRepository):
        super().__init__()
        self._repository = repository

    def check_password(self, password: str) -> bool:
        return password == "Test2Password"

    async def create_car(self, request):
        if not self.check_password(request.password):
            return ServiceResult.fail("Wrong password")
        try:
            result = await self._repository.create_car(request)
            return ServiceResult.success(result)
        except Exception as e:
            return  ServiceResult.failure(str(e))

    async def delete_car(self, request):
        if not self.check_password(request.password):
            return ServiceResult.fail("Wrong password")
        try:
            result = await self._repository.delete_car(request)
            return ServiceResult.success(result)
        except Exception as e:
            return ServiceResult.failure(str(e))

    async def edit_user_balance(self, request):
        if not self.check_password(request.password):
            return ServiceResult.fail("Wrong password")
        try:
            result = await self._repository.edit_user_balance(request)
            return ServiceResult.success(result)
        except Exception as e:
            return ServiceResult.failure(str(e))

    #
    # async def distribute_referral_rewards(self, password: str):
    #     if not self.check_password(password):
    #         return ServiceResult.fail("Wrong password")
    #     try:
    #         result = await self._repository.distribute_referral_rewards()
    #         return ServiceResult.success(result)
    #     except Exception as e:
    #         return ServiceResult.failure(str(e))