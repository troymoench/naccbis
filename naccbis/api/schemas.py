from datetime import date
from typing import Optional
from math import isnan

from pydantic import BaseModel as PydanticBaseModel, validator


class BaseModel(PydanticBaseModel):
    @validator("*")
    def change_nan_to_none(cls, v, values, field):
        # pydantic doesn't like pandas NaN
        if field.outer_type_ is float and isnan(v):
            return None
        return v


class OffenseSchema(BaseModel):
    g: int
    pa: int
    ab: int
    r: int
    h: int
    x2b: int
    x3b: int
    hr: int
    rbi: int
    bb: int
    so: int
    hbp: int
    tb: int
    xbh: int
    sf: int
    sh: int
    gdp: int
    sb: int
    cs: int
    go: int
    fo: int
    go_fo: Optional[float]
    hbp_p: Optional[float]
    bb_p: Optional[float]
    so_p: Optional[float]
    babip: Optional[float]
    iso: Optional[float]
    avg: Optional[float]
    obp: Optional[float]
    slg: Optional[float]
    ops: Optional[float]
    sar: Optional[float]
    # advanced stats (not in db)
    sbr: Optional[float]
    wsb: Optional[float]
    woba: Optional[float]
    wraa: Optional[float]
    off: Optional[float]
    wrc: Optional[float]
    wrc_p: Optional[float]
    off_p: Optional[float]
    rar: Optional[float]

    class Config:
        orm_mode = True


class BattersSchema(BaseModel):
    no: int
    fname: str
    lname: str
    team: str
    season: int
    yr: str
    pos: Optional[str]
    g: int
    pa: int
    ab: int
    r: int
    h: int
    x2b: int
    x3b: int
    hr: int
    rbi: int
    bb: int
    so: int
    hbp: int
    tb: int
    xbh: int
    sf: int
    sh: int
    gdp: int
    sb: int
    cs: int
    go: int
    fo: int
    go_fo: Optional[float]
    hbp_p: Optional[float]
    bb_p: Optional[float]
    so_p: Optional[float]
    babip: Optional[float]
    iso: Optional[float]
    avg: Optional[float]
    obp: Optional[float]
    slg: Optional[float]
    ops: Optional[float]
    sar: Optional[float]
    # advanced stats (not in db)
    sbr: Optional[float]
    wsb: Optional[float]
    woba: Optional[float]
    wraa: Optional[float]
    off: Optional[float]
    wrc: Optional[float]
    wrc_p: Optional[float]
    off_p: Optional[float]
    rar: Optional[float]

    class Config:
        orm_mode = True


class TeamOffenseSchema(BaseModel):
    name: str
    season: int
    g: int
    pa: int
    ab: int
    r: int
    h: int
    x2b: int
    x3b: int
    hr: int
    rbi: int
    bb: int
    so: int
    hbp: int
    tb: int
    xbh: int
    sf: int
    sh: int
    gdp: int
    sb: int
    cs: int
    go: int
    fo: int
    go_fo: Optional[float]
    hbp_p: Optional[float]
    bb_p: Optional[float]
    so_p: Optional[float]
    babip: Optional[float]
    iso: Optional[float]
    avg: Optional[float]
    obp: Optional[float]
    slg: Optional[float]
    ops: Optional[float]
    sar: Optional[float]
    # advanced stats (not in db)
    sbr: Optional[float]
    wsb: Optional[float]
    woba: Optional[float]
    wraa: Optional[float]
    off: Optional[float]
    wrc: Optional[float]
    wrc_p: Optional[float]
    off_p: Optional[float]
    rar: Optional[float]

    class Config:
        orm_mode = True


class LeagueOffenseSchema(BaseModel):
    season: int
    g: int
    pa: int
    ab: int
    r: int
    h: int
    x2b: int
    x3b: int
    hr: int
    rbi: int
    bb: int
    so: int
    hbp: int
    tb: int
    xbh: int
    sf: int
    sh: int
    gdp: int
    sb: int
    cs: int
    go: int
    fo: int
    go_fo: float
    hbp_p: float
    bb_p: float
    so_p: float
    babip: float
    iso: float
    avg: float
    obp: float
    slg: float
    ops: float
    sar: float
    lg_r_pa: float
    bsr_bmult: float
    bsr: float
    lw_hbp: float
    lw_bb: float
    lw_x1b: float
    lw_x2b: float
    lw_x3b: float
    lw_hr: float
    lw_sb: float
    lw_cs: float
    lw_out: float
    ww_hbp: float
    ww_bb: float
    ww_x1b: float
    ww_x2b: float
    ww_x3b: float
    ww_hr: float
    woba_scale: float
    woba: float
    sbr: float
    lg_wsb: float
    wsb: float
    wraa: float
    off: float
    wrc: float
    wrc_p: float
    off_p: float
    rep_level: float
    rar: float

    class Config:
        orm_mode = True


