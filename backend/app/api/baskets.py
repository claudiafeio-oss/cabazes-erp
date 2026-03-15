from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.basket_bom import BasketBom
from app.models.basket_bom_line import BasketBomLine
from app.models.substitution_group import SubstitutionGroup
from app.models.substitution_group_item import SubstitutionGroupItem
from app.schemas.basket import (
    BasketBomCreate,
    BasketBomOut,
    SubstitutionGroupCreate,
    SubstitutionGroupOut,
)


router = APIRouter(prefix="/baskets", tags=["baskets"])


@router.get("", response_model=list[BasketBomOut])
def list_boms(db: Session = Depends(get_db)) -> list[BasketBom]:
    return list(db.execute(select(BasketBom)).scalars())


@router.post("", response_model=BasketBomOut)
def create_bom(payload: BasketBomCreate, db: Session = Depends(get_db)) -> BasketBom:
    bom = BasketBom(
        basket_product_id=payload.basket_product_id,
        version=payload.version,
        active=payload.active,
    )
    db.add(bom)
    db.flush()
    for line in payload.lines:
        db.add(
            BasketBomLine(
                basket_bom_id=bom.id,
                component_product_id=line.component_product_id,
                quantity=line.quantity,
                substitution_group_id=line.substitution_group_id,
            )
        )
    db.commit()
    db.refresh(bom)
    return bom


@router.get("/{bom_id}", response_model=BasketBomOut)
def get_bom(bom_id: int, db: Session = Depends(get_db)) -> BasketBom:
    bom = db.get(BasketBom, bom_id)
    if bom is None:
        raise HTTPException(status_code=404, detail="bom not found")
    return bom


@router.post("/substitution-groups", response_model=SubstitutionGroupOut)
def create_substitution_group(
    payload: SubstitutionGroupCreate, db: Session = Depends(get_db)
) -> SubstitutionGroupOut:
    group = SubstitutionGroup(name=payload.name, active=True)
    db.add(group)
    db.flush()
    for item in payload.items:
        db.add(
            SubstitutionGroupItem(
                substitution_group_id=group.id, product_id=item.product_id
            )
        )
    db.commit()
    return SubstitutionGroupOut(id=group.id, name=group.name)
