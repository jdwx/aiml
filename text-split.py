#!/usr/bin/env python3

import jsonlines
import random
import sys

from lib.Config import config_from_tag


config = config_from_tag( sys.argv[ 1 ] )

print( "Reading X-Y samples..." )
data = []
with jsonlines.open( config[ 'xy_json' ] ) as rdr:
    for sample in rdr:
        data.append( sample )
data_len = len( data )
train_len = int( data_len * config[ 'train_val_split' ] )

print( "Shuffling samples..." )
random.shuffle( data )

print( "Writing training set..." )
with jsonlines.open( config[ 'train_json' ], 'w' ) as wri:
    for i in range( train_len ):
        wri.write( data[ i ] )

print( "Writing validation set..." )
with jsonlines.open( config[ 'val_json' ], 'w' ) as wri:
    for i in range( train_len, data_len ):
        wri.write( data[ i ] )

print( "Done!" )
