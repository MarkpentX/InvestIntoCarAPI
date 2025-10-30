from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from database.models import CarModel, UserModel
from .base_repo import BaseRepo


class AdminRepository(BaseRepo):
    def __init__(self, db_session):
        super().__init__(db_session)

    async def create_car(self, request):
        car = CarModel(
            name=request.name,
            img=request.img,
            price=request.price,
            roi=request.roi,
            rent_1_day=request.rent_1_day,
            prodit_15_day=request.prodit_15_day,
            year_profit=request.year_profit,
            payback=request.payback,
            annual_profit=request.annual_profit,
            invested=request.invested
        )

        self._db_session.add(
            car
        )
        await self._db_session.commit()
        return car

    # car = await db_session.get(CarModel, car_id)
    # if car:
    #     # Delete the car
    #     await db_session.delete(car)
    #     await db_session.commit()
    #     return True
    # return False

    async def delete_car(self, request):
        car = await self._db_session.get(CarModel, request.car_id)
        if car:
            await self._db_session.delete(car)
            await self._db_session.commit()
            return "Car deleted successfully"
        raise ValueError("Car not found or does not exist")


    async def edit_user_balance(self, request):
        user = await self._db_session.get(UserModel, request.user_id)
        if user:
            if request.isWithdraw:
                user.balance -= request.amount
                await self._db_session.commit()
                return "User balance updated successfully"
            else:
                user.balance += request.amount
                await self._db_session.commit()
                return "User balance updated successfully"
        raise ValueError("User not found or does not exist")

    # async def distribute_referral_rewards(self):
    #     try:
    #         # Get all users who have referrers and their cars
    #         stmt = (
    #             select(UserModel, UserModel.referrer_id)
    #             .options(selectinload(UserModel.cars))
    #             .where(UserModel.referrer_id.isnot(None))
    #         )
    #
    #         users_with_referrers = (await self._db_session.execute(stmt)).scalars().all()
    #
    #         rewards_distributed = []
    #         referrer_updates = {}
    #
    #         for user in users_with_referrers:
    #             total_invested = sum(car.invested for car in user.cars) if user.cars else 0
    #             if total_invested > 0:
    #                 # Get referrer details
    #                 referrer_result = await self._db_session.execute(
    #                     select(UserModel).filter_by(id=user.referrer_id)
    #                 )
    #                 referrer = referrer_result.scalars().first()
    #
    #                 if referrer:
    #                     reward = total_invested * (referrer.referal_percent / 100)
    #
    #                     # Accumulate rewards for each referrer
    #                     if referrer.id in referrer_updates:
    #                         referrer_updates[referrer.id] += reward
    #                     else:
    #                         referrer_updates[referrer.id] = reward
    #
    #                     rewards_distributed.append({
    #                         "referrer_id": referrer.id,
    #                         "referred_user_id": user.id,
    #                         "reward": reward,
    #                         "total_invested": total_invested
    #                     })
    #
    #         # Update referrer balances
    #         for referrer_id, total_reward in referrer_updates.items():
    #             await self._db_session.execute(
    #                 update(UserModel)
    #                 .where(UserModel.id == referrer_id)
    #                 .values(balance=UserModel.balance + total_reward)
    #             )
    #
    #         await self._db_session.commit()
    #         return {"message": "Referral rewards distributed successfully", "details": rewards_distributed}
    #
    #     except Exception as e:
    #         await self._db_session.rollback()
    #         raise e
