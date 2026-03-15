from pydantic import BaseModel


class SupplierCreate(BaseModel):
    code: str
    name: str
    active: bool = True


class SupplierOut(SupplierCreate):
    id: int
