#!/usr/bin/env python3

import fasttext
import json
import numpy as np
import pickle
import sys
import tensorflow as tf


from lib.Config import config_from_tag
from lib.Index import Index


config = config_from_tag( sys.argv[ 1 ] )

print( "Reading raw embed model..." )
raw_embed = fasttext.load_model( config[ 'raw_embed' ] )

print( "Reading parent embed model..." )
parent_embed = fasttext.load_model( config[ 'parent_embed' ] )

print( "Loading training data..." )
with open( config[ 'embed_merge_file' ] ) as f:
    x = json.load( f )
    in_set = x[ 'in_set' ]
    out_set = x[ 'out_set' ]
    del x

print( "Loading model..." )
model = tf.keras.models.load_model( config[ 'embed_merge_model' ] )

print( "Loading index..." )
index = Index( config[ 'index_file' ] )

print( "Applying transform..." )
matrix = np.empty( ( len( out_set ), 300 ), dtype = np.float )
i = 0
word_in_matrix = {}
for word in out_set:
    matrix[ i, : ] = raw_embed[ word ]
    word_in_matrix[ word ] = i
    i += 1

print( matrix.shape )

y_matrix = model.predict( matrix )

print( "Collecting final embed matrix..." )
embed_weights = np.empty( ( len( index ), 300  ) )

for i in range( len( index ) ):
    word = index.key_to_word[ i ]
    if 0 == i:
        vec = np.zeros( 300 )
    elif word in out_set:
        vec = y_matrix[ word_in_matrix[ word ] ]
    else:
        vec = parent_embed[ word ]
    embed_weights[ i, : ] = vec

print( "Writing embed matrix..." )
with open( config[ 'embed_weights' ], 'wb' ) as f:
    pickle.dump( embed_weights, f )

print( "Done." )
