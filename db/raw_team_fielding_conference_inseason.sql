create table raw_team_fielding_conference_inseason (
  Name varchar(30),
  Season integer,
  Date date,
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
  primary key (Name, Date)
)
