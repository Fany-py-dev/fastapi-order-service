from typing import AsyncGenerator, cast, Callable
from sqlalchemy import Connection
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.db.base import Base
from app.db.connection import get_db
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine_test = create_async_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = async_sessionmaker(bind=engine_test, expire_on_commit=False)

@pytest_asyncio.fixture(scope="session", autouse=True, loop_scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(cast(Callable[[Connection], None], Base.metadata.create_all))
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(cast(Callable[[Connection], None], Base.metadata.drop_all))

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client