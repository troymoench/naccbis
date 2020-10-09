from typing import Optional
from pydantic import BaseModel


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