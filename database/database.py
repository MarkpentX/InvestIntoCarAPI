from environs import Env
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

env = Env()
env.read_env('.env')

DATABASE_URL = URL.create(
    drivername='postgresql+asyncpg',
    username='car_invest_db_user',
    password='ltf13EyjtMt4Fca9L2CcD9kzHzJysLxj',
    host='dpg-d410ic8dl3ps73dd6r1g-a.oregon-postgres.render.com',
    database='car_invest_db',
    port=5432,
).render_as_string(hide_password=False)
# url = "sqlite+aiosqlite:///database.db"

engine = create_async_engine(DATABASE_URL, echo=False, poolclass=None)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
