from sqlalchemy import select

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import (
    UsersDataMapper,
    UsersDataMapperWithHashedPass,
)


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UsersDataMapper

    async def get_user_with_hashed_pass(self, login: str):
        query = select(self.model).filter_by(login=login)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UsersDataMapperWithHashedPass.map_to_domain_entity(model)
