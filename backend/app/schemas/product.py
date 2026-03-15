from pydantic import BaseModel


class ProductCreate(BaseModel):
    sku: str
    name: str
    product_type: str
    unit_of_measure: str
    active: bool = True
    track_lot: bool = False
    track_expiry: bool = False
    minimum_stock: float = 0
    default_cost: float = 0


class ProductUpdate(BaseModel):
    name: str | None = None
    active: bool | None = None
    track_lot: bool | None = None
    track_expiry: bool | None = None
    minimum_stock: float | None = None
    default_cost: float | None = None


class ProductOut(ProductCreate):
    id: int
