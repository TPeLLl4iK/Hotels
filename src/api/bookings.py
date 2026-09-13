from fastapi import APIRouter, HTTPException

from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundHTTPException
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingsAdd, BookingsAddRequest

router = APIRouter(prefix='/bookings', tags=['Бронирования'])

@router.post('', summary='Созданть бронирование')
async def add_booking(
    booking_data: BookingsAddRequest, 
    db: DBDep,
    user_id: UserIdDep
):

    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    
    room_price: int = room.price
    _booking_data = BookingsAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)

    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    
    await db.commit()
    return {"status": "Added", "data": booking}


@router.get("", summary="Получить все бронирования")
async def get_all_bookings(
    db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/me", summary="Получить бронирования аутентифицированного пользователя")
async def get_booking(
    user_id: UserIdDep,
    db: DBDep,
):

    return await db.bookings.get_filtered(user_id=user_id)
