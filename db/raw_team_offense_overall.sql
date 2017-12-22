create table raw_team_offense_overall (
  Name varchar(30),
  Season integer,
  G integer,
  PA integer,
  AB integer,
  R integer,
  H integer,
  x2B integer,
  x3B integer,
  HR integer,
  RBI integer,
  BB integer,
  SO integer,
  SB integer,
  CS integer,
  AVG numeric,
  OBP numeric,
  SLG numeric,
  HBP integer,
  SF integer,
  SH integer,
  TB integer,
  XBH integer,
  GDP integer,
  GO integer,
  FO integer,
  GO_FO numeric,
  primary key (Name, Season)
)
