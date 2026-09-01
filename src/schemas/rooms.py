from pydantic import BaseModel, ConfigDict, Field

from src.schemas.facilities import Facilities


class RoomsAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] | None = []

class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int

class Rooms(RoomsAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class RoomsWithRels(Rooms):
    facilities: list[Facilities]


class RoomsPatchRequest(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    facilities_ids: list[int] | None = []


class RoomsPatch(BaseModel):
    hotel_id: int | None = Field(None) 
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
