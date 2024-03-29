""" Database models """
from typing import Any

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKeyConstraint,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

# HACK: sqlalchemy-stubs should be used instead
Base: Any = declarative_base()

Base.metadata.naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class PlayerId(Base):
    __tablename__ = "player_id"

    fname = Column(String(20), primary_key=True)
    lname = Column(String(20), primary_key=True)
    team = Column(String(5), primary_key=True)
    season = Column(Integer, primary_key=True)
    player_id = Column(String(10), nullable=False)


class BattersOverall(Base):
    __tablename__ = "batters_overall"

    no = Column(Integer)
    fname = Column(String(20), primary_key=True)
    lname = Column(String(20), primary_key=True)
    team = Column(String(5), primary_key=True)
    season = Column(Integer, primary_key=True)
    yr = Column(String(2))
    pos = Column(String(15))
    g = Column(Integer)
    pa = Column(Integer)
    ab = Column(Integer)
    r = Column(Integer)
    h = Column(Integer)
    x2b = Column(Integer)
    x3b = Column(Integer)
    hr = Column(Integer)
    rbi = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    hbp = Column(Integer)
    tb = Column(Integer)
    xbh = Column(Integer)
    sf = Column(Integer)
    sh = Column(Integer)
    gdp = Column(Integer)
    sb = Column(Integer)
    cs = Column(Integer)
    go = Column(Integer)
    fo = Column(Integer)
    go_fo = Column(Numeric)
    hbp_p = Column(Numeric)
    bb_p = Column(Numeric)
    so_p = Column(Numeric)
    babip = Column(Numeric)
    iso = Column(Numeric)
    avg = Column(Numeric)
    obp = Column(Numeric)
    slg = Column(Numeric)
    ops = Column(Numeric)
    sar = Column(Numeric)

    __table_args__ = (
        ForeignKeyConstraint(
            ["fname", "lname", "team", "season"],
            [
                "player_id.fname",
                "player_id.lname",
                "player_id.team",
                "player_id.season",
            ],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )


class BattersConference(Base):
    __tablename__ = "batters_conference"

    no = Column(Integer)
    fname = Column(String(20), primary_key=True)
    lname = Column(String(20), primary_key=True)
    team = Column(String(5), primary_key=True)
    season = Column(Integer, primary_key=True)
    yr = Column(String(2))
    pos = Column(String(15))
    g = Column(Integer)
    pa = Column(Integer)
    ab = Column(Integer)
    r = Column(Integer)
    h = Column(Integer)
    x2b = Column(Integer)
    x3b = Column(Integer)
    hr = Column(Integer)
    rbi = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    hbp = Column(Integer)
    tb = Column(Integer)
    xbh = Column(Integer)
    sf = Column(Integer)
    sh = Column(Integer)
    gdp = Column(Integer)
    sb = Column(Integer)
    cs = Column(Integer)
    go = Column(Integer)
    fo = Column(Integer)
    go_fo = Column(Numeric)
    hbp_p = Column(Numeric)
    bb_p = Column(Numeric)
    so_p = Column(Numeric)
    babip = Column(Numeric)
    iso = Column(Numeric)
    avg = Column(Numeric)
    obp = Column(Numeric)
    slg = Column(Numeric)
    ops = Column(Numeric)
    sar = Column(Numeric)

    __table_args__ = (
        ForeignKeyConstraint(
            ["fname", "lname", "team", "season"],
            [
                "player_id.fname",
                "player_id.lname",
                "player_id.team",
                "player_id.season",
            ],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )


class PitchersOverall(Base):
    __tablename__ = "pitchers_overall"

    no = Column(Integer)
    fname = Column(String(20), primary_key=True)
    lname = Column(String(20), primary_key=True)
    team = Column(String(5), primary_key=True)
    season = Column(Integer, primary_key=True)
    yr = Column(String(2))
    pos = Column(String(15))
    g = Column(Integer)
    gs = Column(Integer)
    w = Column(Integer)
    l = Column(Integer)  # noqa: E741
    sv = Column(Integer)
    cg = Column(Integer)
    sho = Column(Integer)
    ip = Column(Numeric)
    h = Column(Integer)
    r = Column(Integer)
    er = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    x2b = Column(Integer)
    x3b = Column(Integer)
    hr = Column(Integer)
    ab = Column(Integer)
    wp = Column(Integer)
    hbp = Column(Integer)
    bk = Column(Integer)
    sf = Column(Integer)
    sh = Column(Integer)
    pa = Column(Integer)
    hbp_p = Column(Numeric)
    bb_p = Column(Numeric)
    so_p = Column(Numeric)
    iso = Column(Numeric)
    babip = Column(Numeric)
    avg = Column(Numeric)
    obp = Column(Numeric)
    slg = Column(Numeric)
    ops = Column(Numeric)
    lob_p = Column(Numeric)
    era = Column(Numeric)
    ra_9 = Column(Numeric)
    so_9 = Column(Numeric)
    bb_9 = Column(Numeric)
    hr_9 = Column(Numeric)
    whip = Column(Numeric)

    __table_args__ = (
        ForeignKeyConstraint(
            ["fname", "lname", "team", "season"],
            [
                "player_id.fname",
                "player_id.lname",
                "player_id.team",
                "player_id.season",
            ],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )


class PitchersConference(Base):
    __tablename__ = "pitchers_conference"

    no = Column(Integer)
    fname = Column(String(20), primary_key=True)
    lname = Column(String(20), primary_key=True)
    team = Column(String(5), primary_key=True)
    season = Column(Integer, primary_key=True)
    yr = Column(String(2))
    pos = Column(String(15))
    g = Column(Integer)
    gs = Column(Integer)
    w = Column(Integer)
    l = Column(Integer)  # noqa: E741
    sv = Column(Integer)
    cg = Column(Integer)
    ip = Column(Numeric)
    h = Column(Integer)
    r = Column(Integer)
    er = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    hr = Column(Integer)
    era = Column(Numeric)
    ra_9 = Column(Numeric)
    so_9 = Column(Numeric)
    bb_9 = Column(Numeric)
    hr_9 = Column(Numeric)
    whip = Column(Numeric)

    __table_args__ = (
        ForeignKeyConstraint(
            ["fname", "lname", "team", "season"],
            [
                "player_id.fname",
                "player_id.lname",
                "player_id.team",
                "player_id.season",
            ],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )


class TeamOffenseOverall(Base):
    __tablename__ = "team_offense_overall"

    name = Column(String(30), primary_key=True)
    season = Column(Integer, primary_key=True)
    g = Column(Integer)
    pa = Column(Integer)
    ab = Column(Integer)
    r = Column(Integer)
    h = Column(Integer)
    x2b = Column(Integer)
    x3b = Column(Integer)
    hr = Column(Integer)
    rbi = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    hbp = Column(Integer)
    tb = Column(Integer)
    xbh = Column(Integer)
    sf = Column(Integer)
    sh = Column(Integer)
    gdp = Column(Integer)
    sb = Column(Integer)
    cs = Column(Integer)
    go = Column(Integer)
    fo = Column(Integer)
    go_fo = Column(Numeric)
    hbp_p = Column(Numeric)
    bb_p = Column(Numeric)
    so_p = Column(Numeric)
    babip = Column(Numeric)
    iso = Column(Numeric)
    avg = Column(Numeric)
    obp = Column(Numeric)
    slg = Column(Numeric)
    ops = Column(Numeric)
    sar = Column(Numeric)


class TeamOffenseConference(Base):
    __tablename__ = "team_offense_conference"

    name = Column(String(30), primary_key=True)
    season = Column(Integer, primary_key=True)
    g = Column(Integer)
    pa = Column(Integer)
    ab = Column(Integer)
    r = Column(Integer)
    h = Column(Integer)
    x2b = Column(Integer)
    x3b = Column(Integer)
    hr = Column(Integer)
    rbi = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    hbp = Column(Integer)
    tb = Column(Integer)
    xbh = Column(Integer)
    sf = Column(Integer)
    sh = Column(Integer)
    gdp = Column(Integer)
    sb = Column(Integer)
    cs = Column(Integer)
    go = Column(Integer)
    fo = Column(Integer)
    go_fo = Column(Numeric)
    hbp_p = Column(Numeric)
    bb_p = Column(Numeric)
    so_p = Column(Numeric)
    babip = Column(Numeric)
    iso = Column(Numeric)
    avg = Column(Numeric)
    obp = Column(Numeric)
    slg = Column(Numeric)
    ops = Column(Numeric)
    sar = Column(Numeric)


class TeamPitchingOverall(Base):
    __tablename__ = "team_pitching_overall"

    name = Column(String(30), primary_key=True)
    season = Column(Integer, primary_key=True)
    g = Column(Integer)
    w = Column(Integer)
    l = Column(Integer)  # noqa: E741
    sv = Column(Integer)
    cg = Column(Integer)
    sho = Column(Integer)
    ip = Column(Numeric)
    h = Column(Integer)
    r = Column(Integer)
    er = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    x2b = Column(Integer)
    x3b = Column(Integer)
    hr = Column(Integer)
    ab = Column(Integer)
    wp = Column(Integer)
    hbp = Column(Integer)
    bk = Column(Integer)
    sf = Column(Integer)
    sh = Column(Integer)
    pa = Column(Integer)
    hbp_p = Column(Numeric)
    bb_p = Column(Numeric)
    so_p = Column(Numeric)
    iso = Column(Numeric)
    babip = Column(Numeric)
    avg = Column(Numeric)
    obp = Column(Numeric)
    slg = Column(Numeric)
    ops = Column(Numeric)
    lob_p = Column(Numeric)
    era = Column(Numeric)
    ra_9 = Column(Numeric)
    so_9 = Column(Numeric)
    bb_9 = Column(Numeric)
    hr_9 = Column(Numeric)
    whip = Column(Numeric)


class TeamPitchingConference(Base):
    __tablename__ = "team_pitching_conference"

    name = Column(String(30), primary_key=True)
    season = Column(Integer, primary_key=True)
    g = Column(Integer)
    ip = Column(Numeric)
    h = Column(Integer)
    r = Column(Integer)
    er = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    so_9 = Column(Numeric)
    hr = Column(Integer)
    era = Column(Numeric)
    ra_9 = Column(Numeric)
    bb_9 = Column(Numeric)
    hr_9 = Column(Numeric)
    whip = Column(Numeric)


class LeagueOffenseOverall(Base):
    __tablename__ = "league_offense_overall"

    season = Column(Integer, primary_key=True)
    g = Column(Integer)
    pa = Column(Integer)
    ab = Column(Integer)
    r = Column(Integer)
    h = Column(Integer)
    x2b = Column(Integer)
    x3b = Column(Integer)
    hr = Column(Integer)
    rbi = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    hbp = Column(Integer)
    tb = Column(Integer)
    xbh = Column(Integer)
    sf = Column(Integer)
    sh = Column(Integer)
    gdp = Column(Integer)
    sb = Column(Integer)
    cs = Column(Integer)
    go = Column(Integer)
    fo = Column(Integer)
    go_fo = Column(Numeric)
    hbp_p = Column(Numeric)
    bb_p = Column(Numeric)
    so_p = Column(Numeric)
    babip = Column(Numeric)
    iso = Column(Numeric)
    avg = Column(Numeric)
    obp = Column(Numeric)
    slg = Column(Numeric)
    ops = Column(Numeric)
    sar = Column(Numeric)
    lg_r_pa = Column(Numeric)
    bsr_bmult = Column(Numeric)
    bsr = Column(Numeric)
    lw_hbp = Column(Numeric)
    lw_bb = Column(Numeric)
    lw_x1b = Column(Numeric)
    lw_x2b = Column(Numeric)
    lw_x3b = Column(Numeric)
    lw_hr = Column(Numeric)
    lw_sb = Column(Numeric)
    lw_cs = Column(Numeric)
    lw_out = Column(Numeric)
    ww_hbp = Column(Numeric)
    ww_bb = Column(Numeric)
    ww_x1b = Column(Numeric)
    ww_x2b = Column(Numeric)
    ww_x3b = Column(Numeric)
    ww_hr = Column(Numeric)
    woba_scale = Column(Numeric)
    woba = Column(Numeric)
    sbr = Column(Numeric)
    lg_wsb = Column(Numeric)
    wsb = Column(Numeric)
    wraa = Column(Numeric)
    off = Column(Numeric)
    wrc = Column(Numeric)
    wrc_p = Column(Numeric)
    off_p = Column(Numeric)
    rep_level = Column(Numeric)
    rar = Column(Numeric)


class LeagueOffenseConference(Base):
    __tablename__ = "league_offense_conference"

    season = Column(Integer, primary_key=True)
    g = Column(Integer)
    pa = Column(Integer)
    ab = Column(Integer)
    r = Column(Integer)
    h = Column(Integer)
    x2b = Column(Integer)
    x3b = Column(Integer)
    hr = Column(Integer)
    rbi = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    hbp = Column(Integer)
    tb = Column(Integer)
    xbh = Column(Integer)
    sf = Column(Integer)
    sh = Column(Integer)
    gdp = Column(Integer)
    sb = Column(Integer)
    cs = Column(Integer)
    go = Column(Integer)
    fo = Column(Integer)
    go_fo = Column(Numeric)
    hbp_p = Column(Numeric)
    bb_p = Column(Numeric)
    so_p = Column(Numeric)
    babip = Column(Numeric)
    iso = Column(Numeric)
    avg = Column(Numeric)
    obp = Column(Numeric)
    slg = Column(Numeric)
    ops = Column(Numeric)
    sar = Column(Numeric)
    lg_r_pa = Column(Numeric)
    bsr_bmult = Column(Numeric)
    bsr = Column(Numeric)
    lw_hbp = Column(Numeric)
    lw_bb = Column(Numeric)
    lw_x1b = Column(Numeric)
    lw_x2b = Column(Numeric)
    lw_x3b = Column(Numeric)
    lw_hr = Column(Numeric)
    lw_sb = Column(Numeric)
    lw_cs = Column(Numeric)
    lw_out = Column(Numeric)
    ww_hbp = Column(Numeric)
    ww_bb = Column(Numeric)
    ww_x1b = Column(Numeric)
    ww_x2b = Column(Numeric)
    ww_x3b = Column(Numeric)
    ww_hr = Column(Numeric)
    woba_scale = Column(Numeric)
    woba = Column(Numeric)
    sbr = Column(Numeric)
    lg_wsb = Column(Numeric)
    wsb = Column(Numeric)
    wraa = Column(Numeric)
    off = Column(Numeric)
    wrc = Column(Numeric)
    wrc_p = Column(Numeric)
    off_p = Column(Numeric)
    rep_level = Column(Numeric)
    rar = Column(Numeric)


class LeaguePitchingOverall(Base):
    __tablename__ = "league_pitching_overall"

    season = Column(Integer, primary_key=True)
    g = Column(Integer)
    w = Column(Integer)
    l = Column(Integer)  # noqa: E741
    sv = Column(Integer)
    cg = Column(Integer)
    sho = Column(Integer)
    ip = Column(Numeric)
    h = Column(Integer)
    r = Column(Integer)
    er = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    x2b = Column(Integer)
    x3b = Column(Integer)
    hr = Column(Integer)
    ab = Column(Integer)
    wp = Column(Integer)
    hbp = Column(Integer)
    bk = Column(Integer)
    sf = Column(Integer)
    sh = Column(Integer)
    pa = Column(Integer)
    hbp_p = Column(Numeric)
    bb_p = Column(Numeric)
    so_p = Column(Numeric)
    iso = Column(Numeric)
    babip = Column(Numeric)
    avg = Column(Numeric)
    obp = Column(Numeric)
    slg = Column(Numeric)
    ops = Column(Numeric)
    lob_p = Column(Numeric)
    era = Column(Numeric)
    ra_9 = Column(Numeric)
    so_9 = Column(Numeric)
    bb_9 = Column(Numeric)
    hr_9 = Column(Numeric)
    whip = Column(Numeric)
    lg_r_pa = Column(Numeric)
    bsr_bmult = Column(Numeric)
    bsr = Column(Numeric)
    bsr_9 = Column(Numeric)
    fip_constant = Column(Numeric)
    fip = Column(Numeric)
    raa = Column(Numeric)
    bsraa = Column(Numeric)
    fipraa = Column(Numeric)
    era_minus = Column(Numeric)
    fip_minus = Column(Numeric)
    bsr_minus = Column(Numeric)


class LeaguePitchingConference(Base):
    __tablename__ = "league_pitching_conference"

    season = Column(Integer, primary_key=True)
    g = Column(Integer)
    ip = Column(Numeric)
    h = Column(Integer)
    r = Column(Integer)
    er = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    so_9 = Column(Numeric)
    hr = Column(Integer)
    era = Column(Numeric)
    ra_9 = Column(Numeric)
    bb_9 = Column(Numeric)
    hr_9 = Column(Numeric)
    whip = Column(Numeric)
    raa = Column(Numeric)
    era_minus = Column(Numeric)


class GameLog(Base):
    __tablename__ = "game_log"

    game_num = Column(Integer, primary_key=True)
    date = Column(Date)
    season = Column(Integer, primary_key=True)
    team = Column(String(30), primary_key=True)
    opponent = Column(String(30))
    result = Column(String(1))
    rs = Column(Integer)
    ra = Column(Integer)
    home = Column(Boolean)
    conference = Column(Boolean)


class NameCorrection(Base):
    __tablename__ = "name_corrections"

    uc_fname = Column(String(20), primary_key=True)
    uc_lname = Column(String(20), primary_key=True)
    uc_team = Column(String(5), primary_key=True)
    uc_season = Column(Integer, primary_key=True)
    c_fname = Column(String(20), nullable=False)
    c_lname = Column(String(20), nullable=False)
    type = Column(String(1))
    submitted = Column(DateTime, server_default=func.now())


class Nickname(Base):
    __tablename__ = "nicknames"

    rid = Column(Integer, nullable=False)
    name = Column(String(20), primary_key=True)
    nickname = Column(String(20), primary_key=True)


class DuplicateName(Base):
    __tablename__ = "duplicate_names"
    fname = Column(String(20), primary_key=True)
    lname = Column(String(20), primary_key=True)
    team = Column(String(5), primary_key=True)
    season = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=False)


class RawBattersOverall(Base):
    __tablename__ = "raw_batters_overall"

    no = Column(Integer)
    name = Column(String(35), primary_key=True)
    team = Column(String(5), primary_key=True)
    season = Column(Integer, primary_key=True)
    yr = Column(String(2))
    pos = Column(String(15))
    g = Column(Integer)
    pa = Column(Integer)
    ab = Column(Integer)
    r = Column(Integer)
    h = Column(Integer)
    x2b = Column(Integer)
    x3b = Column(Integer)
    hr = Column(Integer)
    rbi = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    sb = Column(Integer)
    cs = Column(Integer)
    avg = Column(Numeric)
    obp = Column(Numeric)
    slg = Column(Numeric)
    hbp = Column(Integer)
    sf = Column(Integer)
    sh = Column(Integer)
    tb = Column(Integer)
    xbh = Column(Integer)
    gdp = Column(Integer)
    go = Column(Integer)
    fo = Column(Integer)
    go_fo = Column(Numeric)


class RawBattersConference(Base):
    __tablename__ = "raw_batters_conference"

    no = Column(Integer)
    name = Column(String(35), primary_key=True)
    team = Column(String(5), primary_key=True)
    season = Column(Integer, primary_key=True)
    yr = Column(String(2))
    pos = Column(String(15))
    g = Column(Integer)
    pa = Column(Integer)
    ab = Column(Integer)
    r = Column(Integer)
    h = Column(Integer)
    x2b = Column(Integer)
    x3b = Column(Integer)
    hr = Column(Integer)
    rbi = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    sb = Column(Integer)
    cs = Column(Integer)
    avg = Column(Numeric)
    obp = Column(Numeric)
    slg = Column(Numeric)
    hbp = Column(Integer)
    sf = Column(Integer)
    sh = Column(Integer)
    tb = Column(Integer)
    xbh = Column(Integer)
    gdp = Column(Integer)
    go = Column(Integer)
    fo = Column(Integer)
    go_fo = Column(Numeric)


class RawPitchersOverall(Base):
    __tablename__ = "raw_pitchers_overall"

    no = Column(Integer)
    name = Column(String(35), primary_key=True)
    team = Column(String(5), primary_key=True)
    season = Column(Integer, primary_key=True)
    yr = Column(String(2))
    pos = Column(String(15))
    g = Column(Integer)
    gs = Column(Integer)
    w = Column(Integer)
    l = Column(Integer)  # noqa: E741
    sv = Column(Integer)
    cg = Column(Integer)
    sho = Column(Integer)
    ip = Column(String(20))
    h = Column(Integer)
    r = Column(Integer)
    er = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    era = Column(Numeric)
    x2b = Column(Integer)
    x3b = Column(Integer)
    hr = Column(Integer)
    ab = Column(Integer)
    avg = Column(Numeric)
    wp = Column(Integer)
    hbp = Column(Integer)
    bk = Column(Integer)
    sf = Column(Integer)
    sh = Column(Integer)
    so_9 = Column(Numeric)


class RawPitchersConference(Base):
    __tablename__ = "raw_pitchers_conference"

    no = Column(Integer)
    name = Column(String(35), primary_key=True)
    team = Column(String(5), primary_key=True)
    season = Column(Integer, primary_key=True)
    yr = Column(String(2))
    pos = Column(String(15))
    g = Column(Integer)
    gs = Column(Integer)
    w = Column(Integer)
    l = Column(Integer)  # noqa: E741
    sv = Column(Integer)
    cg = Column(Integer)
    ip = Column(String(20))
    h = Column(Integer)
    r = Column(Integer)
    er = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    so_9 = Column(Numeric)
    hr = Column(Integer)
    era = Column(Numeric)


class RawGameLogFielding(Base):
    __tablename__ = "raw_game_log_fielding"

    game_num = Column(Integer, primary_key=True)
    date = Column(String(10), primary_key=True)
    season = Column(Integer, primary_key=True)
    name = Column(String(30), primary_key=True)
    opponent = Column(String)
    score = Column(String(10))
    tc = Column(Integer)
    po = Column(Integer)
    a = Column(Integer)
    e = Column(Integer)
    fpct = Column(Numeric)
    dp = Column(Integer)
    sba = Column(Integer)
    cs = Column(Integer)
    cspct = Column(Numeric)
    pb = Column(Integer)
    ci = Column(Integer)


class RawGameLogHitting(Base):
    __tablename__ = "raw_game_log_hitting"

    game_num = Column(Integer, primary_key=True)
    date = Column(String(10), primary_key=True)
    season = Column(Integer, primary_key=True)
    name = Column(String(30), primary_key=True)
    opponent = Column(String)
    score = Column(String(10))
    ab = Column(Integer)
    r = Column(Integer)
    h = Column(Integer)
    x2b = Column(Integer)
    x3b = Column(Integer)
    hr = Column(Integer)
    rbi = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)
    sb = Column(Integer)
    cs = Column(Integer)
    hbp = Column(Integer)
    sf = Column(Integer)
    sh = Column(Integer)
    tb = Column(Integer)
    xbh = Column(Integer)
    gbp = Column(Integer)
    go = Column(Integer)
    fo = Column(Integer)
    go_fo = Column(Numeric)
    pa = Column(Integer)


class RawGameLogPitching(Base):
    __tablename__ = "raw_game_log_pitching"

    game_num = Column(Integer, primary_key=True)
    date = Column(String(10), primary_key=True)
    season = Column(Integer, primary_key=True)
    name = Column(String(30), primary_key=True)
    opponent = Column(String)
    score = Column(String(10))
    w = Column(Integer)
    l = Column(Integer)  # noqa: E741
    sv = Column(Integer)
    ip = Column(Numeric)
    h = Column(Integer)
    r = Column(Integer)
    er = Column(Integer)
    era = Column(Numeric)
    bb = Column(Integer)
    so = Column(Integer)
    hr = Column(Integer)
