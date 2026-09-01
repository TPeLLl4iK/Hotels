from pydantic import BaseModel, Field


class HotelsAdd(BaseModel):
    title: str
    location: str


class Hotels(HotelsAdd):
    id: int


class HotelsPATCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
