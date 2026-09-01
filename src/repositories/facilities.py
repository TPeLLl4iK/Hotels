from sqlalchemy import delete, insert, select

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import (
    FacilitiesDataMapper,
    RoomsFacilitiesDataMapper,
)


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilitiesDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    mapper = RoomsFacilitiesDataMapper

    async def set_rooms_facilities(self, room_id, facilities_ids: list[int]):
        facilites_list = (
            select(RoomsFacilitiesOrm.facility_id)
            .filter_by(room_id=room_id)
        )

        result = await self.session.execute(facilites_list)
        current_facilities_ids: list[int] = result.scalars().all()

        ids_to_delete = list(set(current_facilities_ids) - set(facilities_ids))

        ids_to_add = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_delete:
            delete_m2m_facilities = (
            delete(RoomsFacilitiesOrm)
            .filter(
                RoomsFacilitiesOrm.room_id == room_id, 
                RoomsFacilitiesOrm.facility_id.in_(ids_to_delete)
            )
        )
            await self.session.execute(delete_m2m_facilities)

        if ids_to_add:
            add_m2m_facilities = (
            insert(RoomsFacilitiesOrm)
            .values([{'room_id': room_id, 'facility_id': f_id} for f_id in ids_to_add])
        )
            await self.session.execute(add_m2m_facilities)
