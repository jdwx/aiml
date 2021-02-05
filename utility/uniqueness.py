#!/usr/bin/env python3

#
# This looks at the flat corpus and attempts to estimate how many
# words of lookback are needed for unique context.
#


import jsonlines
import sys


from lib.Config import config_from_tag
from lib.Index import Index


config = config_from_tag( sys.argv[ 1 ] )
index = Index( config[ 'index_file' ] )

context_size = 87

blank_x = [ 0 ] * context_size

data = {}
i = 0
with jsonlines.open( config[ 'flat_keys_json' ] ) as rdr:
    for doc in rdr:
        x = []
        for y in doc:
            if len( x ) < context_size:
                x.append( y )
                continue
            xkey = ' '.join( [ str( z ) for z in x ] )
            if xkey not in data:
                data[ xkey ] = {}
            if y not in data[ xkey ]:
                data[ xkey ][ y ] = 0
            data[ xkey ][ y ] += 1
            x.append( y )
            x = x[ -context_size : ]

most = 0
mosttext = ""
total = 0
for text in data:
    num = len( data[ text ] )
    if num > 1:
        total += 1
    if num > most:
        print( text, ":", num )
        most = num
        mosttext = text

print( "Total", total, " non-unique sequences." )
print( most, ":", mosttext, ":", data[ mosttext ] )
keys = [ int( key ) for key in mosttext.split( ' ' ) ]
print( index.keys_to_words( keys ) )
