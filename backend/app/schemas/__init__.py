from app.schemas.assembly import (
    AssemblyConsumptionCreate,
    AssemblyOrderCreate,
    AssemblyOutputCreate,
    AssemblyOrderOut,
)
from app.schemas.auth import LoginRequest, Token
from app.schemas.basket import (
    BasketBomCreate,
    BasketBomOut,
    SubstitutionGroupCreate,
    SubstitutionGroupOut,
)
from app.schemas.inventory import InventoryAdjustmentCreate, InventoryAdjustmentOut
from app.schemas.location import LocationCreate, LocationOut
from app.schemas.lot import LotCreate, LotOut
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.schemas.purchase import (
    PurchaseOrderCreate,
    PurchaseOrderOut,
    PurchaseReceiptCreate,
    PurchaseReceiptOut,
)
from app.schemas.stock import StockBalanceOut, StockMoveOut
from app.schemas.supplier import SupplierCreate, SupplierOut

__all__ = [
    "AssemblyConsumptionCreate",
    "AssemblyOrderCreate",
    "AssemblyOrderOut",
    "AssemblyOutputCreate",
    "BasketBomCreate",
    "BasketBomOut",
    "SubstitutionGroupCreate",
    "SubstitutionGroupOut",
    "InventoryAdjustmentCreate",
    "InventoryAdjustmentOut",
    "LocationCreate",
    "LocationOut",
    "LoginRequest",
    "LotCreate",
    "LotOut",
    "ProductCreate",
    "ProductOut",
    "ProductUpdate",
    "PurchaseOrderCreate",
    "PurchaseOrderOut",
    "PurchaseReceiptCreate",
    "PurchaseReceiptOut",
    "StockBalanceOut",
    "StockMoveOut",
    "SupplierCreate",
    "SupplierOut",
    "Token",
]