class PitchersSchema(BaseModel):
    no: int
    fname: str
    lname: str
    team: str
    season: int
    yr: str
    pos: Optional[str]
    g: int
    gs: int
    w: int
    l: int
    sv: int
    cg: int
    sho: Optional[int]
    ip: float
    h: int
    r: int
    er: int
    bb: int
    so: int
    x2b: Optional[int]
    x3b: Optional[int]
    hr: int
    ab: Optional[int]
    wp: Optional[int]
    hbp: Optional[int]
    bk: Optional[int]
    sf: Optional[int]
    sh: Optional[int]
    pa: Optional[int]
    hbp_p: Optional[float]
    bb_p: Optional[float]
    so_p: Optional[float]
    iso: Optional[float]
    babip: Optional[float]
    avg: Optional[float]
    obp: Optional[float]
    slg: Optional[float]
    ops: Optional[float]
    lob_p: Optional[float]
    era: Optional[float]
    ra_9: Optional[float]
    so_9: Optional[float]
    bb_9: Optional[float]
    hr_9: Optional[float]
    whip: Optional[float]

    class Config:
        orm_mode = True


class PitchingSchema(BaseModel):
    g: int
    gs: int
    w: int
    l: int
    sv: int
    cg: int
    sho: Optional[int]
    ip: float
    h: int
    r: int
    er: int
    bb: int
    so: int
    x2b: Optional[int]
    x3b: Optional[int]
    hr: int
    ab: Optional[int]
    wp: Optional[int]
    hbp: Optional[int]
    bk: Optional[int]
    sf: Optional[int]
    sh: Optional[int]
    pa: Optional[int]
    hbp_p: Optional[float]
    bb_p: Optional[float]
    so_p: Optional[float]
    iso: Optional[float]
    babip: Optional[float]
    avg: Optional[float]
    obp: Optional[float]
    slg: Optional[float]
    ops: Optional[float]
    lob_p: Optional[float]
    era: Optional[float]
    ra_9: Optional[float]
    so_9: Optional[float]
    bb_9: Optional[float]
    hr_9: Optional[float]
    whip: Optional[float]


class TeamPitchingSchema(BaseModel):
    name: str
    season: int
    g: int
    w: Optional[int]
    l: Optional[int]
    sv: Optional[int]
    cg: Optional[int]
    sho: Optional[int]
    ip: float
    h: int
    r: int
    er: int
    bb: int
    so: int
    x2b: Optional[int]
    x3b: Optional[int]
    hr: int
    ab: Optional[int]
    wp: Optional[int]
    hbp: Optional[int]
    bk: Optional[int]
    sf: Optional[int]
    sh: Optional[int]
    pa: Optional[int]
    hbp_p: Optional[float]
    bb_p: Optional[float]
    so_p: Optional[float]
    iso: Optional[float]
    babip: Optional[float]
    avg: Optional[float]
    obp: Optional[float]
    slg: Optional[float]
    ops: Optional[float]
    lob_p: Optional[float]
    era: Optional[float]
    ra_9: Optional[float]
    so_9: Optional[float]
    bb_9: Optional[float]
    hr_9: Optional[float]
    whip: Optional[float]

    class Config:
        orm_mode = True


class LeaguePitchingSchema(BaseModel):
    season: int
    g: int
    w: Optional[int]
    l: Optional[int]
    sv: Optional[int]
    cg: Optional[int]
    sho: Optional[int]
    ip: float
    h: int
    r: int
    er: int
    bb: int
    so: int
    x2b: Optional[int]
    x3b: Optional[int]
    hr: int
    ab: Optional[int]
    wp: Optional[int]
    hbp: Optional[int]
    bk: Optional[int]
    sf: Optional[int]
    sh: Optional[int]
    pa: Optional[int]
    hbp_p: Optional[float]
    bb_p: Optional[float]
    so_p: Optional[float]
    iso: Optional[float]
    babip: Optional[float]
    avg: Optional[float]
    obp: Optional[float]
    slg: Optional[float]
    ops: Optional[float]
    lob_p: Optional[float]
    era: Optional[float]
    ra_9: Optional[float]
    so_9: Optional[float]
    bb_9: Optional[float]
    hr_9: Optional[float]
    whip: Optional[float]
    lg_r_pa: Optional[float]
    bsr_bmult: Optional[float]
    bsr: Optional[float]
    bsr_9: Optional[float]
    fip_constant: Optional[float]
    fip: Optional[float]
    raa: Optional[float]
    bsraa: Optional[float]
    fipraa: Optional[float]
    era_minus: Optional[float]
    fip_minus: Optional[float]
    bsr_minus: Optional[float]

    class Config:
        orm_mode = True


class PlayerSchema(BaseModel):
    offense: list[BattersSchema] = []
    offense_career: list[OffenseSchema] = []
    pitching: list[PitchersSchema] = []
    pitching_career: list[PitchingSchema] = []


class GameLogSchema(BaseModel):
    game_num: int
    date: date
    season: int
    team: str
    opponent: str
    result: str
    rs: int
    ra: int
    home: bool
    conference: bool

    class Config:
        orm_mode = True
