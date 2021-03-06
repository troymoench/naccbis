create table raw_batters_conference (
  No integer,
  Name varchar(35),
  Team varchar(5),
  Season integer,
  Yr char(2),
  Pos varchar(15),
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
  primary key (Name, Team, Season)
);

create table raw_batters_conference_inseason (
  No integer,
  Name varchar(35),
  Team varchar(5),
  Season integer,
  Date date,
  Yr char(2),
  Pos varchar(15),
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
  primary key (Name, Team, Date)
);

create table raw_batters_overall (
  No integer,
  Name varchar(35),
  Team varchar(5),
  Season integer,
  Yr char(2),
  Pos varchar(15),
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
  primary key (Name, Team, Season)
);

create table raw_batters_overall_inseason (
  No integer,
  Name varchar(35),
  Team varchar(5),
  Season integer,
  Date date,
  Yr char(2),
  Pos varchar(15),
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
  primary key (Name, Team, Date)
);

create table raw_game_log_fielding (
  Game_num integer,
  Date varchar(10),
  Season integer,
  Name varchar(30),
  Opponent text,
  Score varchar(10),
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
  primary key (Game_num, Date, Season, Name)
);

create table raw_game_log_fielding_inseason (
  Game_num integer,
  Scrape_date date,
  Date varchar(10),
  Season integer,
  Name varchar(30),
  Opponent text,
  Score varchar(10),
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
  primary key (Game_num, Scrape_date, Name)
);

create table raw_game_log_hitting (
  Game_num integer,
  Date varchar(10),
  Season integer,
  Name varchar(30),
  Opponent text,
  Score varchar(10),
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
  HBP integer,
  SF integer,
  SH integer,
  TB integer,
  XBH integer,
  GDP integer,
  GO integer,
  FO integer,
  GO_FO numeric,
  PA integer,
  primary key (Game_num, Date, Season, Name)

);

create table raw_game_log_hitting_inseason (
  Game_num integer,
  Scrape_date date,
  Date varchar(10),
  Season integer,
  Name varchar(30),
  Opponent text,
  Score varchar(10),
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
  HBP integer,
  SF integer,
  SH integer,
  TB integer,
  XBH integer,
  GDP integer,
  GO integer,
  FO integer,
  GO_FO numeric,
  PA integer,
  primary key (Game_num, Scrape_date, Name)

);

create table raw_game_log_pitching (
  Game_num integer,
  Date varchar(10),
  Season integer,
  Name varchar(30),
  Opponent text,
  Score varchar(10),
  W integer,
  L integer,
  SV integer,
  IP varchar(20),
  H integer,
  R integer,
  ER integer,
  ERA numeric,
  BB integer,
  SO integer,
  HR integer,
  primary key (Game_num, Date, Season, Name)
);

create table raw_game_log_pitching_inseason (
  Game_num integer,
  Scrape_date date,
  Date varchar(10),
  Season integer,
  Name varchar(30),
  Opponent text,
  Score varchar(10),
  W integer,
  L integer,
  SV integer,
  IP varchar(20),
  H integer,
  R integer,
  ER integer,
  ERA numeric,
  BB integer,
  SO integer,
  HR integer,
  primary key (Game_num, Scrape_date, Name)

);

create table raw_pitchers_conference (
  No integer,
  Name varchar(35),
  Team varchar(5),
  Season integer,
  Yr varchar(2),
  Pos varchar(15),
  G integer,
  GS integer,
  W integer,
  L integer,
  SV integer,
  CG integer,
  IP varchar(20),
  H integer,
  R integer,
  ER integer,
  BB integer,
  SO integer,
  SO_9 numeric,
  HR integer,
  ERA numeric,
  primary key (Name, Team, Season)
);

create table raw_pitchers_conference_inseason (
  No integer,
  Name varchar(35),
  Team varchar(5),
  Season integer,
  Date date,
  Yr varchar(2),
  Pos varchar(15),
  G integer,
  GS integer,
  W integer,
  L integer,
  SV integer,
  CG integer,
  IP varchar(20),
  H integer,
  R integer,
  ER integer,
  BB integer,
  SO integer,
  SO_9 numeric,
  HR integer,
  ERA numeric,
  primary key (Name, Team, Date)
);

