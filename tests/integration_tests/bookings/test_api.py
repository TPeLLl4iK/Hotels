import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2026-09-03", "2026-09-24", 200),
        (1, "2026-09-04", "2026-09-23", 200),
        (1, "2026-09-05", "2026-09-25", 200),
        (1, "2026-09-06", "2026-09-29", 200),
        (1, "2026-09-03", "2026-09-27", 200),
        (1, "2026-09-10", "2026-09-28", 500),
    ],
)
async def test_add_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    db,
    authenticated_ac,
):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    print(response)

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "Added"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_all_booking():
    async for deleting_db in get_db_null_pool():
        await deleting_db.bookings.delete()
        await deleting_db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, cnt_booked_room",
    [
        (1, "2026-09-03", "2026-09-24", 1),
        (1, "2026-09-03", "2026-09-24", 2),
        (1, "2026-09-03", "2026-09-24", 3),
    ],
)
async def test_add_and_get_bookings(
    room_id,
    date_from,
    date_to,
    cnt_booked_room,
    delete_all_booking,
    authenticated_ac,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == 200

    resposne_my_bookings = await authenticated_ac.get(
        '/bookings/me'
    )

    print(resposne_my_bookings.json())
    assert resposne_my_bookings.status_code == 200
    assert len(resposne_my_bookings.json()) == cnt_booked_room
