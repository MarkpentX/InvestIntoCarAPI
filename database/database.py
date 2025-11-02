from environs import Env
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

env = Env()
env.read_env('.env')

DATABASE_URL = URL.create(
    drivername='postgresql+asyncpg',
    username='car_invest_db_ga2b_user',
    password='Dk9H8kaa4mja8OyZfqpNcalbWxX190US',
    host='dpg-d43hvuur433s739hlhrg-a.oregon-postgres.render.com',
    database='car_invest_db_ga2b',
    port=5432,
).render_as_string(hide_password=False)
# DATABASE_URL = "sqlite+aiosqlite:///database.db"

engine = create_async_engine(DATABASE_URL, echo=False, poolclass=None)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
