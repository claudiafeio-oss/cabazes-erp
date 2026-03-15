from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.stock_balance import StockBalance
from app.models.stock_move import StockMove
from app.schemas.inventory import InventoryAdjustmentCreate, InventoryAdjustmentOut
from app.schemas.stock import StockBalanceOut, StockMoveOut
from app.services.inventory_service import apply_inventory_adjustment, create_inventory_adjustment


router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("/on-hand", response_model=list[StockBalanceOut])
def list_stock_on_hand(
    product_id: int | None = None,
    location_id: int | None = None,
    db: Session = Depends(get_db),
) -> list[StockBalance]:
    query = select(StockBalance)
    if product_id is not None:
        query = query.where(StockBalance.product_id == product_id)
    if location_id is not None:
        query = query.where(StockBalance.location_id == location_id)
    return list(db.execute(query).scalars())


@router.get("/movements", response_model=list[StockMoveOut])
def list_stock_movements(
    product_id: int | None = None,
    location_id: int | None = None,
    db: Session = Depends(get_db),
) -> list[StockMove]:
    query = select(StockMove)
    if product_id is not None:
        query = query.where(StockMove.product_id == product_id)
    if location_id is not None:
        query = query.where(StockMove.location_id == location_id)
    return list(db.execute(query).scalars())


@router.post("/adjustments", response_model=InventoryAdjustmentOut)
def create_adjustment(
    payload: InventoryAdjustmentCreate, db: Session = Depends(get_db)
) -> InventoryAdjustmentOut:
    adjustment = create_inventory_adjustment(db, payload.location_id, payload.lines)
    db.commit()
    db.refresh(adjustment)
    return InventoryAdjustmentOut(
        id=adjustment.id, location_id=adjustment.location_id, status=adjustment.status
    )


@router.post("/adjustments/{adjustment_id}/apply", response_model=InventoryAdjustmentOut)
def apply_adjustment(adjustment_id: int, db: Session = Depends(get_db)) -> InventoryAdjustmentOut:
    adjustment = apply_inventory_adjustment(db, adjustment_id)
    db.commit()
    db.refresh(adjustment)
    return InventoryAdjustmentOut(
        id=adjustment.id, location_id=adjustment.location_id, status=adjustment.status
    )
