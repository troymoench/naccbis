create table raw_team_fielding_overall (
  Name varchar(30),
  Season integer,
  G integer,
  TC integer,
  PO integer,
  A integer,
  E integer,
  FPCT numeric,
  DP integer,
  SBA integer,
  CS integer,
  CSPCT numeric,
  PB integer,
  CI integer,
  primary key (Name, Season)
)
