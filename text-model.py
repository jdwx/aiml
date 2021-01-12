#!/usr/bin/env python3

import json
import pickle
import sys
import tensorflow as tf

from lib.Config import config_from_tag
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional, Dropout, Reshape
from tensorflow.keras.models import Sequential


config = config_from_tag( sys.argv[ 1 ] )

print( "Loading pre-trained embed weights..." )
with open( config[ 'embed_weights' ], 'rb' ) as f:
    embed_weights = pickle.load( f )

vocab_size = embed_weights.shape[ 0 ]
embed_dims = embed_weights.shape[ 1 ]

print( "Building model..." )
model = Sequential()
model.add( Embedding(
    vocab_size,
    embed_dims,
    weights = [ embed_weights ],
    input_length = config[ 'per_word_context' ],
    trainable = False
) )
model.add( LSTM( 300, return_sequences = True ) )
model.add( Dropout( 0.2 ) )
model.add( LSTM( 300 ) )
model.add( Dense( 600, activation = 'relu' ) )
model.add( Dense( embed_dims ) )
model.compile( loss = 'cosine_similarity', optimizer = 'adam', metrics = [ tf.keras.metrics.CosineSimilarity(axis=1) ] )

print( "Saving model..." )
model.save( config[ 'model_file' ] )
print( model.summary() )
print( "Done!" )

print( "Writing model params..." )
params = {
    'batch_size': 512,
    'epochs': 100,
    'in_size': config[ 'per_word_context' ],
    'out_size': 300
}

with open( config[ 'model_params' ], 'w' ) as f:
    json.dump( params, f )
