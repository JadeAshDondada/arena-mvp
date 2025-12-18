from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models.fighterDB import FighterDB
from services.Fighters.fighter_service import FighterService

router = APIRouter(prefix="/characters", tags=["characters"])

#Проверка валидности имени, хп и атаки
def name_param():
    return Query(
        ...,
        min_length=2,
        max_length=40,
        regex=r"^[a-zA-ZА-Яа-я0-9]+(?:\s+[a-zA-ZА-Яа-я0-9]{2,})*$"
    )

def hp_param():
    return Query(..., ge=1, le=1000)

def attack_param():
    return Query(..., ge=1, le=1000)

@router.post("/create/fighter")
def create_fighter(
        name: str = name_param(),
        hp: int = hp_param(),
        attack: int = attack_param(),
        db: Session = Depends(get_db)
):
    fighter = FighterService.create_fighter(name, hp, attack, db)

    return {
        "status": "ok",
        "massage": f"Боец {name} создан",
        "fighter": {"id": fighter.id,
                    "name": fighter.name,
                    "hp": fighter.max_hp,
                    "attack": fighter.max_attack}
    }

