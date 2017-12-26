import psycopg2

# This script reads in an sql file with the DDL for a new table
# The sql file name is stored in the fname variable

conn = psycopg2.connect(host="192.168.0.101", database="naccbisdb", user="troy", password="baseballisfun")
cur = conn.cursor()

# might need to change numeric to double

fname = "raw_team_pitching_conference.sql"
with open(fname, 'r') as f:
    query = f.read()

print(query)

cur.execute(query)

conn.commit()

cur.close()
conn.close()
