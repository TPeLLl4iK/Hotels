from src.schemas.hotels import HotelsAdd


async def test_add_hotel(db):
    hotel_data = HotelsAdd(title="Hotel 1", location="Сочи-стар")
    await db.hotels.add(hotel_data)
    await db.commit()
