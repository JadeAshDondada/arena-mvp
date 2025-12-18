from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from services.battle.battle_service import *
from models.fighterDB import FighterDB

router = APIRouter(prefix="/battle", tags=["battle"])

#Валидатор id
def fighter_id_param():
    return Query(..., ge=1)

@router.post("/start")
def start_battle(
        fighter1_id: int = fighter_id_param(),
        fighter2_id: int = fighter_id_param(),
        db: Session = Depends(get_db)):
        session = create_battle(db, fighter1_id, fighter2_id)
        fighter1 = db.query(FighterDB).get(fighter1_id)
        fighter2 = db.query(FighterDB).get(fighter2_id)
        return {
        "status": "ok",
        "massage": f"Битва {session.id} началась!",
        "fighter1": {"id": fighter1.id,"name": fighter1.name, "hp": fighter1.max_hp, "attack": fighter1.max_attack},
        "fighter2": {"id": fighter2.id,"name": fighter2.name, "hp": fighter2.max_hp, "attack": fighter2.max_attack},
    }

@router.post("/turn")
def battle_turn(battle_id: int, db: Session = Depends(get_db)):
    return make_turn(db, battle_id)


@router.get("/state")
def state(battle_id: int, db: Session = Depends(get_db)):
    return get_state(db, battle_id)