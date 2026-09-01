#ruff: noqa: I001
import pytest
import json
from unittest import mock

mock.patch('fastapi_cache.decorator.cache', lambda *args, **kwargs: lambda f: f).start()

from src.models import *

from src.database import Base, engine
from src.database import settings
from src.database import async_session_maker_null_pool
from src.main import app
from src.schemas.hotels import HotelsAdd
from src.schemas.rooms import RoomsAdd
from src.api.dependencies import DBManager, get_db



from httpx import ASGITransport, AsyncClient

@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    print(settings.MODE)
    assert settings.MODE == "TEST"

@pytest.fixture()
async def db():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

app.dependency_overrides[get_db] = get_db_null_pool

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)



@pytest.fixture(scope='session', autouse=True)
async def post_data(setup_database):
    with open('tests/mock_hotels.json', 'r', encoding='utf-8') as hotels_data:
        hotels = json.load(hotels_data)

    with open('tests/mock_rooms.json', 'r', encoding='utf-8') as rooms_data:
        rooms = json.load(rooms_data)

    hotels = [HotelsAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomsAdd.model_validate(room) for room in rooms]
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()

@pytest.fixture(scope='session', autouse=True)
async def ac():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
        yield ac

@pytest.fixture(scope='session', autouse=True)
async def register_user(ac, setup_database):
    response = await ac.post(
        '/auth/register',
        json={'login': 'sveta', 'password': '1234'}
    )

    assert response.status_code == 200

@pytest.fixture(scope='session')
async def authenticated_ac(ac, register_user):
    response = await ac.post(
        '/auth/login',
        json={'login': 'sveta', 'password': '1234'}
    )

    assert response.status_code == 200
    assert ac.cookies['access_token']
    yield ac
