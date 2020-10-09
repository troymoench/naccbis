from typing import List, Optional

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import queries, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/ping")
def ping():
    return "pong"


@app.get("/batters/", response_model=List[schemas.BattersSchema])
def read_batters(
    season: Optional[int] = None,
    team: Optional[str] = None,
    split: str = "overall",
    min_pa: int = 0,
    db: Session = Depends(get_db)
):
    return queries.get_batters(db, season, team, split, min_pa)


@app.get("/pitchers/", response_model=List[schemas.PitchersSchema])
def read_pitchers(
    season: Optional[int] = None,
    team: Optional[str] = None,
    split: str = "overall",
    min_ip: int = 0,
    db: Session = Depends(get_db)
):
    return queries.get_pitchers(db, season, team, split, min_ip)
