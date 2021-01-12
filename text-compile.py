#!/usr/bin/env python3

import jsonlines
import pickle
import sys
import tensorflow as tf


from lib.Config import config_from_tag


def make_example( x, y ):
    return tf.train.Example(
        features = tf.train.Features( feature = {
            'data': tf.train.Feature(
                int64_list = tf.train.Int64List( value = x )
            ),
            'label': tf.train.Feature(
                float_list = tf.train.FloatList( value = y )
            ),
        } )
    )


def compile_json_to_tfrecords( in_path, out_path ):
    with jsonlines.open( in_path ) as rdr, tf.io.TFRecordWriter( out_path ) as wri:
        for sample in rdr:
            ex = make_example( sample[ 0 ], embed_weights[ sample[ 1 ] ]  )
            wri.write( ex.SerializeToString() )


config = config_from_tag( sys.argv[ 1 ] )

print( "Loading embed weights..." )
with open( config[ 'embed_weights' ], 'rb' ) as f:
    embed_weights = pickle.load( f )

print( "Compiling training set..." )
compile_json_to_tfrecords( config[ 'train_json' ], config[ 'train_tf' ] )

print( "Compiling validation set..." )
compile_json_to_tfrecords( config[ 'val_json' ], config[ 'val_tf' ] )
