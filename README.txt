Converts multiple pgn files to csv structure.

Usage : python pgn2csv.py -d <root_directory_where_to_start_looking_for_pgns> -o <output_directory> -i <id_starting_point>
or    : python pgn2csv.py -f <lonely_pgn_path> -o <output_directory> -i <id_starting_point>
help  : python pgn2csv.py --help

All arguments are optional. If neither is specified then pgn2csv runs in directory mode where it considers as source directory (-d) the current directory(the one where script is executed) and as output directory (the same). The id default initial value is 1.

So the easiest way to execute is to put pgn2csv.py in the top folder( where the pgn files are ) in your disk and just run:
>> python pgn2csv.py

Since Version 0.6 and later, pgn2csv recursively finds all pgns from -d subfolders

=== CHANGES in v1.5 ===

This should be portable to any directory structure naming (unix's or dos's)
Fixed foutName bug in process_file

=== CHANGES in v1.4 ===

Since this version, an additional column is added before moves, called 'Title' (this is convinient when importing nodes in drupal).
This is autofilled with the value [White] - [Black], aka: the names with a dash in the middle.

Also since now the id default value is 1 instead of 0 which was what v1.2 introduced when supposed to fix that lol 


=== CHANGES in v1.3 ===

Guess what. Just fixed another idiotic bug.
Moves wasn't printing in the exact corresponding column, instead it was printing one empty column after the last tag. (aka:
We had an empty column in the values : , , 


=== CHANGES in v1.2 ===

Fixed the following bug:
counter (id) specified by argument -i was incremented before writed so we had a +1 initial starting point in the id column


=== CHANGES in v1.1 ===

Critical bug fixed when occuring EventDate tag, script was executing the part of the code belonging to 'Event' tag...
bakery style fix for the time being by making the condition statement 
if line[0:7] == '[Event ': 

(trolol) y i know


=== CHANGES in v1.0 ===

Id counter can now be initialized from command line (-i , --id)-argument
Since now script doesn't make use of the odict.py file, it imports the apporpirate library instead


=== CHANGES in v0.9 ===

Completely rewritten(process_file func) so that now we identify the tags readed, storing them in an ordered Dictionary and then
writting to file (csv) with the appropriate order. It ignores all the unidentified tags (see below the list with tags searching).

By that way we can assume that since now png2csv convertor car read ANY type of pgn and produce a similar(same columns) csv file.

The standard column(tags) are now:
Id, Event, Site, Date, Round, White, Black, Result, ECO, WhiteTitle, WhiteElo, WhiteFideId, BlackTitle, BlackElo, BlackFideId, EventDate, Opening, Variation, Moves


=== CHANGES in v0.8 ===

1. Completely different logic of detecting tags. Since now we read the 7 standard tags (by wikipedia pgn specification : http://en.wikipedia.org/wiki/Portable_Game_Notation#Tag_pairs ) and IGNORE all the others below until the moves section

2. Added an Id column before 'Event' needed by the drupal's module 


=== CHANGES in v0.7 ===

Since Version 0.7 and later, pgn2csv surrounds moves section(cell) with [pgn] , [/pgn] tags used by : http://code.google.com/p/pgn4web/wiki/User_Notes_drupal


