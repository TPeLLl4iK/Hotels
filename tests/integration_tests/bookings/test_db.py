from datetime import date

from src.schemas.bookings import BookingsAdd


async def test_booking(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingsAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=9, day=29),
        date_to=date(year=2026, month=9, day=2),
        price=1000,
    )

    new_booking = await db.bookings.add(booking_data)

    got_booking_data = await db.bookings.get_one_or_none(id=new_booking.id)
    assert got_booking_data
    assert got_booking_data.user_id == new_booking.user_id
    assert got_booking_data.room_id == new_booking.room_id

    updated_booking_data = BookingsAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=9, day=29),
        date_to=date(year=2026, month=9, day=2),
        price=2000,
    )

    await db.bookings.edit(updated_booking_data, id=new_booking.id)
    edited_booking_data = await db.bookings.get_one_or_none(id=new_booking.id)

    assert edited_booking_data
    assert edited_booking_data.price == updated_booking_data.price

    await db.bookings.delete(id=new_booking.id)

    got_booking_data = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not got_booking_data
