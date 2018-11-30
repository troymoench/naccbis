-- Create guts view
CREATE VIEW guts AS
SELECT season, lg_r_pa, bsr_bmult, lw_hbp, lw_bb, lw_x1b, lw_x2b, lw_x3b, lw_hr,
lw_sb, lw_cs, lw_out, ww_hbp, ww_bb, ww_x1b, ww_x2b, ww_x3b, ww_hr, woba_scale, rep_level
FROM league_offense_overall;
