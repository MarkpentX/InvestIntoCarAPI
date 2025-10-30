from typing import Optional

from pydantic import BaseModel


class SignUpRequest(BaseModel):
    gmail: str
    password: str
    author_code: Optional[int] = None

class SignInRequest(BaseModel):
    gmail: str
    password: str

class SignInOrSignUpResponse(BaseModel):
    gmail: str
    referrer_id: Optional[int] = None
    id: int
    referal_percent: int
    balance: int

class InvestRequest(BaseModel):
    user_id: int
    car_id: int
    amount: int

class PaymentRequest(BaseModel):
    user_id: int
    amount: float
    transaction_hash: str
    from_address: str

class WithdrawRequest(BaseModel):
    user_id: int
    amount: float
    wallet_address: str


# 1