create table raw_pitchers_overall (
  No integer,
  Name varchar(35),
  Team varchar(5),
  Season integer,
  Yr char(2),
  Pos varchar(15),
  G integer,
  GS integer,
  W integer,
  L integer,
  SV integer,
  CG integer,
  SHO integer,
  IP varchar(20),
  H integer,
  R integer,
  ER integer,
  BB integer,
  SO integer,
  ERA numeric,
  x2B integer,
  x3B integer,
  HR integer,
  AB integer,
  AVG numeric,
  WP integer,
  HBP integer,
  BK integer,
  SF integer,
  SH integer,
  SO_9 numeric,
  primary key (Name, Team, Season)
);

create table raw_pitchers_overall_inseason (
  No integer,
  Name varchar(35),
  Team varchar(5),
  Season integer,
  Date date,
  Yr char(2),
  Pos varchar(15),
  G integer,
  GS integer,
  W integer,
  L integer,
  SV integer,
  CG integer,
  SHO integer,
  IP varchar(20),
  H integer,
  R integer,
  ER integer,
  BB integer,
  SO integer,
  ERA numeric,
  x2B integer,
  x3B integer,
  HR integer,
  AB integer,
  AVG numeric,
  WP integer,
  HBP integer,
  BK integer,
  SF integer,
  SH integer,
  SO_9 numeric,
  primary key (Name, Team, Date)
);

create table raw_team_fielding_conference (
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
);

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
);

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
);

create table raw_team_fielding_overall_inseason (
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
);

create table raw_team_offense_conference (
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
);

create table raw_team_offense_conference_inseason (
  Name varchar(30),
  Season integer,
  Date date,
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
  primary key (Name, Season, Date)
);

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
);

create table raw_team_offense_overall_inseason (
  Name varchar(30),
  Season integer,
  Date date,
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
  primary key (Name, Season, Date)
);

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
);

create table raw_team_pitching_conference_inseason (
  Name varchar(30),
  Season integer,
  Date date,
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
  primary key (Name, Season, Date)
);

create table raw_team_pitching_overall (
  Name varchar(30),
  Season integer,
  G integer,
  W integer,
  L integer,
  SV integer,
  CG integer,
  SHO integer,
  IP varchar(20),
  H integer,
  R integer,
  ER integer,
  BB integer,
  SO integer,
  ERA numeric,
  x2B integer,
  x3B integer,
  HR integer,
  AB integer,
  AVG numeric,
  WP integer,
  HBP integer,
  BK integer,
  SF integer,
  SH integer,
  SO_9 numeric,
  primary key (Name, Season)
);

create table raw_team_pitching_overall_inseason (
  Name varchar(30),
  Season integer,
  Date date,
  G integer,
  W integer,
  L integer,
  SV integer,
  CG integer,
  SHO integer,
  IP varchar(20),
  H integer,
  R integer,
  ER integer,
  BB integer,
  SO integer,
  ERA numeric,
  x2B integer,
  x3B integer,
  HR integer,
  AB integer,
  AVG numeric,
  WP integer,
  HBP integer,
  BK integer,
  SF integer,
  SH integer,
  SO_9 numeric,
  primary key (Name, Season, Date)
);

create table name_corrections (
  uc_fname varchar(20) not null,
  uc_lname varchar(20) not null,
  uc_team varchar(5) not null,
  uc_season integer not null,
  c_fname varchar(20) not null,
  c_lname varchar(20) not null,
  type char(1),
  submitted timestamp default now(),
  primary key (uc_fname, uc_lname, uc_team, uc_season)
);

create table nicknames (
  rid integer,
  name varchar(20),
  nickname varchar(20),
  primary key (name, nickname)
);

create table duplicate_names (
  fname varchar(20),
  lname varchar(20),
  team varchar(5),
  season integer,
  id integer,
  primary key (fname, lname, team, season)
);

create table player_id (
  fname varchar(20),
  lname varchar(20),
  team varchar(5),
  season integer,
  player_id varchar(10),
  primary key (fname, lname, team, season)
);

create table game_log (
  game_num integer,
  date date,
  season integer,
  team varchar(30),
  opponent varchar(30),
  result varchar(1),
  rs integer,
  ra integer,
  home boolean,
  conference boolean,
  primary key (game_num, season, team)
);

create table game_log_inseason (
  scrape_date date,
  game_num integer,
  date date,
  season integer,
  team varchar(30),
  opponent varchar(30),
  result varchar(1),
  rs integer,
  ra integer,
  home boolean,
  conference boolean,
  primary key (scrape_date, game_num, season, team)
);

create table batters_overall (
  no integer,
  fname varchar(20),
  lname varchar(20),
  team varchar(5),
  season integer,
  yr char(2),
  pos varchar(15),
  g integer,
  pa integer,
  ab integer,
  r integer,
  h integer,
  x2b integer,
  x3b integer,
  hr integer,
  rbi integer,
  bb integer,
  so integer,
  hbp integer,
  tb integer,
  xbh integer,
  sf integer,
  sh integer,
  gdp integer,
  sb integer,
  cs integer,
  go integer,
  fo integer,
  go_fo numeric,
  hbp_p numeric,
  bb_p numeric,
  so_p numeric,
  babip numeric,
  iso numeric,
  avg numeric,
  obp numeric,
  slg numeric,
  ops numeric,
  sar numeric,
  primary key (fname, lname, team, season)
);

create table batters_overall_inseason (
  no integer,
  fname varchar(20),
  lname varchar(20),
  team varchar(5),
  season integer,
  date date,
  yr char(2),
  pos varchar(15),
  g integer,
  pa integer,
  ab integer,
  r integer,
  h integer,
  x2b integer,
  x3b integer,
  hr integer,
  rbi integer,
  bb integer,
  so integer,
  hbp integer,
  tb integer,
  xbh integer,
  sf integer,
  sh integer,
  gdp integer,
  sb integer,
  cs integer,
  go integer,
  fo integer,
  go_fo numeric,
  hbp_p numeric,
  bb_p numeric,
  so_p numeric,
  babip numeric,
  iso numeric,
  avg numeric,
  obp numeric,
  slg numeric,
  ops numeric,
  sar numeric,
  primary key (fname, lname, team, season, date)
);

create table batters_conference (
  no integer,
  fname varchar(20),
  lname varchar(20),
  team varchar(5),
  season integer,
  yr char(2),
  pos varchar(15),
  g integer,
  pa integer,
  ab integer,
  r integer,
  h integer,
  x2b integer,
  x3b integer,
  hr integer,
  rbi integer,
  bb integer,
  so integer,
  hbp integer,
  tb integer,
  xbh integer,
  sf integer,
  sh integer,
  gdp integer,
  sb integer,
  cs integer,
  go integer,
  fo integer,
  go_fo numeric,
  hbp_p numeric,
  bb_p numeric,
  so_p numeric,
  babip numeric,
  iso numeric,
  avg numeric,
  obp numeric,
  slg numeric,
  ops numeric,
  sar numeric,
  primary key (fname, lname, team, season)
);

create table batters_conference_inseason (
  no integer,
  fname varchar(20),
  lname varchar(20),
  team varchar(5),
  season integer,
  date date,
  yr char(2),
  pos varchar(15),
  g integer,
  pa integer,
  ab integer,
  r integer,
  h integer,
  x2b integer,
  x3b integer,
  hr integer,
  rbi integer,
  bb integer,
  so integer,
  hbp integer,
  tb integer,
  xbh integer,
  sf integer,
  sh integer,
  gdp integer,
  sb integer,
  cs integer,
  go integer,
  fo integer,
  go_fo numeric,
  hbp_p numeric,
  bb_p numeric,
  so_p numeric,
  babip numeric,
  iso numeric,
  avg numeric,
  obp numeric,
  slg numeric,
  ops numeric,
  sar numeric,
  primary key (fname, lname, team, season, date)
);

create table pitchers_overall (
  no integer,
  fname varchar(20),
  lname varchar(20),
  team varchar(5),
  season integer,
  yr char(2),
  pos varchar(15),
  g integer,
  gs integer,
  w integer,
  l integer,
  sv integer,
  cg integer,
  sho integer,
  ip numeric,
  h integer,
  r integer,
  er integer,
  bb integer,
  so integer,
  x2b integer,
  x3b integer,
  hr integer,
  ab integer,
  wp integer,
  hbp integer,
  bk integer,
  sf integer,
  sh integer,
  pa integer,
  hbp_p numeric,
  bb_p numeric,
  so_p numeric,
  iso numeric,
  babip numeric,
  avg numeric,
  obp numeric,
  slg numeric,
  ops numeric,
  lob_p numeric,
  era numeric,
  ra_9 numeric,
  so_9 numeric,
  bb_9 numeric,
  hr_9 numeric,
  whip numeric,
  primary key (fname, lname, team, season)
);

create table pitchers_overall_inseason (
  no integer,
  fname varchar(20),
  lname varchar(20),
  team varchar(5),
  season integer,
  date date,
  yr char(2),
  pos varchar(15),
  g integer,
  gs integer,
  w integer,
  l integer,
  sv integer,
  cg integer,
  sho integer,
  ip numeric,
  h integer,
  r integer,
  er integer,
  bb integer,
  so integer,
  x2b integer,
  x3b integer,
  hr integer,
  ab integer,
  wp integer,
  hbp integer,
  bk integer,
  sf integer,
  sh integer,
  pa integer,
  hbp_p numeric,
  bb_p numeric,
  so_p numeric,
  iso numeric,
  babip numeric,
  avg numeric,
  obp numeric,
  slg numeric,
  ops numeric,
  lob_p numeric,
  era numeric,
  ra_9 numeric,
  so_9 numeric,
  bb_9 numeric,
  hr_9 numeric,
  whip numeric,
  primary key (fname, lname, team, season, date)
);

create table pitchers_conference (
  no integer,
  fname varchar(20),
  lname varchar(20),
  team varchar(5),
  season integer,
  yr char(2),
  pos varchar(15),
  g integer,
  gs integer,
  w integer,
  l integer,
  sv integer,
  cg integer,
  ip numeric,
  h integer,
  r integer,
  er integer,
  bb integer,
  so integer,
  so_9 numeric,
  hr integer,
  era numeric,
  ra_9 numeric,
  bb_9 numeric,
  hr_9 numeric,
  whip numeric,
  primary key (fname, lname, team, season)
);

create table pitchers_conference_inseason (
  no integer,
  fname varchar(20),
  lname varchar(20),
  team varchar(5),
  season integer,
  date date,
  yr char(2),
  pos varchar(15),
  g integer,
  gs integer,
  w integer,
  l integer,
  sv integer,
  cg integer,
  ip numeric,
  h integer,
  r integer,
  er integer,
  bb integer,
  so integer,
  so_9 numeric,
  hr integer,
  era numeric,
  ra_9 numeric,
  bb_9 numeric,
  hr_9 numeric,
  whip numeric,
  primary key (fname, lname, team, season, date)
);

create table team_offense_overall (
  name varchar(30),
  season integer,
  g integer,
  pa integer,
  ab integer,
  r integer,
  h integer,
  x2b integer,
  x3b integer,
  hr integer,
  rbi integer,
  bb integer,
  so integer,
  hbp integer,
  tb integer,
  xbh integer,
  sf integer,
  sh integer,
  gdp integer,
  sb integer,
  cs integer,
  go integer,
  fo integer,
  go_fo numeric,
  hbp_p numeric,
  bb_p numeric,
  so_p numeric,
  babip numeric,
  iso numeric,
  avg numeric,
  obp numeric,
  slg numeric,
  ops numeric,
  sar numeric,
  primary key (name, season)
);

create table team_offense_overall_inseason (
  name varchar(30),
  season integer,
  date date,
  g integer,
  pa integer,
  ab integer,
  r integer,
  h integer,
  x2b integer,
  x3b integer,
  hr integer,
  rbi integer,
  bb integer,
  so integer,
  hbp integer,
  tb integer,
  xbh integer,
  sf integer,
  sh integer,
  gdp integer,
  sb integer,
  cs integer,
  go integer,
  fo integer,
  go_fo numeric,
  hbp_p numeric,
  bb_p numeric,
  so_p numeric,
  babip numeric,
  iso numeric,
  avg numeric,
  obp numeric,
  slg numeric,
  ops numeric,
  sar numeric,
  primary key (name, season, date)
);

create table team_offense_conference (
  name varchar(30),
  season integer,
  g integer,
  pa integer,
  ab integer,
  r integer,
  h integer,
  x2b integer,
  x3b integer,
  hr integer,
  rbi integer,
  bb integer,
  so integer,
  hbp integer,
  tb integer,
  xbh integer,
  sf integer,
  sh integer,
  gdp integer,
  sb integer,
  cs integer,
  go integer,
  fo integer,
  go_fo numeric,
  hbp_p numeric,
  bb_p numeric,
  so_p numeric,
  babip numeric,
  iso numeric,
  avg numeric,
  obp numeric,
  slg numeric,
  ops numeric,
  sar numeric,
  primary key (name, season)
);

create table team_offense_conference_inseason (
  name varchar(30),
  season integer,
  date date,
  g integer,
  pa integer,
  ab integer,
  r integer,
  h integer,
  x2b integer,
  x3b integer,
  hr integer,
  rbi integer,
  bb integer,
  so integer,
  hbp integer,
  tb integer,
  xbh integer,
  sf integer,
  sh integer,
  gdp integer,
  sb integer,
  cs integer,
  go integer,
  fo integer,
  go_fo numeric,
  hbp_p numeric,
  bb_p numeric,
  so_p numeric,
  babip numeric,
  iso numeric,
  avg numeric,
  obp numeric,
  slg numeric,
  ops numeric,
  sar numeric,
  primary key (name, season, date)
);

create table team_pitching_overall (
  name varchar(30),
  season integer,
  g integer,
  w integer,
  l integer,
  sv integer,
  cg integer,
  sho integer,
  ip numeric,
  h integer,
  r integer,
  er integer,
  bb integer,
  so integer,
  era numeric,
  x2b integer,
  x3b integer,
  hr integer,
  ab integer,
  avg numeric,
  wp integer,
  hbp integer,
  bk integer,
  sf integer,
  sh integer,
  so_9 numeric,
  pa integer,
  obp numeric,
  slg numeric,
  ops numeric,
  hbp_p numeric,
  bb_p numeric,
  so_p numeric,
  iso  numeric,
  babip numeric,
  lob_p numeric,
  ra_9 numeric,
  bb_9 numeric,
  hr_9 numeric,
  whip numeric,
  primary key (name, season)
);

create table team_pitching_overall_inseason (
  name varchar(30),
  season integer,
  date date,
  g integer,
  w integer,
  l integer,
  sv integer,
  cg integer,
  sho integer,
  ip numeric,
  h integer,
  r integer,
  er integer,
  bb integer,
  so integer,
  era numeric,
  x2b integer,
  x3b integer,
  hr integer,
  ab integer,
  avg numeric,
  wp integer,
  hbp integer,
  bk integer,
  sf integer,
  sh integer,
  so_9 numeric,
  pa integer,
  obp numeric,
  slg numeric,
  ops numeric,
  hbp_p numeric,
  bb_p numeric,
  so_p numeric,
  iso  numeric,
  babip numeric,
  lob_p numeric,
  ra_9 numeric,
  bb_9 numeric,
  hr_9 numeric,
  whip numeric,
  primary key (name, season, date)
);

create table team_pitching_conference (
  name varchar(30),
  season integer,
  g integer,
  ip numeric,
  h integer,
  r integer,
  er integer,
  bb integer,
  so integer,
  so_9 numeric,
  hr integer,
  era numeric,
  ra_9 numeric,
  bb_9 numeric,
  hr_9 numeric,
  whip numeric,
  primary key(name, season)
);

create table team_pitching_conference_inseason (
  name varchar(30),
  season integer,
  date date,
  g integer,
  ip numeric,
  h integer,
  r integer,
  er integer,
  bb integer,
  so integer,
  so_9 numeric,
  hr integer,
  era numeric,
  ra_9 numeric,
  bb_9 numeric,
  hr_9 numeric,
  whip numeric,
  primary key(name, season, date)
);

create table replacement_level_overall (
  season integer,
  g	integer,
  pa integer,
  ab integer,
  r integer,
  h integer,
  x2b integer,
  x3b integer,
  hr integer,
  rbi integer,
  bb integer,
  so integer,
  hbp integer,
  tb integer,
  xbh integer,
  sf integer,
  sh integer,
  gdp integer,
  sb integer,
  cs integer,
  go integer,
  fo integer,
  avg numeric,
  obp numeric,
  slg numeric,
  ops numeric,
  go_fo numeric,
  hbp_p numeric,
  bb_p numeric,
  so_p numeric,
  iso numeric,
  babip numeric,
  sar numeric,
  sbr numeric,
  wsb numeric,
  woba numeric,
  wraa numeric,
  off numeric,
  wrc numeric,
  wrc_p numeric,
  off_p numeric,
  off_pa numeric,
  primary key(season)
);

create table replacement_level_conference (
  season integer,
  g	integer,
  pa integer,
  ab integer,
  r integer,
  h integer,
  x2b integer,
  x3b integer,
  hr integer,
  rbi integer,
  bb integer,
  so integer,
  hbp integer,
  tb integer,
  xbh integer,
  sf integer,
  sh integer,
  gdp integer,
  sb integer,
  cs integer,
  go integer,
  fo integer,
  avg numeric,
  obp numeric,
  slg numeric,
  ops numeric,
  go_fo numeric,
  hbp_p numeric,
  bb_p numeric,
  so_p numeric,
  iso numeric,
  babip numeric,
  sar numeric,
  sbr numeric,
  wsb numeric,
  woba numeric,
  wraa numeric,
  off numeric,
  wrc numeric,
  wrc_p numeric,
  off_p numeric,
  off_pa numeric,
  primary key(season)
);

create table league_offense_overall (
    season integer,
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    sb integer,
    cs integer,
    hbp integer,
    sf integer,
    sh integer,
    tb integer,
    xbh integer,
    gdp integer,
    go integer,
    fo integer,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    go_fo numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    iso numeric,
    babip numeric,
    sar numeric,
    lg_r_pa numeric,
    bsr_bmult numeric,
    bsr numeric,
    lw_hbp numeric,
    lw_bb numeric,
    lw_x1b numeric,
    lw_x2b numeric,
    lw_x3b numeric,
    lw_hr numeric,
    lw_sb numeric,
    lw_cs numeric,
    lw_out numeric,
    ww_hbp numeric,
    ww_bb numeric,
    ww_x1b numeric,
    ww_x2b numeric,
    ww_x3b numeric,
    ww_hr numeric,
    woba_scale numeric,
    woba numeric,
    sbr numeric,
    lg_wsb numeric,
    wsb numeric,
    wraa numeric,
    off numeric,
    wrc numeric,
    wrc_p numeric,
    off_p numeric,
    rep_level numeric,
    rar numeric,
    primary key(season)
);

create table league_offense_conference (
    season integer,
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    sb integer,
    cs integer,
    hbp integer,
    sf integer,
    sh integer,
    tb integer,
    xbh integer,
    gdp integer,
    go integer,
    fo integer,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    go_fo numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    iso numeric,
    babip numeric,
    sar numeric,
    lg_r_pa numeric,
    bsr_bmult numeric,
    bsr numeric,
    lw_hbp numeric,
    lw_bb numeric,
    lw_x1b numeric,
    lw_x2b numeric,
    lw_x3b numeric,
    lw_hr numeric,
    lw_sb numeric,
    lw_cs numeric,
    lw_out numeric,
    ww_hbp numeric,
    ww_bb numeric,
    ww_x1b numeric,
    ww_x2b numeric,
    ww_x3b numeric,
    ww_hr numeric,
    woba_scale numeric,
    woba numeric,
    sbr numeric,
    lg_wsb numeric,
    wsb numeric,
    wraa numeric,
    off numeric,
    wrc numeric,
    wrc_p numeric,
    off_p numeric,
    rep_level numeric,
    rar numeric,
    primary key(season)
);

create table league_pitching_overall (
  season integer,
  g integer,
  w integer,
  l integer,
  sv integer,
  cg integer,
  sho integer,
  ip numeric,
  h integer,
  r integer,
  er integer,
  bb integer,
  so integer,
  x2b integer,
  x3b integer,
  hr integer,
  ab integer,
  wp integer,
  hbp integer,
  bk integer,
  sf integer,
  sh integer,
  pa integer,
  avg numeric,
  obp numeric,
  slg numeric,
  ops numeric,
  hbp_p numeric,
  bb_p numeric,
  so_p numeric,
  iso numeric,
  babip numeric,
  lob_p numeric,
  era numeric,
  ra_9 numeric,
  so_9 numeric,
  bb_9 numeric,
  hr_9 numeric,
  whip numeric,
  lg_r_pa numeric,
  bsr_bmult numeric,
  bsr numeric,
  bsr_9 numeric,
  fip_constant numeric,
  fip numeric,
  raa numeric,
  bsraa numeric,
  fipraa numeric,
  era_minus numeric,
  fip_minus numeric,
  bsr_minus numeric,
  primary key(season)
);

create table league_pitching_conference (
  season integer,
  g integer,
  ip numeric,
  h integer,
  r integer,
  er integer,
  bb integer,
  so integer,
  hr integer,
  era numeric,
  ra_9 numeric,
  so_9 numeric,
  bb_9 numeric,
  hr_9 numeric,
  whip numeric,
  raa numeric,
  era_minus numeric,
  primary key(season)
);
