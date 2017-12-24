import psycopg2

conn = psycopg2.connect(host="192.168.0.101", database="naccbisdb", user="troy", password="baseballisfun")
cur = conn.cursor()

# might need to change numeric to double

query = """
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
)
"""
cur.execute(query)

conn.commit()

cur.close()
conn.close()
