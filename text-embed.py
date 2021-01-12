#!/usr/bin/env python3

import fasttext
import sys


from lib.Config import config_from_tag

config = config_from_tag( sys.argv[ 1 ] )

print( "Training FastText embedding model..." )
embed = fasttext.train_unsupervised( config[ 'fasttext_file' ], minCount = 1, epoch = 10, dim = 300 )

print( "Saving trained model..." )
embed.save_model( config[ 'raw_embed' ] )

print( "Done!" )
