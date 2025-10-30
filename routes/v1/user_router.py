from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user
from database.database import get_db
from repository import UserRepository
from schemas.routes import InvestRequest, PaymentRequest, SignUpRequest, SignInRequest, WithdrawRequest
from services import UserService

user_router = APIRouter()


async def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(session))

def handle_service_result(result):
    if result.is_success:
        return result.data
    # status_code = USER_ERROR_STATUS_MAP.get(result.error, status.HTTP_500_INTERNAL_SERVER_ERROR)
    raise HTTPException(status_code=500, detail=result.error)

@user_router.post('/sign-in')
async def sign_in(request: SignInRequest, service: UserService = Depends(get_user_service)):
    result = await service.sign_in(request.gmail, request.password)
    return handle_service_result(result)

@user_router.post('/sign-up')
async def sign_up(request: SignUpRequest, service: UserService = Depends(get_user_service)):
    result = await service.sign_up(request.gmail, request.password, request.author_code)
    return handle_service_result(result)

@user_router.get('/user/{user_id}')
async def get_user(user_id: int, service: UserService = Depends(get_user_service), current_user: dict = Depends(get_current_user)):
    result = await service.get_user(user_id)
    return handle_service_result(result)

@user_router.put('/payment')
async def payment(request: PaymentRequest, service: UserService = Depends(get_user_service), current_user: dict = Depends(get_current_user)):
    result = await service.payment(request)
    return handle_service_result(result)

@user_router.post('/invest')
async def invest(request: InvestRequest, service: UserService = Depends(get_user_service), current_user: dict = Depends(get_current_user)):
    result = await service.invest(request.user_id, request.car_id, request.amount)
    return handle_service_result(result)

@user_router.post('/withdraw')
async def withdraw(request: WithdrawRequest, service: UserService = Depends(get_user_service)):
    result = await service.withdraw(request)
    return handle_service_result(result)

# /USER
# POST /user/sign-in - log in to the profile
# POST /user/sign-up - registration
# GET /user/{user_id} -> get profile info
# PUT /user/payment -> {user_id, amount, ...}
# POST /user/invest -> {user_id, car_id, amount, ...}

# /CARS
# POST /car - create a new car
# GET /car -> get all cars
# GET /car/{car_id} -> get info about the specific car

# /ADMIN
# POST /admin/car -> {admin_id, ...car}
# PUT /admin/car -> {admin_id, car_id, ...new_car}
# DELETE /admin/car -> {admin_id, car_id}
# PUT /admin/user -> {isWithdraw: false/true, user_id, admin_id ... }