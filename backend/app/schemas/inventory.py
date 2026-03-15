from pydantic import BaseModel


class InventoryAdjustmentLineCreate(BaseModel):
    product_id: int
    lot_id: int | None = None
    quantity_counted: float
    quantity_system: float


class InventoryAdjustmentCreate(BaseModel):
    location_id: int
    lines: list[InventoryAdjustmentLineCreate]


class InventoryAdjustmentOut(BaseModel):
    id: int
    location_id: int
    status: str
