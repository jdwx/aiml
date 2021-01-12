#!/usr/bin/env python3

import json
import os
import tensorflow as tf

from functools import partial
from tensorflow.data import AUTOTUNE


def read_tfrecord( example, tffeatures ):
    example = tf.io.parse_single_example( example, features = tffeatures )
    return example[ 'data' ], example[ 'label' ]


def get_dataset( filenames, tffeatures, batch_size ):
    options = tf.data.Options()
    options.experimental_deterministic = False
    dataset = tf.data.TFRecordDataset( filenames )
    dataset = dataset.with_options( options )
    dataset = dataset.map(
        partial( read_tfrecord, tffeatures = tffeatures ),
        num_parallel_calls = AUTOTUNE
    )
    dataset = dataset.prefetch( buffer_size = AUTOTUNE )
    dataset = dataset.batch( batch_size )
    return dataset


def make_or_restore_model( model_checkpoint_dir, model_path ):
    checkpoints = [ model_checkpoint_dir + '/' + name
                    for name in os.listdir( model_checkpoint_dir ) ]
    if not checkpoints:
        print( "Loading original model." )
        return tf.keras.models.load_model( model_path )

    latest_checkpoint = max( checkpoints, key = os.path.getctime )
    print( "Restoring from:", latest_checkpoint )
    return tf.keras.models.load_model( latest_checkpoint )


with open( "params.json" ) as f:
    params = json.load( f )

checkpoint_dir = 'checkpoints'
if not os.path.exists( checkpoint_dir ):
    print( "Making checkpoint directory." )
    os.makedirs( checkpoint_dir )

model = make_or_restore_model( checkpoint_dir, "model.h5" )
xfeatures = {
    'data': tf.io.FixedLenFeature( [ params[ 'in_size'] ], tf.int64 ),
    'label': tf.io.FixedLenFeature( [ params[ 'out_size' ] ], tf.float32 ),
}


train_data = get_dataset( [ "train.tfrecords" ], xfeatures, params[ 'batch_size' ] )
val_data = get_dataset( [ "val.tfrecords" ], xfeatures, params[ 'batch_size' ] )


callbacks = [
    tf.keras.callbacks.ModelCheckpoint(
        filepath = checkpoint_dir + '/check-loss={loss:.2f}',
        save_freq = 'epoch',
        save_best_only = True,
    ),
    tf.keras.callbacks.EarlyStopping(
        monitor = 'val_cosine_similarity', patience = 5, restore_best_weights = True
    )
]


hist = model.fit(
    train_data,
    validation_data = val_data,
    epochs = params[ 'epochs' ],
    verbose = 1,
    callbacks = callbacks
)
model.save( "model-trained.h5" )
print( hist )
