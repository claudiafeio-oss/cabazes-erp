from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationOut


router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("", response_model=list[LocationOut])
def list_locations(db: Session = Depends(get_db)) -> list[Location]:
    return list(db.execute(select(Location)).scalars())


@router.post("", response_model=LocationOut)
def create_location(payload: LocationCreate, db: Session = Depends(get_db)) -> Location:
    location = Location(**payload.model_dump())
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


@router.get("/{location_id}", response_model=LocationOut)
def get_location(location_id: int, db: Session = Depends(get_db)) -> Location:
    location = db.get(Location, location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="location not found")
    return location
