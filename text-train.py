#!/usr/bin/env python3

import json
import os
import tensorflow as tf

from functools import partial
from tensorflow.data import AUTOTUNE


def read_tfrecord( example, tffeatures ):
    example = tf.io.parse_single_example( example, features = tffeatures )
    # y = example[ 'label' ]
    y = tf.SparseTensor( indices = [ example[ 'label' ] ], values = [ 1.0 ], dense_shape = [ vocab_size ] )
    return example[ 'data' ], tf.sparse.to_dense( y )


def get_dataset( filenames, tffeatures, batch_size ):
    ds_options = tf.data.Options()
    ds_options.experimental_deterministic = False
    dataset = tf.data.TFRecordDataset( filenames )
    dataset = dataset.with_options( ds_options )
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


print( "Building strategy & model." )
strategy = tf.distribute.MirroredStrategy()
print( 'Number of devices: {}'.format(strategy.num_replicas_in_sync))
with strategy.scope():
    model = make_or_restore_model( checkpoint_dir, "model.h5" )
    in_size = model.layers[ 0 ].input_shape[ 1 ]
    vocab_size = model.layers[ -1 ].output_shape[ 1 ]
    print( model.summary() )

xfeatures = {
    'data': tf.io.FixedLenFeature( in_size, tf.int64 ),
    'label': tf.io.FixedLenFeature( 1, tf.int64 ),
}

train_data = get_dataset( [ "train.tfrecords" ], xfeatures, params[ 'batch_size' ] )
val_data = get_dataset( [ "val.tfrecords" ], xfeatures, params[ 'batch_size' ] )

options = tf.data.Options()
options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.DATA
train_data = train_data.with_options( options )
val_data = val_data.with_options( options )

callbacks = [
    tf.keras.callbacks.ModelCheckpoint(
        filepath = checkpoint_dir + '/check-loss={loss:.2f}',
        save_freq = 'epoch',
        save_best_only = True,
    ),
    tf.keras.callbacks.EarlyStopping(
        monitor = 'val_loss', patience = 5, restore_best_weights = True
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
