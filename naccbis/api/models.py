from sqlalchemy import (
    Column, Integer, String, Numeric, Boolean, Date, ForeignKeyConstraint
)
from .database import Base


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
            ["player_id.fname", "player_id.lname", "player_id.team", "player_id.season"],
            onupdate="CASCADE", ondelete="CASCADE"
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
            ["player_id.fname", "player_id.lname", "player_id.team", "player_id.season"],
            onupdate="CASCADE", ondelete="CASCADE"
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
    l = Column(Integer)
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
            ["player_id.fname", "player_id.lname", "player_id.team", "player_id.season"],
            onupdate="CASCADE", ondelete="CASCADE"
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
    l = Column(Integer)
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
            ["player_id.fname", "player_id.lname", "player_id.team", "player_id.season"],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
    )


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
