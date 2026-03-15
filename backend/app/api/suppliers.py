from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierOut


router = APIRouter(prefix="/suppliers", tags=["suppliers"])


@router.get("", response_model=list[SupplierOut])
def list_suppliers(db: Session = Depends(get_db)) -> list[Supplier]:
    return list(db.execute(select(Supplier)).scalars())


@router.post("", response_model=SupplierOut)
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db)) -> Supplier:
    supplier = Supplier(**payload.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


@router.get("/{supplier_id}", response_model=SupplierOut)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)) -> Supplier:
    supplier = db.get(Supplier, supplier_id)
    if supplier is None:
        raise HTTPException(status_code=404, detail="supplier not found")
    return supplier
