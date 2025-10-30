from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from repository.admin_repo import AdminRepository
from schemas.routes.admin_req import CreateCar, DeleteCar, EditUserBalance
from services import AdminService

# from schemas.routes.car_req import CrateCarRequest

admin_router = APIRouter()

async def get_admin_service(session: AsyncSession = Depends(get_db)) -> AdminService:
    return AdminService(AdminRepository(session))

def handle_service_result(result):
    if result.is_success:
        return result.data
    # status_code = USER_ERROR_STATUS_MAP.get(result.error, status.HTTP_500_INTERNAL_SERVER_ERROR)
    raise HTTPException(status_code=500, detail=result.error)

@admin_router.post("/")
async def create_car(request: CreateCar, service: AdminService = Depends(get_admin_service)):
    result = await service.create_car(request)
    return handle_service_result(result)

@admin_router.delete("/")
async def delete_car(request: DeleteCar, service: AdminService = Depends(get_admin_service)):
    result = await service.delete_car(request)
    return handle_service_result(result)

@admin_router.put("/edit_balance")
async def edit_user_balance(request: EditUserBalance, service: AdminService = Depends(get_admin_service)):
    result = await service.edit_user_balance(request)
    return handle_service_result(result)

# @admin_router.post("/distribute_referral_rewards")
# async def distribute_referral_rewards(password: str, service: AdminService = Depends(get_admin_service)):
#     result = await service.distribute_referral_rewards(password)
#     return handle_service_result(result)

# /ADMIN
# POST /admin/car -> {admin_id, ...car}
# PUT /admin/car -> {admin_id, car_id, ...new_car}
# DELETE /admin/car -> {admin_id, car_id}
# PUT /admin/user -> {isWithdraw: false/true, user_id, admin_id ... }