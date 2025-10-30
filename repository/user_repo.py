from datetime import datetime, timedelta
from typing import Optional

import requests
from sqlalchemy.orm import selectinload

from database.models import UserModel, CarModel, TransactionModel
from database.models.user_model import UserModel
from .base_repo import BaseRepo
from sqlalchemy import func, select
import asyncio
from aiogram import Bot

TOKEN = '8166134212:AAGLIVjgPaFA5em9rSSoDfH6BG8DvW-AMew'
chat_id = '1103207867' # 805328675
bot = Bot(token=TOKEN)

class UserRepository(BaseRepo):
    def __init__(self, db_session):
        super().__init__(db_session)

    async def get_user_by_email(self, gmail: str) -> UserModel:
        query = select(UserModel).where(
            UserModel.gmail == gmail,
        )
        result = await self._db_session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def sign_up(self, gmail: str, password: str, author_code: Optional[int] = None):
        query = select(UserModel).where(
            UserModel.gmail == gmail,
            UserModel.password == password
        )
        if author_code:
            author_query = select(UserModel).where(
                UserModel.id == author_code,
            )
            author_result = await self._db_session.execute(author_query)
            referer = author_result.scalar_one_or_none()
            if not referer:
                raise Exception('referrer id not found')
        result = await self._db_session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return user
        user = UserModel(
            gmail=gmail,
            password=password,
            referrer_id=author_code
        )

        self._db_session.add(
            user
        )
        await self._db_session.commit()
        return user

    async def get_user(self, user_id: int):
        result = await self._db_session.execute(
            select(UserModel)
            .options(selectinload(UserModel.cars))  # подгружаем связи
            .options(selectinload(UserModel.referrals))  # подгружаем связи
            .where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise ValueError(f"User {user_id} not found")

        total_invested = sum(car.invested or 0 for car in user.cars)

        if 100 <= total_invested < 500:
            rank = "Bronze"
        elif 500 <= total_invested < 1000:
            rank = "Silver"
        elif 1000 <= total_invested < 5000:
            rank = "Gold"
        else:
            rank = "Basic"

        return {
            "user": user,
            "rank": rank,
            "total_invested": total_invested
        }

    async def invest(self, user_id: int, car_id: int, amount: int):
        result = await self._db_session.execute(
            select(UserModel)
            .options(selectinload(UserModel.cars))
            .where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()
        car = await self._db_session.get(CarModel, car_id)

        if not user or not car:
            raise ValueError("User or Car not found")
        if amount < 100:
            raise ValueError("Minimum investment amount is $100")
        if user.balance < amount:
            raise ValueError("Not enough money")

        # Update user balance and invested amount
        user.balance -= amount
        car.invested = (car.invested or 0) + amount

        if car not in user.cars:
            user.cars.append(car)

        # Commit changes
        await self._db_session.commit()
        return "Success"

    async def payment(self, request):
        transaction_hash = request.transaction_hash.strip()
        user = await self._db_session.get(UserModel, request.user_id)

        # --- 1. Проверяем, есть ли уже такой хэш в базе ---
        query = select(TransactionModel).where(TransactionModel.transaction_hash == transaction_hash)
        result = await self._db_session.execute(query)
        existing_tx = result.scalar_one_or_none()

        if existing_tx:
            raise ValueError("❌ Транзакция с таким хэшем уже есть в базе")

        r = requests.get(f"https://apilist.tronscanapi.com/api/transaction-info?hash={transaction_hash}")
        if r.status_code != 200:
            raise ValueError("❌ Не удалось получить данные о транзакции (ошибка API)")

        data = r.json()
        if not data.get("trc20TransferInfo"):
            raise ValueError("❌ В транзакции нет TRC20 перевода")

        transfer = data["trc20TransferInfo"][0]
        from_address = transfer["from_address"]
        to_address = transfer["to_address"]
        amount_raw = int(transfer["amount_str"])
        decimals = transfer["decimals"]
        amount_usdt = amount_raw / (10 ** decimals)
        timestamp = data.get("timestamp")

        expected_to_address = "TE8waYvBK9ithae1799nDWBigoJiS9ep8x"  # ← сюда поставь свой адрес
        expected_from_address = request.from_address
        expected_amount = float(request.amount)

        if from_address.lower() != expected_from_address.lower():
            raise ValueError("❌ Неверный адрес отправителя")
        if to_address.lower() != expected_to_address.lower():
            raise ValueError("❌ Неверный адрес получателя")

        if round(amount_usdt, 2) != round(expected_amount, 2):
            raise ValueError(f"❌ Неверная сумма. Ожидалось {expected_amount}, получено {amount_usdt}")

        tx_time = datetime.fromtimestamp(timestamp / 1000)
        if datetime.now() - tx_time > timedelta(minutes=260):
            raise ValueError("❌ Транзакция старше 5 минут")

        new_tx = TransactionModel(transaction_hash=transaction_hash)
        self._db_session.add(new_tx)
        referrer = await self._db_session.get(UserModel, user.referrer_id)
        if referrer:
            referrer_add_balance = amount_usdt * (5/ 100)
            referrer.balance += referrer_add_balance

        user.balance += amount_usdt
        await self._db_session.commit()

        return {"status": "✅ Транзакция успешно подтверждена"}

    async def withdraw(self, request):
        user = await self._db_session.get(UserModel, request.user_id)
        if not user:
            raise ValueError("User not found")
        if user.balance < request.amount:
            raise ValueError("Not enough money")
        # user.balance -= request.amount
        # await self._db_session.commit()
        text = f"New withdraw request \n Amount: {request.amount} \n Address: {request.wallet_address} \n User_id: {request.user_id}"
        await bot.send_message(chat_id, text)
        return "Success"









