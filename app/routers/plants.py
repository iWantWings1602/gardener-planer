from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Plant
from app.schemas import PlantCreate, PlantOut, PlantUpdate

router = APIRouter(prefix="/plants", tags=["plants"])

def get_plant_or_404(plant_id: int, db: Session) -> Plant:
    plant = db.get(Plant, plant_id)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant


@router.get("", response_model=list[PlantOut])
def list_plants(
    city: str | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    query = select(Plant)
    if city is not None:
        query = query.where(Plant.city == city)
    query = query.order_by(Plant.id).limit(limit).offset(offset)
    return db.scalars(query).all()


@router.get("/{plant_id}", response_model=PlantOut)
def get_plant(plant_id: int, db: Session = Depends(get_db)):
    return get_plant_or_404(plant_id, db)


@router.post("", response_model=PlantOut, status_code=201)
def create_plant(data: PlantCreate, db: Session = Depends(get_db)):
    plant = Plant(**data.model_dump())
    db.add(plant)
    db.commit()
    db.refresh(plant)
    return plant


@router.patch("/{plant_id}", response_model=PlantOut)
def update_plant(plant_id: int, data: PlantUpdate, db: Session = Depends(get_db)):
    plant = get_plant_or_404(plant_id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(plant, field, value)
    db.commit()
    db.refresh(plant)
    return plant


@router.delete("/{plant_id}", status_code=204)
def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = get_plant_or_404(plant_id, db)
    db.delete(plant)
    db.commit()
    return Response(status_code=204)
