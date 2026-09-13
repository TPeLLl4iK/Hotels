from datetime import date

from fastapi import APIRouter, Body, Query, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import HotelsAdd, HotelsPATCH
from src.exceptions import check_date_accuracy, ObjectNotFoundException, HotelNotFoundHTTPException

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}", summary="Получение отеля по айди ")
async def get_one_hotel(hotel_id: int, db: DBDep):
    try:
        return await db.hotels.get_one(id=hotel_id)

    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.get("", summary="Получение информации об отелях")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(
        None,
        description="Название отеля",
        openapi_examples={
            "default": {
                "summary": "Без фильтра",
                "value": None,
            },
            "example1": {
                "summary": "Поиск по названию 'Sochi'",
                "value": "Сочи-стар",
            },
            "example2": {
                "summary": "Поиск по названию 'St. Petersburg'",
                "value": "Питер-стар",
            },
            "example3": {
                "summary": "Питер-elite",
                "value": "Питер-elite",
            },
        },
    ),
    location: str | None = Query(
        None,
        description="Место отеля",
        openapi_examples={
            "default": {
                "summary": "Без фильтра",
                "value": None,
            },
            "example1": {
                "summary": "Сочи-стар",
                "value": "ул. Моря 1",
            },
            "example2": {
                "summary": "Питер-стар",
                "value": "ул. Блюхера 1",
            },
            "example3": {
                "summary": "Питер-elite",
                "value": "Ст. Петербург, ул. Маршала-Бюхера 3",
            },
        },
    ),
    date_from: date = Query(
        description="Дата заезда",
        openapi_examples={
            "1": {
                "summary": "2026-10-01",
                "value": "2026-10-01",
            },
        },
    ),
    date_to: date = Query(
        description="Дата выезда",
        openapi_examples={
            "1": {
                "summary": "2026-09-01",
                "value": "2026-09-01",
            },
        },
    ),
):

    check_date_accuracy(date_from, date_to)
    per_page = pagination.per_page or 5
    try:
            
        return await db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=pagination.page * per_page - per_page,
        )
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

@router.post("", summary="Создание отеля")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelsAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "Сочи-стар", "location": "ул. Моря 1"},
            },
            "2": {
                "summary": "Дубай",
                "value": {"title": "Дубай-стар", "location": "ул. Шейха 2"},
            },
        }
    ),
):

    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "Added", "data": hotel}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(db: DBDep, hotel_id: int):

    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "deleted"}


@router.put(
    "/{hotel_id}",
    summary="Полное изменение данных отеля",
    description="Меняем все данные",
)
async def put_hotel(db: DBDep, hotel_id: int, hotel_data: HotelsAdd):

    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "updated"}


@router.patch(
    "/{hotel_id}",
    summary="Изменение отдельных данных отела",
    description="Меняем данные",
)
async def patch_hotel(hotel_id: int, hotel_data: HotelsPATCH, db: DBDep):

    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "changed"}
