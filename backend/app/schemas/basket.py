from pydantic import BaseModel


class BasketBomLineCreate(BaseModel):
    component_product_id: int
    quantity: float
    substitution_group_id: int | None = None


class BasketBomCreate(BaseModel):
    basket_product_id: int
    version: str = "v1"
    active: bool = True
    lines: list[BasketBomLineCreate]


class BasketBomOut(BaseModel):
    id: int
    basket_product_id: int
    version: str
    active: bool


class SubstitutionGroupItemCreate(BaseModel):
    product_id: int


class SubstitutionGroupCreate(BaseModel):
    name: str
    items: list[SubstitutionGroupItemCreate]


class SubstitutionGroupOut(BaseModel):
    id: int
    name: str
