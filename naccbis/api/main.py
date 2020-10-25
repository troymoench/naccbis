from typing import List, Optional

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import queries, schemas
from .database import SessionLocal
from naccbis import __version__


app = FastAPI(version=__version__)


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


@app.get("/team_offense", response_model=List[schemas.TeamOffenseSchema])
def read_team_offense(
    season: Optional[int] = None,
    team: Optional[str] = None,
    split: str = "overall",
    db: Session = Depends(get_db)
):
    df = queries.get_team_offense(db, season, team, split)
    return [row for row in df.itertuples(index=False)]


@app.get("/team_pitching", response_model=List[schemas.TeamPitchingSchema])
def read_team_pitching(
    season: Optional[int] = None,
    team: Optional[str] = None,
    split: str = "overall",
    db: Session = Depends(get_db)
):
    df = queries.get_team_pitching(db, season, team, split)
    return [row for row in df.itertuples(index=False)]


@app.get("/league_offense", response_model=List[schemas.LeagueOffenseSchema])
def read_league_offense(
    season: Optional[int] = None,
    split: str = "overall",
    db: Session = Depends(get_db)
):
    df = queries.get_league_offense(db, season, split)
    return [row for row in df.itertuples(index=False)]


@app.get("/league_pitching", response_model=List[schemas.LeaguePitchingSchema])
def read_league_pitching(
    season: Optional[int] = None,
    split: str = "overall",
    db: Session = Depends(get_db)
):
    df = queries.get_league_pitching(db, season, split)
    return [row for row in df.itertuples(index=False)]


@app.get("/player/{player_id}", response_model=schemas.PlayerSchema)
def read_player(player_id: str, db: Session = Depends(get_db)):
    off = queries.get_player_offense(db, player_id)
    off_totals = queries.get_player_career_offense(db, player_id)
    pitch = queries.get_player_pitching(db, player_id)
    pitch_totals = queries.get_player_career_pitching(db, player_id)

    return {
        "offense": [value for _, value in off.iterrows()],
        "offense_career": [value for _, value in off_totals.iterrows()],
        "pitching": [value for _, value in pitch.iterrows()],
        "pitching_career": [value for _, value in pitch_totals.iterrows()],
    }
