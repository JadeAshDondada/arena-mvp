from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models.fighterDB import FighterDB

class FighterService:
    @staticmethod
    def create_fighter(
            name: str ,
            max_hp: int,
            max_attack: int,
            db: Session = Depends(get_db)
    ):
        fighter = FighterDB(
            name=name,
            max_hp=max_hp,
            cur_hp=max_hp,
            max_attack=max_attack,
            cur_attack=max_attack,
        )

        db.add(fighter)
        db.commit()
        db.refresh(fighter)
        return fighter


