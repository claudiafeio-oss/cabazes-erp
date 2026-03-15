from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.purchase_order import PurchaseOrder
from app.schemas.purchase import (
    PurchaseOrderCreate,
    PurchaseOrderOut,
    PurchaseReceiptCreate,
    PurchaseReceiptOut,
)
from app.services.purchase_service import (
    confirm_purchase_order,
    create_purchase_order as create_purchase_order_service,
    receive_purchase_order,
)


router = APIRouter(prefix="/purchase-orders", tags=["purchases"])


@router.get("", response_model=list[PurchaseOrderOut])
def list_purchase_orders(db: Session = Depends(get_db)) -> list[PurchaseOrder]:
    return list(db.execute(select(PurchaseOrder)).scalars())


@router.post("", response_model=PurchaseOrderOut)
def create_purchase_order(
    payload: PurchaseOrderCreate, db: Session = Depends(get_db)
) -> PurchaseOrder:
    order = create_purchase_order_service(
        db, payload.supplier_id, [line.model_dump() for line in payload.lines]
    )
    db.commit()
    db.refresh(order)
    return order


@router.get("/{order_id}", response_model=PurchaseOrderOut)
def get_purchase_order(order_id: int, db: Session = Depends(get_db)) -> PurchaseOrder:
    order = db.get(PurchaseOrder, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="purchase order not found")
    return order


@router.post("/{order_id}/confirm", response_model=PurchaseOrderOut)
def confirm_order(order_id: int, db: Session = Depends(get_db)) -> PurchaseOrder:
    order = confirm_purchase_order(db, order_id)
    db.commit()
    db.refresh(order)
    return order


@router.post("/{order_id}/receive", response_model=PurchaseReceiptOut)
def receive_order(
    order_id: int, payload: PurchaseReceiptCreate, db: Session = Depends(get_db)
) -> PurchaseReceiptOut:
    receipt = receive_purchase_order(db, order_id, [line.model_dump() for line in payload.lines])
    db.commit()
    db.refresh(receipt)
    return PurchaseReceiptOut(
        id=receipt.id, purchase_order_id=receipt.purchase_order_id, status=receipt.status
    )
