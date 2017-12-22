import psycopg2

conn = psycopg2.connect(host="192.168.0.101", database="naccbisdb", user="troy", password="baseballisfun")
cur = conn.cursor()


# query = """create table team_ids
#   (name varchar(30),
#   id varchar(5)
# )"""
#
# cur.execute(query)


values = [('Aurora', 'AUR'),
('Benedictine', 'BEN'),
('Concordia Chicago', 'CUC'),
('Concordia Wisconsin', 'CUW'),
('Dominican', 'DOM'),
('Edgewood', 'EDG'),
('Lakeland', 'LAK'),
('MSOE', 'MSOE'),
('Marian', 'MAR'),
('Maranatha', 'MARN'),
('Rockford', 'ROCK'),
('Wisconsin Lutheran', 'WLC')]

for value in values:
    cur.execute("INSERT INTO team_ids VALUES (%s,%s)", value)

conn.commit()

cur.close()
conn.close()
