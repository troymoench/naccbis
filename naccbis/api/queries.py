from typing import Optional
from sqlalchemy.orm import Session

from .models import (
    BattersOverall,
    BattersConference,
    PitchersOverall,
    PitchersConference,
)


def get_batters(
    db: Session,
    season: Optional[int] = None,
    team: Optional[str] = None,
    split: str = "overall",
    min_pa: int = 0
):
    if split == "overall":
        table = BattersOverall
    else:
        table = BattersConference

    q = db.query(table)
    if season:
        q = q.filter(table.season == season)
    if team:
        q = q.filter(table.team == team)
    q = q.filter(table.pa >= min_pa)
    return q.all()


def get_pitchers(
    db: Session,
    season: Optional[int] = None,
    team: Optional[str] = None,
    split: str = "overall",
    min_ip: int = 0
):
    if split == "overall":
        table = PitchersOverall
    else:
        table = PitchersConference

    q = db.query(table)
    if season:
        q = q.filter(table.season == season)
    if team:
        q = q.filter(table.team == team)
    q = q.filter(table.ip >= min_ip)
    return q.all()
