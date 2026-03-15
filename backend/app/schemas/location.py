from pydantic import BaseModel


class LocationCreate(BaseModel):
    code: str
    name: str
    active: bool = True


class LocationOut(LocationCreate):
    id: int
