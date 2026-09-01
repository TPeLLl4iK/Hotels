from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingsAdd, BookingsAddRequest

router = APIRouter(prefix='/bookings', tags=['Бронирования'])

@router.post('', summary='Созданть бронирование')
async def add_booking(
    booking_data: BookingsAddRequest, 
    db: DBDep,
    user_id: UserIdDep
):


    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingsAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )

    await db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
    booking = await db.bookings.add(_booking_data)
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
