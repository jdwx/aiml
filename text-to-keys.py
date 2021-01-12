#!/usr/bin/env python3

import jsonlines
import sys

from lib.Config import config_from_tag
from lib.Index import Index


config = config_from_tag( sys.argv[ 1 ] )
index = Index( config[ 'index_file' ] )


print( "Converting words to keys..." )
with jsonlines.open( config[ 'body_json' ] ) as rdr, jsonlines.open( config[ 'keys_json' ], 'w' ) as wri:
    for in_doc in rdr:
        wri.write( index.words_to_keys( in_doc ) )

print( "Done!" )
