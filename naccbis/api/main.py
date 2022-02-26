from datetime import date
from typing import Optional, Iterator

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import queries, schemas
from .database import SessionLocal
from naccbis import __version__
from naccbis.common import metrics


app = FastAPI(version=__version__)


# Dependency
def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/ping")
def ping():
    return "pong"


@app.get("/batters/", response_model=list[schemas.BattersSchema])
def read_batters(
    season: Optional[int] = None,
    team: Optional[str] = None,
    split: str = "overall",
    min_pa: int = 0,
    db: Session = Depends(get_db),
):
    batters = queries.get_batters(db, season, team, split, min_pa)
    totals = queries.get_league_offense(db, season, split)
    df = metrics.multi_season(batters, totals, metrics.season_offensive_metrics_rar)
    return [row for row in df.itertuples(index=False)]


@app.get("/pitchers/", response_model=list[schemas.PitchersSchema])
def read_pitchers(
    season: Optional[int] = None,
    team: Optional[str] = None,
    split: str = "overall",
    min_ip: int = 0,
    db: Session = Depends(get_db),
):
    return queries.get_pitchers(db, season, team, split, min_ip)


@app.get("/team_offense", response_model=list[schemas.TeamOffenseSchema])
def read_team_offense(
    season: Optional[int] = None,
    team: Optional[str] = None,
    split: str = "overall",
    db: Session = Depends(get_db),
):
    teams = queries.get_team_offense(db, season, team, split)
    totals = queries.get_league_offense(db, season, split)
    df = metrics.multi_season(teams, totals, metrics.season_offensive_metrics_rar)
    return [row for row in df.itertuples(index=False)]


@app.get("/team_pitching", response_model=list[schemas.TeamPitchingSchema])
def read_team_pitching(
    season: Optional[int] = None,
    team: Optional[str] = None,
    split: str = "overall",
    db: Session = Depends(get_db),
):
    df = queries.get_team_pitching(db, season, team, split)
    return [row for row in df.itertuples(index=False)]


@app.get("/league_offense", response_model=list[schemas.LeagueOffenseSchema])
def read_league_offense(
    season: Optional[int] = None, split: str = "overall", db: Session = Depends(get_db)
):
    df = queries.get_league_offense(db, season, split)
    return [row for row in df.itertuples(index=False)]


@app.get("/league_pitching", response_model=list[schemas.LeaguePitchingSchema])
def read_league_pitching(
    season: Optional[int] = None, split: str = "overall", db: Session = Depends(get_db)
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


@app.get("/game_log/", response_model=list[schemas.GameLogSchema])
def read_game_log(
    team: Optional[str] = None,
    season: Optional[int] = None,
    game_date: Optional[date] = None,
    home: Optional[bool] = None,
    split: str = "overall",
    db: Session = Depends(get_db),
):
    return queries.get_game_log(db, team, season, game_date, home)
