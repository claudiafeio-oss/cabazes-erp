from datetime import datetime

from pydantic import BaseModel


class StockBalanceOut(BaseModel):
    product_id: int
    location_id: int
    lot_id: int | None
    quantity: float


class StockMoveOut(BaseModel):
    id: int
    product_id: int
    location_id: int
    lot_id: int | None
    quantity: float
    move_type: str
    occurred_at: datetime
