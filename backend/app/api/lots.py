from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.lot import Lot
from app.schemas.lot import LotCreate, LotOut


router = APIRouter(prefix="/lots", tags=["lots"])


@router.get("", response_model=list[LotOut])
def list_lots(db: Session = Depends(get_db)) -> list[Lot]:
    return list(db.execute(select(Lot)).scalars())


@router.post("", response_model=LotOut)
def create_lot(payload: LotCreate, db: Session = Depends(get_db)) -> Lot:
    lot = Lot(**payload.model_dump())
    db.add(lot)
    db.commit()
    db.refresh(lot)
    return lot


@router.get("/{lot_id}", response_model=LotOut)
def get_lot(lot_id: int, db: Session = Depends(get_db)) -> Lot:
    lot = db.get(Lot, lot_id)
    if lot is None:
        raise HTTPException(status_code=404, detail="lot not found")
    return lot
