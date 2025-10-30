from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from repository import UserRepository
from services import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/user/token')

async def get_user_service(
    session: AsyncSession = Depends(get_db),
) -> UserService:
    return UserService(UserRepository(session))

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service)
) -> dict:
    user_id = service.get_user_id_by_token(token)
    if not user_id:
        print('401')
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
