#!/usr/bin/env python3

import numpy as np
import pickle
import sys
import tensorflow as tf

from lib.Config import config_from_tag
from lib.Index import Index
from lib.Parse import tokens_from_file
from lib.Flatten import flatten_list
from numpy import dot
from numpy.linalg import norm


def cossimit( vec ):
    best = 0
    score = -2
    nvec = norm( vec )
    for i in range( len( embed_weights ) ):
        now = dot( vec, embed_weights[ i, : ] ) / ( nvec * norm( embed_weights[ i, : ] ) )
        if now > score:
            best = i
            score = now
    print( best, score )
    return best


config = config_from_tag( sys.argv[ 1 ] )

print( "Loading embed weights..." )
with open( config[ 'embed_weights' ], 'rb' ) as f:
    embed_weights = pickle.load( f )

print( "Loading index..." )
index = Index( config[ 'index_file' ] )

doc = list( tokens_from_file( config[ 'test_file' ] ) )
print( doc )
keys = index.words_to_keys( doc )
keys = np.array( [ 0 ] * ( 500 - len( keys ) ) + keys )
keys.shape = ( 1, 500 )
print( keys )


model = tf.keras.models.load_model( "model-trained-cossim.h5" )
input_length = model.layers[ 0 ].input_length

print( doc )
for i in range( 1 ):
    # print( keys )
    y = model.predict( keys )[ 0 ]
    print( y )
    key = cossimit( y )
    word = index.key_to_word[ key ]
    # print( key, word )

    keys = np.append( keys[ : , 1 : ], [ [ key ] ], 1 )
    #print( keys )
    #print( keys.shape )
    print( word )

