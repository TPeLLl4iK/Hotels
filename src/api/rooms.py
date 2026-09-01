from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomsFacilitiesAdd
from src.schemas.rooms import RoomsAdd, RoomsAddRequest, RoomsPatch, RoomsPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получить все номера в отеле")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(
        openapi_examples={
            "default": {
                "summary": "Дата выезда",
                "value": "2026-10-01",
            }
        }
    ),
    date_to: date = Query(
        openapi_examples={
            "default": {
                "summary": "Дата заезда",
                "value": "2026-08-01",
            }
        }
    ),
):

    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get(
    "/{hotel_id}/rooms/{room_id}", summary="Получить номер у определенного отеля"
)
async def get_one_room(hotel_id: int, room_id: int, db: DBDep):

    return await db.rooms.get_one_or_none_with_rels(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}/rooms", summary="Добавить номер")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomsAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "default",
                "value": {
                    "title": "pickme",
                    "description": "pickme_rooms",
                    "price": 5000,
                    "quantity": 4,
                    "facilities_ids": [],
                },
            },
            "2": {
                "summary": "luxe",
                "value": {
                    "title": "emo",
                    "description": "123",
                    "price": 1000,
                    "quantity": 10,
                    "facilities_ids": [],
                },
            },
        }
    ),
):
    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [
        RoomsFacilitiesAdd(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "added", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер в отеле")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):

    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()

    return {"status": "deleted"}


@router.put('/{hotel_id}/rooms/{room_id}', summary='Изменить все данные номера в отеле')
async def put_room(
    hotel_id: int, 
    room_id: int, 
    room_data: RoomsAddRequest, 
    db: DBDep
):

    _room_data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, hotel_id=hotel_id, id=room_id)
    await db.rooms_facilities.set_rooms_facilities(
        room_id, facilities_ids=room_data.facilities_ids
    )
    await db.commit()

    return {"status": "updated"}


@router.patch('/{hotel_id}/rooms/{room_id}', summary='Частично изменить данные номера в отеле')
async def patch_room(hotel_id: int, room_id: int, room_data: RoomsPatchRequest, db: DBDep):
\
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomsPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(
        _room_data,
        exclude_unset=True, 
        hotel_id=hotel_id,
        id=room_id
        )

    if 'facilities_ids' in _room_data_dict:
        await db.rooms_facilities.set_rooms_facilities(room_id, facilities_ids=room_data.facilities_ids)

    await db.commit()
    return {"status": "changed"}
