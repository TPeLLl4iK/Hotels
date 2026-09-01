from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить все удобства")
@cache(expire=10)
async def get_facilities(
    db: DBDep,
):
    test_task.delay()
    return await db.facilities.get_filtered()

    
@router.post('', summary='Создать удобство')
async def create_facilities(
    db: DBDep,
    facilitites_data: FacilitiesAdd
):

    facilities = await db.facilities.add(facilitites_data)
    await db.commit()

    return {"status": "Added", "data": facilities}
