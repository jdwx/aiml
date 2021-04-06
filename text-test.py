#!/usr/bin/env python3

import numpy as np
import pickle
import sys
import tensorflow as tf
import textwrap

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

print( "Loading model..." )
model = tf.keras.models.load_model( config[ 'trained_model_file' ] )
input_length = model.layers[ 0 ].input_length

doc = list( tokens_from_file( config[ 'test_file' ] ) )
keys = index.words_to_keys( doc )
keys = np.array( [ 0 ] * ( input_length - len( keys ) ) + keys[ -input_length : ] )
keys.shape = ( 1, input_length )
# print( keys )


words = []
for i in range( 50 ):
    print( keys )
    y = model.predict( keys )[ 0 ]
    # print( y )
    key = y.argmax()
    word = index.key_to_word[ key ]
    print( y[ key ], key, word )

    keys = np.append( keys[ : , 1 : ], [ [ key ] ], 1 )
    # print( keys )
    # print( keys.shape )
    words.append( word )


print( "Input:" )
print( "\n".join( textwrap.wrap( ' '.join( doc ) ) ) )

print( "[machine-generated text starts here]" )
print( "\n".join( textwrap.wrap( ' '.join( words ) ) ) )

