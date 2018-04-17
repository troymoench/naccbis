create table raw_team_pitching_conference (
  Name varchar(30),
  Season integer,
  G integer,
  IP varchar(20),
  H integer,
  R integer,
  ER integer,
  BB integer,
  SO integer,
  SO_9 numeric,
  HR integer,
  ERA numeric,
  primary key (Name, Season)
)
