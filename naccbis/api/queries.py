from datetime import date
from typing import Optional, Union

import pandas as pd
from sqlalchemy import func
from sqlalchemy.orm import Session, aliased

from naccbis.common import metrics
from naccbis.common.models import (
    BattersConference,
    BattersOverall,
    GameLog,
    LeagueOffenseConference,
    LeagueOffenseOverall,
    LeaguePitchingConference,
    LeaguePitchingOverall,
    PitchersConference,
    PitchersOverall,
    PlayerId,
    TeamOffenseConference,
    TeamOffenseOverall,
    TeamPitchingConference,
    TeamPitchingOverall,
)


def get_batters(
    db: Session,
    season: Optional[int] = None,
    team: Optional[str] = None,
    split: str = "overall",
    min_pa: int = 0,
):
    table: Union[type[BattersOverall], type[BattersConference]]
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
    return pd.read_sql_query(q.statement, q.session.connection())


def get_pitchers(
    db: Session,
    season: Optional[int] = None,
    team: Optional[str] = None,
    split: str = "overall",
    min_ip: int = 0,
):
    table: Union[type[PitchersOverall], type[PitchersConference]]
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
    return pd.read_sql_query(q.statement, q.session.connection())


def get_player_offense(db: Session, player_id: str):
    q = (
        db.query(BattersOverall)
        .select_from(BattersOverall)
        .join(PlayerId)
        .filter(PlayerId.player_id == player_id)
        .order_by(BattersOverall.season)
    )

    return pd.read_sql_query(q.statement, q.session.connection())


def get_player_career_offense(db: Session, player_id: str):
    b = aliased(BattersOverall)
    q = (
        db.query(
            func.sum(b.g).label("g"),
            func.sum(b.pa).label("pa"),
            func.sum(b.ab).label("ab"),
            func.sum(b.r).label("r"),
            func.sum(b.h).label("h"),
            func.sum(b.x2b).label("x2b"),
            func.sum(b.x3b).label("x3b"),
            func.sum(b.hr).label("hr"),
            func.sum(b.rbi).label("rbi"),
            func.sum(b.bb).label("bb"),
            func.sum(b.so).label("so"),
            func.sum(b.hbp).label("hbp"),
            func.sum(b.tb).label("tb"),
            func.sum(b.xbh).label("xbh"),
            func.sum(b.sf).label("sf"),
            func.sum(b.sh).label("sh"),
            func.sum(b.gdp).label("gdp"),
            func.sum(b.sb).label("sb"),
            func.sum(b.cs).label("cs"),
            func.sum(b.go).label("go"),
            func.sum(b.fo).label("fo"),
        )
        .select_from(b)
        .join(PlayerId)
        .filter(PlayerId.player_id == player_id)
    )

    df = pd.read_sql_query(q.statement, q.session.connection())
    return metrics.basic_offensive_metrics(df)


def get_player_pitching(db: Session, player_id: str):
    q = (
        db.query(PitchersOverall)
        .select_from(PitchersOverall)
        .join(PlayerId)
        .filter(PlayerId.player_id == player_id)
        .order_by(PitchersOverall.season)
    )

    return pd.read_sql_query(q.statement, q.session.connection())


def get_player_career_pitching(db: Session, player_id: str):
    p = aliased(PitchersOverall)
    q = (
        db.query(
            func.sum(p.g).label("g"),
            func.sum(p.gs).label("gs"),
            func.sum(p.w).label("w"),
            func.sum(p.l).label("l"),
            func.sum(p.sv).label("sv"),
            func.sum(p.cg).label("cg"),
            func.sum(p.sho).label("sho"),
            func.sum(p.ip).label("ip"),
            func.sum(p.h).label("h"),
            func.sum(p.r).label("r"),
            func.sum(p.er).label("er"),
            func.sum(p.bb).label("bb"),
            func.sum(p.so).label("so"),
            func.sum(p.x2b).label("x2b"),
            func.sum(p.x3b).label("x3b"),
            func.sum(p.hr).label("hr"),
            func.sum(p.ab).label("ab"),
            func.sum(p.wp).label("wp"),
            func.sum(p.hbp).label("hbp"),
            func.sum(p.bk).label("bk"),
            func.sum(p.sf).label("sf"),
            func.sum(p.sh).label("sh"),
            func.sum(p.pa).label("pa"),
        )
        .select_from(p)
        .join(PlayerId)
        .filter(PlayerId.player_id == player_id)
    )

    df = pd.read_sql_query(q.statement, q.session.connection())
    return metrics.basic_pitching_metrics(df)


def get_team_offense(
    db: Session,
    season: Optional[int] = None,
    team: Optional[str] = None,
    split: str = "overall",
):
    table: Union[type[TeamOffenseOverall], type[TeamOffenseConference]]
    if split == "overall":
        table = TeamOffenseOverall
    else:
        table = TeamOffenseConference

    q = db.query(table)
    if season:
        q = q.filter(table.season == season)
    if team:
        q = q.filter(table.name == team)
    q = q.order_by(table.season)
    return pd.read_sql_query(q.statement, q.session.connection())


def get_team_pitching(
    db: Session,
    season: Optional[int] = None,
    team: Optional[str] = None,
    split: str = "overall",
):
    table: Union[type[TeamPitchingOverall], type[TeamPitchingConference]]
    if split == "overall":
        table = TeamPitchingOverall
    else:
        table = TeamPitchingConference

    q = db.query(table)
    if season:
        q = q.filter(table.season == season)
    if team:
        q = q.filter(table.name == team)
    q = q.order_by(table.season)
    return pd.read_sql_query(q.statement, q.session.connection())


def get_league_offense(
    db: Session,
    season: Optional[int] = None,
    split: str = "overall",
):
    table: Union[type[LeagueOffenseOverall], type[LeagueOffenseConference]]
    if split == "overall":
        table = LeagueOffenseOverall
    else:
        table = LeagueOffenseConference

    q = db.query(table)
    if season:
        q = q.filter(table.season == season)
    q = q.order_by(table.season)
    return pd.read_sql_query(q.statement, q.session.connection())


def get_league_pitching(
    db: Session,
    season: Optional[int] = None,
    split: str = "overall",
):
    table: Union[type[LeaguePitchingOverall], type[LeaguePitchingConference]]
    if split == "overall":
        table = LeaguePitchingOverall
    else:
        table = LeaguePitchingConference

    q = db.query(table)
    if season:
        q = q.filter(table.season == season)
    q = q.order_by(table.season)
    return pd.read_sql_query(q.statement, q.session.connection())


def get_game_log(
    db: Session,
    team: Optional[str],
    season: Optional[int],
    game_date: Optional[date],
    home: Optional[bool],
    split: Optional[str] = "overall",
):
    q = db.query(GameLog)
    if team:
        q = q.filter(GameLog.team == team)
    if season:
        q = q.filter(GameLog.season == season)
    if game_date:
        q = q.filter(GameLog.date == game_date)
    if home:
        q = q.filter(GameLog.home == home)
    q = q.order_by(GameLog.season, GameLog.team, GameLog.game_num)
    return q.all()
