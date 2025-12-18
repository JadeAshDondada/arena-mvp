from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class FighterDB(Base):
    __tablename__ = "fighters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40), index=True, nullable=False)  # убрал unique=True
    max_hp = Column(Integer, nullable=False)
    cur_hp = Column(Integer, nullable=False)
    max_attack = Column(Integer, nullable=False)
    cur_attack = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())