from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.assembly_order import AssemblyOrder
from app.schemas.assembly import (
    AssemblyConsumptionCreate,
    AssemblyOrderCreate,
    AssemblyOrderOut,
    AssemblyOutputCreate,
)
from app.services.assembly_service import (
    complete_assembly_order,
    confirm_assembly_order,
    create_assembly_order,
    record_assembly_consumption,
)


router = APIRouter(prefix="/assemblies", tags=["assemblies"])


@router.get("", response_model=list[AssemblyOrderOut])
def list_assemblies(db: Session = Depends(get_db)) -> list[AssemblyOrder]:
    return list(db.execute(select(AssemblyOrder)).scalars())


@router.post("", response_model=AssemblyOrderOut)
def create_assembly(
    payload: AssemblyOrderCreate, db: Session = Depends(get_db)
) -> AssemblyOrder:
    order = create_assembly_order(
        db,
        basket_product_id=payload.basket_product_id,
        planned_quantity=payload.planned_quantity,
        basket_bom_id=payload.basket_bom_id,
    )
    db.commit()
    db.refresh(order)
    return order


@router.post("/{order_id}/confirm", response_model=AssemblyOrderOut)
def confirm_assembly(order_id: int, db: Session = Depends(get_db)) -> AssemblyOrder:
    order = confirm_assembly_order(db, order_id)
    db.commit()
    db.refresh(order)
    return order


@router.post("/{order_id}/consumption", response_model=dict)
def add_consumption(
    order_id: int,
    location_id: int,
    payload: list[AssemblyConsumptionCreate],
    db: Session = Depends(get_db),
) -> dict:
    record_assembly_consumption(
        db,
        assembly_order_id=order_id,
        location_id=location_id,
        consumptions=[item.model_dump() for item in payload],
    )
    db.commit()
    return {"status": "ok"}


@router.post("/{order_id}/complete", response_model=dict)
def complete_assembly(
    order_id: int,
    payload: AssemblyOutputCreate,
    db: Session = Depends(get_db),
) -> dict:
    complete_assembly_order(
        db,
        assembly_order_id=order_id,
        location_id=payload.location_id,
        quantity_produced=payload.quantity_produced,
        lot_code=payload.lot_code,
        expiry_date=payload.expiry_date,
    )
    db.commit()
    return {"status": "ok"}
