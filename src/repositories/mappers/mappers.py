from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Bookings
from src.schemas.facilities import Facilities, RoomsFacilities
from src.schemas.hotels import Hotels
from src.schemas.rooms import Rooms, RoomsWithRels
from src.schemas.users import Users, UsersWithHashedPass


class HotelsDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotels


class RoomsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Rooms


class RoomsDataWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomsWithRels


class UsersDataMapper(DataMapper):
    db_model = UsersOrm
    schema = Users


class UsersDataMapperWithHashedPass(DataMapper):
    db_model = UsersOrm
    schema = UsersWithHashedPass


class BookingsDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Bookings


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facilities


class RoomsFacilitiesDataMapper(DataMapper):
    db_model = RoomsFacilitiesOrm
    schema = RoomsFacilities
