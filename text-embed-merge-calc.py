#!/usr/bin/env python3

import json
import sys
import tensorflow as tf


from lib.Config import config_from_tag
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential


config = config_from_tag( sys.argv[ 1 ] )

print( "Loading training data..." )
with open( config[ 'embed_merge_file' ] ) as f:
    x = json.load( f )
    train_x = x[ 'train_x' ]
    train_y = x[ 'train_y' ]
    val_data = ( x[ 'val_x' ], x[ 'val_y' ] )
    del x

print( "Building model..." )
callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor = 'val_cosine_similarity', patience = 10, restore_best_weights = True
    )
]

model = Sequential()
model.add( Dense( 300, activation = 'relu', input_shape = (300,) ) )
model.add( Dense( 600, activation = 'relu' ) )
model.add( Dense( 300 ) )
model.compile( loss = 'cosine_similarity', optimizer = 'adam', metrics = [ tf.keras.metrics.CosineSimilarity(axis=1) ] )
print( model.summary() )

print( "Fitting begins..." )
model.fit( train_x, train_y, epochs = 100, verbose = 1, validation_data = val_data, callbacks = callbacks )

print( "Saving model..." )
model.save( config[ 'embed_merge_model' ] )

print( "Done!" )
