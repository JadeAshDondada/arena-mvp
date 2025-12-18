from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from database import Base   # если Base лежит в models/__init__.py или database.py — подстрой под себя


class BattleSession(Base):
    __tablename__ = "battle_sessions"

    id = Column(Integer, primary_key=True, index=True)

    # ССЫЛКИ на бойцов
    fighter1_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)
    fighter2_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)

    # ТЕКУЩИЕ статы (меняются в бою)
    fighter1_hp = Column(Integer, nullable=False)
    fighter2_hp = Column(Integer, nullable=False)
    fighter1_attack = Column(Integer, nullable=False)
    fighter2_attack = Column(Integer, nullable=False)

    finished = Column(Boolean, default=False)
    winner_name = Column(String, nullable=True)
    current_turn= Column(String, nullable=False)

    created_at = Column(DateTime, default=func.now())

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )