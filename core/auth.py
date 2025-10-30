import os
from datetime import timedelta, datetime, UTC

from environs import Env
from jose import jwt

env = Env()
env.read_env('.env')
JWT_SECRET = env.str('JWT_SECRET', 'secret-key')
JWT_ALGORITHM = env.str('JWT_ALGORITHM', 'HS256')

class JWTManager:
    @staticmethod
    def create_access_token(
            data: dict
    ) -> str:
        """
        Create a JWT access token with the given data and expiration time.
        """
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(minutes=600)
        to_encode.update({"exp": int(expire.timestamp())})
        encoded_jwt = jwt.encode(
            to_encode,
            JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> int:
        try:
            print(f"Verifying token: {token}")
            print(f"Using JWT_SECRET: {JWT_SECRET}")
            print(f"Using JWT_ALGORITHM: {JWT_ALGORITHM}")

            payload = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=[JWT_ALGORITHM]
            )
            print(f"Decoded payload: {payload}")

            user_id = payload.get("sub")
            print(f"Extracted user_id: {user_id}")

            if user_id is None:
                raise ValueError("Subject (sub) not found in token")

            return int(user_id)

        except Exception as e:
            print(f"Unexpected error: {e}")
            raise ValueError("Invalid token")