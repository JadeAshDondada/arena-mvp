from fastapi import FastAPI
from api.battle_router import router as battle_router
from api.character_router import router as character_router
from database import  Base, engine
from models.fighterDB import FighterDB
from models.battle_session import BattleSession  # важно импортнуть модель, чтобы она зарегистрировалась в Base

app = FastAPI(title="Arena API")

app.include_router(battle_router)
app.include_router(character_router)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )