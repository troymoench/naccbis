import psycopg2

conn = psycopg2.connect(host="192.168.0.101", database="naccbisdb", user="troy", password="baseballisfun")
cur = conn.cursor()

# might need to change numeric to double

query = """
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
)
"""
cur.execute(query)

conn.commit()

cur.close()
conn.close()
