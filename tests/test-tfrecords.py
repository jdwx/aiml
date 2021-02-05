#!/usr/bin/env python3


import sys
import tensorflow as tf


from functools import partial
from tensorflow.data.experimental import AUTOTUNE


def read_tfrecord( example, read_features ):
    example = tf.io.parse_single_example( example, features = read_features )
    label = example[ 'label' ]
    label = tf.reshape( label, [ 1, 1 ] )
    print( label )
    label = tf.SparseTensor( indices = label, values = [ 1.0 ], dense_shape = [ vocab_size ] )
    print( label )
    label = tf.sparse.to_dense( label, default_value = 0.0 )
    return example[ 'data' ], label


def get_dataset( filenames, get_features, batch_size ):
    options = tf.data.Options()
    options.experimental_deterministic = True
    dataset = tf.data.TFRecordDataset( filenames )
    dataset = dataset.with_options( options )
    dataset = dataset.map(
        partial( read_tfrecord, read_features = get_features ),
        num_parallel_calls = AUTOTUNE
    )
    # dataset = dataset.shuffle( 2048 )
    dataset = dataset.prefetch( buffer_size = AUTOTUNE )
    dataset = dataset.batch( batch_size )
    return dataset


tfrecords_file = sys.argv[ 1 ]
features = {
    'data': tf.io.FixedLenFeature( [ 500 ], tf.int64 ),
    'label': tf.io.FixedLenFeature( [ 1 ], tf.int64 ),
}
vocab_size = 23257

my_dataset = get_dataset( [ tfrecords_file ], features, 8 )

x, y = next( iter( my_dataset ) )
print( "len( x ) =", len( x ) )
print( "len( x[ 0 ] ) =", len( x[ 0 ] ) )
print( "len( y ) =", len( y ) )
print( "len( y[ 0 ] ) =", len( y[ 0 ] ) )
print( "x[ 0 ] =", x[ 0 ] )
print( "y[ 0 ] =", repr( y[ 0 ] ) )
print( y )

x = y[ 0 ].numpy()
for i in range( len( x ) ):
    if x[ i ] != 0:
        print( i, x[ i ] )
