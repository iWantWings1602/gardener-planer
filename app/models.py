from datetime import date
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Plant(Base):
    __tablename__ = "plants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))
    watering_interval: Mapped[int]
    planted_at: Mapped[date]
    is_indoor: Mapped[bool] = mapped_column(default=False)  # п'яте поле типу bool
