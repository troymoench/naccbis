with split_names as (
    select regexp_split_to_array(name, '\s+') as split_name, team, season, pos from raw_batters_overall
    union all
    select regexp_split_to_array(name, '\s+') as split_name, team, season, pos from raw_pitchers_overall
), lname_fname as (
    select split_name[1] as fname, array_to_string(split_name[2:], ' ') as lname, team, season, pos from split_names
)
select l1.*, l2.* from lname_fname l1
join lname_fname l2 on
levenshtein(l1.lname, l2.lname) = 1
-- l1.lname = l2.lname
and
-- levenshtein(l1.fname, l2.fname) = 1;
l1.fname = l2.fname;
