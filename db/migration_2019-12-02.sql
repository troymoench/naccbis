ALTER TABLE batters_overall
ADD CONSTRAINT fk_batters_overall_fname_player_id
FOREIGN KEY(fname, lname, team, season)
REFERENCES player_id (fname, lname, team, season)
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE batters_conference
ADD CONSTRAINT fk_batters_conference_fname_player_id
FOREIGN KEY(fname, lname, team, season)
REFERENCES player_id (fname, lname, team, season)
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE pitchers_overall
ADD CONSTRAINT fk_pitchers_overall_fname_player_id
FOREIGN KEY(fname, lname, team, season)
REFERENCES player_id (fname, lname, team, season)
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE pitchers_conference
ADD CONSTRAINT fk_pitchers_conference_fname_player_id
FOREIGN KEY(fname, lname, team, season)
REFERENCES player_id (fname, lname, team, season)
ON DELETE CASCADE ON UPDATE CASCADE;
