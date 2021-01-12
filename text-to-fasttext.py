#!/usr/bin/env python3

import jsonlines
import sys


from lib.Config import config_from_tag

config = config_from_tag( sys.argv[ 1 ] )

print( "Writing flat text file for FastText embedding..." )
with jsonlines.open( config[ 'body_json' ] ) as rdr, open( config[ 'fasttext_file' ], 'w' ) as wri:
    for doc in rdr:
        for sent in doc:
            wri.write( ' '.join( sent ) + "\n" )

print( "Done." )