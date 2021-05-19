-- Find players that have the same names but different teams
\echo Pitchers
select name, team, min(season), max(season) from raw_pitchers_overall group by name, team having name in
(select bar.name from
  (select foo.name, count(*) from
  (select name, team from raw_pitchers_overall group by name, team) as foo
  group by foo.name having foo.count > 1) as bar) order by name;

\echo Batters
select name, team, min(season), max(season) from raw_batters_overall group by name, team having name in
(select bar.name from
  (select foo.name, count(*) from
  (select name, team from raw_batters_overall group by name, team) as foo
  group by foo.name having foo.count > 1) as bar) order by name;
