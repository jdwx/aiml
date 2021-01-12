#!/usr/bin/env python3


import sys

import jsonlines

from lib.Config import config_from_tag
from lib.Index import Index


config = config_from_tag( sys.argv[ 1 ] )

index = Index()

with jsonlines.open( config[ 'body_json' ] ) as rdr:
    for doc in rdr:
        for sent in doc:
            for word in sent:
                index.add_once( word )


print( "Index size:", len( index ) )

index.save( config[ 'index_file' ] )

print( "Wrote index:", config[ 'index_file' ] )
