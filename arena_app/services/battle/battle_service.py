from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.battle_session import BattleSession
from models.fighterDB import FighterDB

def get_fighter(db: Session, fighter_id: int):
    fighter = db.query(FighterDB).filter(FighterDB.id == fighter_id).first()
    if not fighter:
        raise HTTPException(status_code=404, detail=f"Боец с ID {fighter_id} не найден")
    return fighter


def create_battle(
        db: Session,
        fighter1_id: int,
        fighter2_id: int
) -> BattleSession:

    fighter1 = get_fighter(db, fighter1_id)
    fighter2 = get_fighter(db, fighter2_id)
    # Проверяем разные ID

    if fighter1_id == fighter2_id:
        raise HTTPException(status_code=400, detail="Нельзя создать бой из двух одинаковых бойцов")

    #Создаем битву
    session = BattleSession(
        fighter1_id=fighter1_id,
        fighter2_id=fighter2_id,
        fighter1_hp=fighter1.max_hp,
        fighter2_hp=fighter2.max_hp,
        fighter1_attack=fighter1.max_attack,
        fighter2_attack=fighter2.max_attack,
        current_turn="fighter1",
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def make_turn(db: Session, battle_id: int) -> dict:
    session = db.query(BattleSession).filter(BattleSession.id == battle_id).first()
    if not session:
        raise HTTPException(status_code=400, detail="Битва с таким id не найдена")

    if session.finished:
        return {
            "status": "ok",
            "massage": "Битва уже завершена",
            "attacker": None,
            "defender": None,
            "f1_hp": session.fighter1_hp,
            "f2_hp": session.fighter2_hp,
            "finished": True,
            "winner": session.winner_name,
        }

    fighter1 = db.query(FighterDB).get(session.fighter1_id)
    fighter2 = db.query(FighterDB).get(session.fighter2_id)
    attacker_name = fighter1.name if session.current_turn == "fighter1" else fighter2.name
    defender_name = fighter2.name if session.current_turn == "fighter1" else fighter1.name

    # Определяем, кто ходит и какие статы трогаем
    if session.current_turn == "fighter1":
        session.fighter1_attack = max(1, session.fighter1_attack)
        attack = session.fighter1_attack
        session.fighter2_hp = max(0, session.fighter2_hp - attack)
    else:
        session.fighter2_attack = max(1, session.fighter2_attack)
        attack = session.fighter2_attack
        session.fighter1_hp = max(0, session.fighter1_hp - attack)

    # Проверяем, не умер ли защитник
    if session.fighter1_hp <= 0 or session.fighter2_hp <= 0:
        session.finished = True
        session.winner_name = attacker_name
        message = "Битва окончена"
    else:
        session.current_turn = "fighter2" if session.current_turn == "fighter1" else "fighter1"
        message = "Ход сделан"

    db.commit()
    db.refresh(session)

    return {
        "status": "ok",
        "massage": message,
        "attacker": attacker_name,
        "defender": defender_name,
        "f1_hp": session.fighter1_hp,
        "f2_hp": session.fighter2_hp,
        "f1_attack": session.fighter1_attack,
        "f2_attack": session.fighter2_attack,
        "finished": session.finished,
        "winner": session.winner_name,
    }

def get_state(db: Session, battle_id: int) -> dict:
    session = db.query(BattleSession).filter(BattleSession.id == battle_id).first()
    if not session:
        raise HTTPException(status_code=400, detail="Битва с таким id не найдена")

    fighter1 = db.query(FighterDB).get(session.fighter1_id)
    fighter2 = db.query(FighterDB).get(session.fighter2_id)
    attacker_name = fighter1.name if session.current_turn == "fighter1" else fighter2.name
    defender_name = fighter2.name if session.current_turn == "fighter1" else fighter1.name

    if session.finished:
        return {
            "status": "ok",
            "massage": "Битва уже завершена",
            "attacker": None,
            "defender": None,
            "f1_hp": session.fighter1_hp,
            "f2_hp": session.fighter2_hp,
            "finished": True,
            "winner": session.winner_name,
        }
    else:
        return {
            "status": "ok",
            "massage": "Битва еще продолжается",
            "attacker": attacker_name,
            "defender": defender_name,
            "f1_hp": session.fighter1_hp,
            "f2_hp": session.fighter2_hp,
            "f1_attack": session.fighter1_attack,
            "f2_attack": session.fighter2_attack,
            "finished": session.finished,
            "winner": session.winner_name,
        }