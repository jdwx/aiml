

import os
import sys

sys.path.append( os.path.abspath( ".." ) )

from lib.Parse import format_for_fasttext

sts = [

    [ "I dun't keer what folks think--ef Lavinny's boy looked like his pa, he wouldn't look like nothin' ye expeck.",
      "I dun't keer what folks think -- ef Lavinny's boy looked like his pa , he wouldn't look like nothin' ye expeck ." ],

    [ "Lavinny's read some, an' has seed some things the most o' ye only tell abaout.",
      "Lavinny's read some , an' has seed some things the most o' ye only tell abaout ." ],

    [ "I calc'late her man is as good a husban' as ye kin find this side of Aylesbury; an' ef ye knowed as much abaout the hills as I dew, ye wouldn't ast no better church weddin' nor her'n.",
      "I calc'late her man is as good a husban' as ye kin find this side of Aylesbury ; an' ef ye knowed as much abaout the hills as I dew , ye wouldn't ast no better church weddin' nor her'n ." ],

    [ "Let me tell ye suthin'--some day yew folks'll hear a child o' Lavinny's a-callin' its father's name on the top o' Sentinel Hill!",
      "Let me tell ye suthin' -- some day yew folks'll hear a child o' Lavinny's a-callin' its father's name on the top o' Sentinel Hill !" ],

    [ "At 11:15 a.m., Sept. 27, I stirred vigorously.",
      "At 11:15 a.m. , Sept. 27 , I stirred vigorously ." ],

    [ "I saw only one thing: myself.", "I saw only one thing : myself ." ],

    [ "She said, \"Yes.\"", "She said , \" Yes . \"" ],

    [ "\"Yes,\" she said, \"I think so.\"", "\" Yes , \" she said , \" I think so . \"" ],

    [ "There was (once) another way.", "There was ( once ) another way ." ],

    [ "Dashes are--I feel--very wishy-washy.", "Dashes are -- I feel -- very wishy - washy ."],

]

for ( before, check ) in sts:
    after = format_for_fasttext( before )
    if check == after:
        print( "OK:", check )
    else:
        print( "From:", before )
        print( "Gave:", after )
        print( "Want:", check )
