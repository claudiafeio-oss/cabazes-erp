from datetime import date

from pydantic import BaseModel


class LotCreate(BaseModel):
    product_id: int
    lot_code: str
    expiry_date: date | None = None


class LotOut(LotCreate):
    id: int
