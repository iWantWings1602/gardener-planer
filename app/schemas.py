from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class PlantCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    watering_interval: int = Field(ge=1, le=365)
    planted_at: date
    is_indoor: bool = Field(default=False)


class PlantUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    city: str | None = Field(default=None, min_length=1, max_length=100)
    watering_interval: int | None = Field(default=None, ge=1, le=365)
    planted_at: date | None = None
    is_indoor: bool | None = None


class PlantOut(PlantCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
