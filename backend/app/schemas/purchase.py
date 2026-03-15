from datetime import date

from pydantic import BaseModel


class PurchaseOrderLineCreate(BaseModel):
    product_id: int
    quantity_ordered: float
    unit_cost: float | None = None


class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    lines: list[PurchaseOrderLineCreate]


class PurchaseOrderOut(BaseModel):
    id: int
    supplier_id: int
    status: str


class PurchaseReceiptLineCreate(BaseModel):
    product_id: int
    location_id: int
    quantity: float
    lot_code: str | None = None
    lot_id: int | None = None
    expiry_date: date | None = None
    unit_cost: float | None = None


class PurchaseReceiptCreate(BaseModel):
    lines: list[PurchaseReceiptLineCreate]


class PurchaseReceiptOut(BaseModel):
    id: int
    purchase_order_id: int
    status: str
