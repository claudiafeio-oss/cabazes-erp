from pydantic import BaseModel


class AssemblyOrderCreate(BaseModel):
    basket_product_id: int
    planned_quantity: float
    basket_bom_id: int | None = None


class AssemblyConsumptionCreate(BaseModel):
    product_id: int
    quantity: float
    lot_id: int | None = None
    planned_product_id: int | None = None
    substitution_group_id: int | None = None


class AssemblyOutputCreate(BaseModel):
    quantity_produced: float
    location_id: int
    lot_code: str
    expiry_date: str | None = None


class AssemblyOrderOut(BaseModel):
    id: int
    basket_product_id: int
    status: str
