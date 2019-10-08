# NACCBIS Data Cleaning Document

This living document explains the architectural and design choices made
during the development of the data cleaning script(s).  

## Dump Names for Inspection

A single script will be used to dump player names for manual/automated inspection to identify corrections.  
Any corrections that are identified should be manually loaded into the name_corrections database table.
The script will provide the option to apply name corrections that were previously identified and present in the name_corrections table.

### Typos

To identify name inconsistencies due to typos, the Levenshtein string distance algorithm will be used.

Find all player-season pairs such that:
* Levenshtein distance between last names is 1
* Levenshtein distance between first names is 1

### Nicknames

To identify name inconsistencies due to nicknames, a nickname lookup table will be used.  

### Transfers and Duplicate Names

To identify players who have either transferred to another NACC team or share a name with another player, find all player-seasons that have the same name but different teams.  

Any transfers and duplicate names should be manually loaded into the duplicate_names database table.

## Generate Player Ids

A single script will be used to generate player ids and load them into the database

A player id takes the following format:  

`<first 5 characters of last name><first 2 characters of first name><2 digits>`  
The last two integer digits allow for the prevention of ID conflicts.

For example:  
`Curtis Engelbrecht` -> `engelcu01`  
`Garrett Balind` -> `balinga01`  
`Galen Balinski` -> `balinga02`  

The script will then load the player-seasons along with the associated player id into the player_id database table.
