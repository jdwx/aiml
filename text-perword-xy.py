#!/usr/bin/env python3

import jsonlines
import sys


from lib.Config import config_from_tag


config = config_from_tag( sys.argv[ 1 ] )
context_size = config[ 'per_word_context' ]
dimensions = 300

blank_x = [ 0 ] * context_size

print( "Generating keyed X-Y per-word samples..." )
with jsonlines.open( config[ 'flat_keys_json' ] ) as rdr, jsonlines.open( config[ 'xy_json' ], 'w' ) as wri:
    for doc in rdr:
        x = list( blank_x )
        for y in doc:
            wri.write( [ x, y ] )
            x.append( y )
            x = x[ -context_size : ]

print( "Done!" )
