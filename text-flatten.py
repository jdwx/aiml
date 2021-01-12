#!/usr/bin/env python3

import jsonlines
import sys

from lib.Config import config_from_tag
from lib.Flatten import completely_flatten


config = config_from_tag( sys.argv[ 1 ] )

print( "Flattening keys..." )
with jsonlines.open( config[ 'keys_json'] ) as rdr, jsonlines.open( config[ 'flat_keys_json' ], 'w' ) as wri:
    for doc in rdr:
        wri.write( completely_flatten( doc ) )

print( "Done!" )
