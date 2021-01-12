#!/usr/bin/env python3

import fasttext
import json
import numpy as np
import random
import sys


from lib.Config import config_from_tag


config = config_from_tag( sys.argv[ 1 ] )

print( "Reading raw embed model..." )
raw_embed = fasttext.load_model( config[ 'raw_embed' ] )
print( "raw embed size =", len( raw_embed.words ) )
print( "raw first word =", raw_embed.words[ 0 ] )

print( "Reading parent embed model..." )
parent_embed = fasttext.load_model( config[ 'parent_embed' ] )
parent_words = parent_embed.get_words( on_unicode_error = 'replace' )

print( "parent embed size =", len( parent_words ) )
print( "parent first word =", parent_words[ 0 ] )

print( "Finding words in common..." )
in_set = set()
out_set = set()

for word in raw_embed.words:
    if word in parent_words:
        in_set.add( word )
    else:
        out_set.add( word )

print( "Words in common:", len( in_set ) )
print( "Unique words:", len( out_set ) )

print( "Building transformation dataset..." )
data = []
for word in in_set:
    data.append( ( raw_embed[ word ], parent_embed[ word ] ) )


print( "Shuffling transformation dataset...")
random.shuffle( data )
train_len = int( len( data ) * config[ 'train_val_split' ] )

print( "Splitting training & validation data..." )
train_data = np.array( data[ 0 : train_len ] )
val_data = np.array( data[ train_len : ] )

train_x = train_data[ :, 0 ].tolist()
train_y = train_data[ :, 1 ].tolist()
val_x = val_data[ :, 0 ].tolist()
val_y = val_data[ :, 1 ].tolist()

print( "Writing output data..." )
x = {
    "train_x": train_x,
    "train_y": train_y,
    "val_x": val_x,
    "val_y": val_y,
    "in_set": list( in_set ),
    "out_set": list( out_set ),
}

with open( config[ 'embed_merge_file' ], 'w' ) as f:
    json.dump( x, f )

print( "Done." )
